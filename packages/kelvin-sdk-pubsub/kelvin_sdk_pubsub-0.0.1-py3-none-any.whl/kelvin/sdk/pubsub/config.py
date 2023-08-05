"""Kelvin Pub-Sub Client Configuration."""

from __future__ import annotations

from collections import defaultdict
from enum import IntEnum
from itertools import groupby, product
from pathlib import Path
from typing import (
    Any,
    Callable,
    Collection,
    DefaultDict,
    Dict,
    Iterator,
    List,
    Mapping,
    NamedTuple,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    cast,
)

import yaml
from pydantic import BaseConfig, BaseSettings, Field, ValidationError, root_validator, validator
from pydantic.main import ErrorWrapper, ModelField

from kelvin.icd import Model

from .types import DNSName, DottedName, Identifier, MQTTUrl
from .utils import deep_get

try:
    from functools import cached_property  # type: ignore
except ImportError:
    from cached_property import cached_property  # type: ignore

DEFAULT_MQTT_HOST = "kelvin-mqtt-broker.app"
WILDCARD = "+"
SELECTORS = [
    "node_names",
    "workload_names",
    "asset_names",
    "names",
]
IO_FIELDS = {
    "inputs": "sources",
    "outputs": "targets",
}


class Selector(NamedTuple):
    """Selector."""

    node_name: str
    workload_name: str
    asset_name: str
    name: str


class QOS(IntEnum):
    """Quality-of-Service."""

    AT_MOST_ONCE = 0
    AT_LEAST_ONCE = 1
    EXACTLY_ONCE = 2

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[[Any, ModelField, BaseConfig], Any]]:
        """Get pydantic validators."""

        yield cls.validate

    @classmethod
    def validate(cls, value: Any, field: ModelField, config: BaseConfig) -> int:
        """Validate data."""

        if isinstance(value, int):
            return cls(value)
        elif not isinstance(value, str):
            raise TypeError(f"Invalid value {value!r}") from None

        try:
            return cls.__members__[value.upper()]
        except KeyError:
            raise ValueError(f"Invalid value {value!r}") from None


class Metric(Model):
    """Metric info."""

    class Config(Model.Config):
        """Pydantic config."""

        keep_untouched = (cached_property,)

    @validator(*SELECTORS, pre=True, always=True)
    def validate_selectors(cls, value: Any) -> Any:
        """Validate selectors."""

        if isinstance(value, (str, bytes)):
            return value

        if not isinstance(value, Collection) or isinstance(value, Mapping):
            return value

        if not all(isinstance(x, str) for x in value):
            return value

        # wildcard
        if "" in value:
            return []

        return sorted(value)

    node_names: Set[DNSName] = Field(
        {*[]},
        title="Node Names",
        description="Node names.",
    )
    workload_names: Set[DNSName] = Field(
        {*[]},
        title="Workload Names",
        description="Workload names.",
    )
    asset_names: Set[DottedName] = Field(
        {*[]},
        title="Asset Names",
        description="Asset names.",
    )
    names: Set[DottedName] = Field(
        {*[]},
        title="Names",
        description="Names.",
    )

    def match(self, x: Mapping[str, str]) -> bool:
        """Check if mapping matches metric info."""

        return all(x.get(k) in v for k, v in self.__dict__.items() if k in SELECTORS)

    @cached_property
    def combinations(self) -> Set[Selector]:
        """Field combinations."""

        return {*product(*(sorted(getattr(self, field)) or [""] for field in SELECTORS))}


class IO(Model):
    """IO."""

    class Config(Model.Config):
        """Pydantic config."""

        keep_untouched = (cached_property,)

    name: Identifier = Field(
        ...,
        title="Name",
        description="Name.",
    )
    data_type: DottedName = Field(
        ...,
        title="Data Type",
        description="Data type.",
    )
    metrics: List[Metric] = Field(
        [{}],
        title="Metrics",
        description="Metrics.",
    )

    @cached_property
    def combinations(self) -> Set[Selector]:
        """Field combinations."""

        return {x for metric in self.metrics for x in metric.combinations}


