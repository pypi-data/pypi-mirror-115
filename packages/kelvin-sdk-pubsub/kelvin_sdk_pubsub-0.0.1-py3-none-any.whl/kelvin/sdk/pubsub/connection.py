"""Connections."""

# TODO
# - check inbound data types

from __future__ import annotations

import asyncio
from asyncio import Task
from queue import Empty, Full, Queue
from types import TracebackType
from typing import Any, AsyncIterator, Dict, List, Optional, Sequence, Tuple, Type, TypeVar, Union

import structlog
from asyncio_mqtt import Client as AsyncClient
from paho.mqtt.client import Client, MQTTMessage

from kelvin.icd import Message
from kelvin.icd.message import Endpoint

from .config import PubSubClientConfig, Selector
from .utils import coalesce

logger = structlog.get_logger(__name__)

E = TypeVar("E", bound=Exception)


class Connection:
    """Pub-Sub Connection."""

    _input_count: int = 0
    _output_count: int = 0

    config: PubSubClientConfig

    def __init__(self, config: PubSubClientConfig) -> None:
        """Initialise the connection."""

        self.config = config

    @property
    def stats(self) -> Dict[str, Any]:
        """Provide connection statistics."""

        return {
            "input_count": self._input_count,
            "output_count": self._output_count,
        }

    def _make_messages(self, topic: str, payload: bytes) -> List[Message]:
        """Make messages."""

        message = Message.decode(payload)

        header = message._
        target = header.target

        node_name = coalesce(target.node_name, "")
        workload_name = coalesce(target.workload_name, "")
        asset_name = coalesce(header.asset_name, "")
        name, data_type = header.name, header.type

        input_map = self.config.input_map

        key = Selector(node_name, workload_name, asset_name, name)
        items = input_map.get(key)
        if items is None:
            raise ValueError(f"Unknown input {key!r}") from None

        messages: List[Message] = []

        for item in items:
            input_name, input_data_type = item
            if input_data_type != data_type:
                logger.warning(
                    f"Skipping data with unexpected data-type {data_type!r} (expected {input_data_type})",
                    topic=topic,
                )
                continue
            if input_name != name:
                message_ = message.copy()
                message_._.name = input_name
                messages += [message_]
            else:
                messages += [message]

        return messages

    def _make_payloads(self, message: Message) -> List[Tuple[str, bytes]]:
        """Publish message."""

        config = self.config

        header = message._
        asset_name = coalesce(header.asset_name, "")
        name, data_type = header.name, header.type

        source, target = header.source, header.target

        source_, target_ = str(source), str(target)
        if not (source_ and target_ and asset_name):
            # fill missing information in header
            message = message.copy()
            header = message._
            if not asset_name:
                asset_name = header.asset_name = coalesce(config.asset_name, "")
            if not source_:
                source = header.source = Endpoint(
                    node_name=config.node_name,
                    workload_name=config.workload_name,
                )
            if not target_:
                target = header.target = source.copy()

        node_name = coalesce(target.node_name, "")
        workload_name = coalesce(target.workload_name, "")

        key = Selector(node_name, workload_name, asset_name, name)

        output_map = config.output_map
        items = output_map.get(key)
        if items is None:
            raise ValueError(f"Unknown output {key!r}") from None

        prefix = "output" if source == target else "input"

        payload = message.encode(False)

        payloads: List[Tuple[str, bytes]] = []

        for item in items:
            output_name, output_data_type = item
            if output_data_type != data_type:
                raise ValueError(
                    f"Unexpected data-type {data_type!r} (expected {output_data_type})"
                ) from None

            topic = f"{prefix}/{node_name}/{workload_name}/{asset_name}/{output_name}"
            payloads += [(topic, payload)]

            if prefix == "input":
                topic = f"output/{node_name}/{workload_name}/{asset_name}/{output_name}"
                payloads += [(topic, payload)]

        return payloads


S = TypeVar("S", bound="SyncConnection", covariant=True)


