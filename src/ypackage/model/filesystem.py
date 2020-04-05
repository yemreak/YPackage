from argparse import ArgumentParser
from pathlib import Path

from . import common


class OptionParser:

    def __init__(self):
        self.parser = ArgumentParser(
            description="Dosya veya dizinleri topluca adlandırma aracı"
        )
        self.parser.add_argument(
            'paths',
            nargs="+",
            metavar='paths',
            help='Dizin yolları',
        )
        self.parser.add_argument(
            "--recursive",
            "-r",
            action="store_true",
            dest="recursive",
            help="Dizin içerisindeki tüm içerikleri ele alır"
        )
        self.parser.add_argument(
            "--silent",
            "-s",
            action="store_true",
            dest="silent",
            help="İşlemleri çıktı göstermeden tamamlar"
        )
        self.parser.add_argument(
            "--dir-mode",
            "-dm",
            action="store_true",
            dest="dir_mode",
            help="Dosya yerine dizinlerin adlarını değiştirir"
        )
        self.parser.add_argument(
            "--pattern",
            "-p",
            dest="pattern",
            help="Değiştirilecek isimleri belirten regex şablonu",
            required=True
        )
        self.parser.add_argument(
            "--to",
            "-t",
            dest="to",
            help="Şablona uygun isimleri verilen değer ile değiştirir",
            required=True
        )
        self.parser.add_argument(
            "--case-sensitive",
            "-cs",
            action="store_true",
            dest="case_sensitive",
            help="Büyük küçük harf duyarlılığını aktif eder"
        )
        self.parser.add_argument(
            "--debug",
            "-d",
            action="store_true",
            dest="debug",
            help="Debug çıktılarını aktif eder",
        )

    def parse_args(self):
        return self.parser.parse_args()


class Options(common.Options):

    def __init__(
        self,
        pattern: str = "",
        to: str = "",
        workdir=Path('.'),
        recursive=False,
        silent=False,
        dir_mode=False,
        case_sensitive=False,
        debug=False
    ):
        self.workdir = workdir
        self.recursive = recursive
        self.silent = silent
        self.dir_mode = dir_mode
        self.pattern = pattern
        self.to = to
        self.case_sensitive = case_sensitive
        self.debug = debug

    def __repr__(self):
        return f"Options(" + \
            "workdir=" + repr(self.workdir) + \
            "recursive=" + repr(self.recursive) + \
            "silent=" + repr(self.silent) + \
            "dir_mode=" + repr(self.dir_mode) + \
            "pattern=" + repr(self.pattern) + \
            "to=" + repr(self.to) + \
            "case_sensitive=" + repr(self.case_sensitive) + \
            "debug=" + repr(self.debug) + \
            ")"

    def load_system_args(self, workdir: Path):
        args = OptionParser().parse_args()

        self.recursive = args.recursive
        self.silent = args.silent
        self.dir_mode = args.dir_mode
        self.pattern = args.pattern
        self.to = args.to
        self.case_sensitive = args.case_sensitive
        self.debug = args.debug

        self.log_load(self.LOG_LOAD_SYSTEM_ARGS)

    @classmethod
    def from_system_args(cls, workdir: Path):
        options = cls()
        options.load_system_args(workdir)
        return options
