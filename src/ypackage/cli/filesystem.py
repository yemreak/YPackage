import logging
from glob import glob
from pathlib import Path

from ..core.filesystem import rename_files, rename_folders
from ..model.filesystem import OptionParser, Options
from . import common

logger = logging.getLogger(__name__)


def rename(options: Options):
    function = rename_folders if options.dir_mode else rename_files
    result = function(
        options.workdir,
        options.pattern,
        options.to,
        ignore_case=not options.case_sensitive,
        recursive=options.recursive
    )

    if not result:
        logger.warning(
            f"Değişiklik yapılmadı: {options.pattern=} {options.to=}"
        )


def main():
    args = OptionParser().parse_args()

    log_level = logging.DEBUG if args.debug else logging.INFO
    common.initialize_logging(level=log_level)

    for path in args.paths:
        paths = [Path(p) for p in glob(path)]
        for path in paths:
            if path.is_dir():
                options = Options.from_system_args(path)
                rename(options)
            else:
                logger.error(f"{path.name} is not valid path")


if __name__ == "__main__":
    main()
