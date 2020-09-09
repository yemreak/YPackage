import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class Base:

    def __str__(self):
        raise NotImplementedError

    def __repr__(self):
        return type(self).__name__ + "(" \
            + ', '.join([f"{key}={repr(value)}" for key, value in vars(self).items()]) \
            + ")"

    def __eq__(self, other):
        if type(self) != type(other):
            return False

        items = vars(self)
        for key, value in vars(other).items():
            if not items[key] == value:
                return False

        return True


class SubOptions(Base):

    ATTRIBUTES = []

    @classmethod
    def from_module(cls, module: dict):
        if not cls.ATTRIBUTES:
            raise NotImplementedError

        attributes = []
        for attr in cls.ATTRIBUTES:
            attributes.append(
                module[attr] if attr in module.keys() else None
            )
        return cls(*attributes)


class ConfigNotFoundError(FileNotFoundError):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ConfigOptions(Base):

    ATTRIBUTES = []

    def __getattribute__(self, name):
        return super().__getattribute__(name)

    @classmethod
    def from_file(cls, filepath: Path):
        raise NotImplementedError

    @classmethod
    def is_config(cls, config: dict) -> bool:
        return all([key in cls.ATTRIBUTES for key in config])

    @classmethod
    def assert_config(cls, config: dict):
        if not cls.is_config(config):
            raise ConfigNotFoundError


class Options(Base):

    LOG_LOAD_TEMPLATE = "{} ile komut çalıştırılıyor"
    LOG_LOAD_SYSTEM_ARGS = "Parametreler"

    def load_system_args(self, workdir: Path):
        raise NotImplementedError

    def log_load(self, load_type: str):
        message = self.LOG_LOAD_TEMPLATE.format(load_type)
        message += "\n"
        message += repr(self)

        logger.debug(message)

    @classmethod
    def from_system_args(cls, workdir: Path):
        raise NotImplementedError
