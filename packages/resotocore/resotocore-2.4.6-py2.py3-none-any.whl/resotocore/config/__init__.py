from __future__ import annotations

from abc import ABC, abstractmethod
from attrs import define
from typing import Optional, AsyncIterator, List

from jsons import set_deserializer, set_serializer

from resotocore.model.model import Model, Kind
from resotocore.types import Json
from resotocore.ids import ConfigId


@define(order=True, hash=True, frozen=True)
class ConfigEntity:
    id: ConfigId
    config: Json
    revision: Optional[str] = None

    # noinspection PyUnusedLocal
    @staticmethod
    def from_json(js: Json, _: type = object, **kwargs: object) -> ConfigEntity:
        if "id" in js and "config" in js:
            return ConfigEntity(js["id"], js["config"], js.get("_rev"))
        else:
            raise AttributeError(f"Can not parse a ConfigEntity from this json: {js}")

    # noinspection PyUnusedLocal
    @staticmethod
    def to_json(o: ConfigEntity, **kw_args: object) -> Json:
        return dict(id=o.id, config=o.config, _rev=o.revision)


@define(order=True, hash=True, frozen=True)
class ConfigValidation:
    id: str
    external_validation: bool = False


class ConfigHandler(ABC):
    @abstractmethod
    def list_config_ids(self) -> AsyncIterator[ConfigId]:
        pass

    @abstractmethod
    async def get_config(self, cfg_id: ConfigId) -> Optional[ConfigEntity]:
        pass

    @abstractmethod
    async def put_config(self, cfg: ConfigEntity, validate: bool = True) -> ConfigEntity:
        pass

    @abstractmethod
    async def patch_config(self, cfg: ConfigEntity) -> ConfigEntity:
        pass

    @abstractmethod
    async def delete_config(self, cfg_id: ConfigId) -> None:
        pass

    @abstractmethod
    async def get_configs_model(self) -> Model:
        pass

    @abstractmethod
    async def update_configs_model(self, kinds: List[Kind]) -> Model:
        pass

    @abstractmethod
    def list_config_validation_ids(self) -> AsyncIterator[str]:
        pass

    @abstractmethod
    async def get_config_validation(self, cfg_id: str) -> Optional[ConfigValidation]:
        pass

    @abstractmethod
    async def put_config_validation(self, validation: ConfigValidation) -> ConfigValidation:
        pass

    @abstractmethod
    async def config_yaml(self, cfg_id: ConfigId, revision: bool = False) -> Optional[str]:
        pass


# register serializer for this class
set_deserializer(ConfigEntity.from_json, ConfigEntity)
set_serializer(ConfigEntity.to_json, ConfigEntity)
