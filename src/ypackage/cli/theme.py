import logging
from pathlib import Path

from ..core.theme import (generate_coretheme, generate_themes,
                          generate_themes_with_extensions)
from ..model.theme import ConfigOptions, OptionParser
from . import common

logger = logging.getLogger(__name__)


def create_theme(config_options: ConfigOptions):
    generate_coretheme(config_options)
    generate_themes(config_options)
    generate_themes_with_extensions(config_options)


def main():
    args = OptionParser().parse_args()

    level = logging.DEBUG if args.debug else logging.INFO
    common.initialize_logging(level=level)

    for path in args.paths:
        filepath = Path(path)

        if not filepath.is_file():
            logger.exception("Dosya yolu geçersiz: {path}")
            continue

        config_options = ConfigOptions.from_file(filepath)
        create_theme(config_options)