class PubSubClientConfig(BaseSettings, Model):
    """Kelvin Pub-Sub Client Configuration."""

    class Config(BaseSettings.Config, Model.Config):
        """Pydantic configuration."""

        keep_untouched = (cached_property,)
        env_prefix = "KELVIN_PUBSUB_CLIENT__"

    broker_url: MQTTUrl = Field(
        f"mqtt://{DEFAULT_MQTT_HOST}",
        title="Kelvin Broker URI",
        description="Kelvin Broker URI. e.g. mqtt://localhost:1883",
    )
    client_id: Optional[str] = Field(
        None,
        title="Client ID",
        description="Client ID.",
    )
    username: Optional[str] = Field(
        None,
        title="Username",
        description="Broker username.",
    )
    password: Optional[str] = Field(
        None,
        title="Password",
        description="Broker password.",
    )
    sync: bool = Field(
        True,
        title="Default Connection",
        description="Default connection type: sync/async",
    )
    qos: QOS = Field(
        QOS.AT_MOST_ONCE,
        title="Quality of Service",
        description="Quality of service for message delivery.",
    )
    max_items: int = Field(
        1024,
        title="Max Items",
        description="Maximum number of items to hold in sync receive queue.",
        ge=0,
    )

    @root_validator(pre=True)
    def validate_app_config(cls, values: Dict[str, Any]) -> Any:
        """Validate app configuration field and fill missing client configuration."""

        root_config = values.get("app_config")
        if root_config is None:
            return values

        if isinstance(root_config, str):
            root_config = Path(root_config.strip()).expanduser().resolve()
            if not root_config.is_file():
                raise ValueError(f"Invalid app configuration file {str(root_config)}") from None

        if isinstance(root_config, Mapping):
            pass
        elif isinstance(root_config, Path):
            root_config = values["app_config"] = yaml.safe_load(root_config.read_text())
        else:
            raise ValueError(
                f"Invalid app configuration type {type(root_config).__name__!r}"
            ) from None

        environment_config = root_config.get("environment", {})

        for name in ["node_name", "workload_name"]:
            if name not in values and name in environment_config:
                values[name] = environment_config[name]

        app_type = root_config.get("app", {}).get("type")
        if app_type is None:
            raise ValueError("Missing app type") from None
        if not isinstance(app_type, str):
            raise TypeError(f"Invalid app type {type(app_type).__name__!r}") from None

        app_config = deep_get(root_config, f"app.{app_type}", {})

        if app_type == "kelvin":
            if "global" not in values and "global" in app_config:
                values["metric_defaults"] = app_config["global"] or {}

            for name in IO_FIELDS:
                if name not in values and name in app_config:
                    values[name] = [
                        {key: x[key] for key in ["name", "data_type", IO_FIELDS[name]] if key in x}
                        for x in app_config[name]
                    ]

        elif app_type == "bridge":
            inputs: List[Dict[str, Any]] = []
            outputs: List[Dict[str, Any]] = []

            def key(x: Mapping[str, Any]) -> Tuple[str, str, str]:
                return x["name"], x["data_type"], x.get("access", "RO")

            metric_groups = groupby(sorted(app_config.get("metrics_map", []), key=key), key=key)

            for (name, data_type, access), entries in metric_groups:
                item = {
                    "name": name,
                    "data_type": data_type,
                    "metrics": [{"asset_names": [x["asset_name"] for x in entries]}],
                }

                outputs += [item]
                if access == "RW":
                    inputs += [item]

            if "inputs" not in values and inputs:
                values["inputs"] = inputs
            if "outputs" not in values and outputs:
                values["outputs"] = outputs

        else:
            raise ValueError(f"Invalid app type {app_type!r}") from None

        if "broker_url" not in values and "mqtt" in app_config:
            mqtt_config = app_config["mqtt"]
            ip = mqtt_config.get("ip")
            if ip is not None:
                port = mqtt_config.get("port")
                if "://" in ip:
                    transport, _, host = ip.partition("://")
                    if transport == "tcp":
                        scheme = "mqtt"
                    elif transport == "ssl":
                        scheme = "mqtts"
                    else:
                        raise ValueError(f"Unsupported transport {transport!r}") from None
                else:
                    host = ip
                    scheme = "mqtt"

                broker_url = f"{scheme}://{host}"
                if port:
                    broker_url = f"{broker_url}:{port}"

                values["broker_url"] = broker_url

            credentials = deep_get(mqtt_config, "authentication.credentials", {})
            if credentials:
                values["username"] = credentials.get("username")
                values["password"] = credentials.get("password")

        return values

    app_config: Optional[Dict[str, Any]] = Field(
        None,
        title="Application Configuration",
        description="Application configuration.",
    )

    node_name: DNSName = Field(
        ...,
        title="ACP Name",
        description="ACP name.",
    )
    workload_name: DNSName = Field(
        ...,
        title="Workload Name",
        description="Workload name.",
    )
    asset_name: Optional[DottedName] = Field(
        None,
        title="Asset Name",
        description="Asset name.",
    )
    metric_defaults: Metric = Field(
        {},
        title="Metric Defaults",
        description="Metric defaults.",
    )

    @validator(*IO_FIELDS, pre=True, always=True)
    def validate_io(cls, value: Any, values: Dict[str, Any], field: ModelField) -> Any:
        """Validate IO."""

        if not value and field.name in values:
            value = values.pop(field.name)

        if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
            return value

        names: Set[str] = {
            item.get("name", "")
            for field_name in IO_FIELDS
            if field_name != field.name and isinstance(values.get(field_name), list)
            for item in values[field_name]
            if isinstance(item, Mapping)
        }
        errors: List[ErrorWrapper] = []

        metric_defaults = values.get("metric_defaults")

        value = [*value]
        for i, x in enumerate(value):
            if not isinstance(x, Mapping):
                continue

            name = x.get("name")
            if not isinstance(name, str):
                continue

            if name not in names:
                names |= {name}
            else:
                errors += [ErrorWrapper(ValueError(f"Name {name!r} must be unique"), loc=(i,))]

            metrics = x.get("metrics", ...)
            if metrics is ...:
                field_name = IO_FIELDS[field.name]
                if field_name in x:
                    x = value[i] = {**x}
                    metrics = x["metrics"] = x.pop(field_name)
                else:
                    metrics = None

            # apply defaults
            if metric_defaults is not None:
                if not metrics:
                    metrics = [{}]
                x["metrics"] = [{**metric_defaults, **metric} for metric in metrics]

            if not metrics and field.name == "inputs":
                errors += [
                    ErrorWrapper(ValueError("Input must have at least one metric"), loc=(i,))
                ]

        if errors:
            raise ValidationError(errors, model=cast(Type[PubSubClientConfig], cls)) from None

        return value

    inputs: List[IO] = Field(
        [],
        title="Inputs",
        description="Message inputs.",
    )
    outputs: List[IO] = Field(
        [],
        title="Outputs",
        description="Message outputs.",
    )

    @cached_property
    def input_map(self) -> Dict[Selector, List[Tuple[str, str]]]:
        """Input map."""

        result: DefaultDict[Selector, Set[Tuple[str, str]]] = defaultdict(set)

        for io in self.inputs:
            for key_ in io.combinations:
                node_name, workload_name, asset_name, name = key_
                key = Selector(
                    node_name or self.node_name,
                    workload_name,
                    asset_name or self.asset_name or "",
                    name or io.name,
                )
                result[key] |= {(io.name, io.data_type)}

        return {k: sorted(v) for k, v in result.items()}

    @cached_property
    def output_map(self) -> Dict[Selector, List[Tuple[str, str]]]:
        """Output map."""

        result: DefaultDict[Selector, Set[Tuple[str, str]]] = defaultdict(set)

        for io in self.outputs:
            for key_ in io.combinations:
                node_name, workload_name, asset_name, name = key_
                key = Selector(
                    node_name or self.node_name,
                    workload_name or self.workload_name,
                    asset_name or self.asset_name or "",
                    io.name,
                )
                result[key] |= {(name or io.name, io.data_type)}

        return {k: sorted(v) for k, v in result.items()}

    @cached_property
    def topics(self) -> List[str]:
        """Topics."""

        source = (self.node_name, self.workload_name)

        def topic(x: Tuple[str, ...]) -> str:
            node_name, workload_name, asset_name, name, *_ = x
            topic_type = "input" if (node_name, workload_name) == source else "output"

            return f"{topic_type}/{'/'.join(v or WILDCARD for v in x)}"

        return [topic(x) for x in self.input_map]

    def __iter__(self) -> Iterator[str]:  # type: ignore
        """Key iterator."""

        return iter(self.__dict__)