class SyncConnection(Connection):
    """Synchronous Pub-Sub Connection."""

    _client: Optional[Client] = None
    _queue: Queue

    def __init__(self, config: PubSubClientConfig) -> None:
        """Initialise the connection."""

        super().__init__(config)

        self._queue = Queue(maxsize=self.config.max_items)

    def connect(self) -> None:
        """Open connection."""

        self._input_count = self._output_count = 0

        client = self._client
        if client is not None:
            try:
                client.disconnect()
            except KeyboardInterrupt:
                raise
            except Exception:
                pass

        config = self.config
        client = self._client = config.broker_url.get_sync_client(
            config.client_id,
            config.username,
            config.password,
        )
        client.on_message = self._on_message

        topics = config.topics
        client.subscribe([(topic, config.qos) for topic in topics])

        topic_summary = "\n".join(f"  - {topic}" for topic in topics)
        logger.info(f"Subscribed to topics:\n{topic_summary}")

        client.loop_start()

    def disconnect(self) -> None:
        """Close connection."""

        client = self._client
        if client is None:
            return

        self._client = None

        client.disconnect()
        client.on_message = None

        # drain queue
        queue = self._queue
        while True:
            try:
                queue.get_nowait()
                queue.task_done()
            except Empty:
                break

    def __enter__(self: S) -> S:
        """Enter the connection."""

        self.connect()

        return self

    def __exit__(
        self,
        exc_type: Optional[Type[E]],
        exc_value: Optional[E],
        traceback: Optional[TracebackType],
    ) -> None:
        """Exit the connection."""

        self.disconnect()

    def _on_message(self, client: Client, userdata: Any, message: MQTTMessage) -> None:
        """Message handler."""

        topic, payload = message.topic, message.payload

        try:
            results = self._make_messages(topic, payload)
        except KeyboardInterrupt:
            raise
        except Exception:
            logger.exception("Unable to decode message", topic=topic)
            return

        queue = self._queue
        for result in results:
            try:
                queue.put_nowait(result)
                self._input_count += 1
            except Full:
                with queue.mutex:
                    if queue.full():
                        logger.warning("Queue full. Discarding oldest message", topic=topic)
                        queue.get_nowait()
                        queue.task_done()
                    queue.put_nowait(result)

    def send(self, message: Union[Message, Sequence[Message]]) -> None:
        """Send message."""

        client = self._client
        if client is None:
            return

        qos = self.config.qos

        messages = message if isinstance(message, Sequence) else [message]

        for message in messages:
            for topic, payload in self._make_payloads(message):
                client.publish(topic, payload, qos=qos)
                self._output_count += 1

    def receive(self, timeout: Optional[float] = None) -> Optional[Message]:
        """Receive message."""

        if self._client is None:
            return None

        try:
            message = self._queue.get(timeout=timeout)
        except Empty:
            return None
        else:
            self._queue.task_done()
            return message


A = TypeVar("A", bound="AsyncConnection", covariant=True)


class AsyncConnection(Connection):
    """Asynchronous Pub-Sub Connection."""

    _client: AsyncClient

    def __init__(self, config: PubSubClientConfig) -> None:
        """Initialise async connection."""

        super().__init__(config)

        config = self.config
        self._client = config.broker_url.get_async_client(
            config.client_id,
            config.username,
            config.password,
        )

    async def connect(self) -> None:
        """Connect."""

        client, config = self._client, self.config
        topics = config.topics

        await client.connect()
        await client.subscribe([(topic, config.qos) for topic in topics])

        topic_summary = "\n".join(f"  - {topic}" for topic in topics)
        logger.info(f"Subscribed to topics:\n{topic_summary}")

    async def disconnect(self) -> None:
        """Close connection."""

        await self._client.disconnect()

    async def __aenter__(self: A) -> A:
        """Enter the connection."""

        await self.connect()

        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[E]],
        exc_value: Optional[E],
        tb: Optional[TracebackType],
    ) -> None:
        """Exit the connection."""

        await self.disconnect()

    def send(self, message: Message) -> Task:
        """Send message."""

        client = self._client
        qos = self.config.qos
        payloads = self._make_payloads(message)

        async def task() -> None:
            await asyncio.gather(
                *(client.publish(topic, payload, qos=qos) for topic, payload in payloads)
            )
            self._output_count += len(payloads)

        # create task and return immediately
        return asyncio.create_task(task())

    async def stream(self) -> AsyncIterator[Message]:
        """Receive message."""

        async with self._client.unfiltered_messages() as messages:
            async for message in messages:
                topic, payload = message.topic, message.payload
                try:
                    results = self._make_messages(topic, payload)
                    for result in results:
                        self._input_count += 1
                        yield result
                except KeyboardInterrupt:
                    raise
                except Exception:
                    logger.exception("Unable to decode message", topic=topic)
