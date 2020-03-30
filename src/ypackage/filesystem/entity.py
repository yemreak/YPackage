from argparse import ArgumentParser
from pathlib import Path


class OptionParser(ArgumentParser):

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


class Options:

    def __init__(
        self,
        pattern: str,
        to: str,
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

    @classmethod
    def from_sytem_args(cls, path: Path):
        args = OptionParser().parse_args()

        recursive = args.recursive
        silent = args.silent
        dir_mode = args.dir_mode
        pattern = args.pattern
        to = args.to
        case_sensitive = args.case_sensitive
        debug = args.debug

        return cls(
            pattern,
            to,
            workdir=path,
            recursive=recursive,
            silent=silent,
            dir_mode=dir_mode,
            case_sensitive=case_sensitive,
            debug=debug
        )
