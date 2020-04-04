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
