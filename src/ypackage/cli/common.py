import logging

import coloredlogs

logger = logging.getLogger(__name__)


def initialize_logging(level=logging.INFO):
    """Renkli raporlayıcı aktif eder

    Keyword Arguments:
        level {int} -- Raporlama seviyesi (default: {logging.INFO})
    """

    if level == logging.DEBUG:
        log_format = r"%(name)s[%(process)d] %(levelname)s %(message)s"
    else:
        log_format = r"%(levelname)s %(message)s"

    coloredlogs.install(fmt=log_format, level=level)
    logger.debug("Renkli raporlayıcı aktif edildi")
