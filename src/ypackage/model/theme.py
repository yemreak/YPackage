import logging
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, List

from ..core import filesystem
from . import common

logger = logging.getLogger(__name__)


class OptionParser(common.Base):

    def __init__(self):
        self.parser = ArgumentParser(
            description="VSCode temaları için renk çevirici"
        )

        self.parser.add_argument(
            "paths",
            nargs="+",
            metavar="paths",
            help="settings.json dosyasının yolları"
        )

        self.parser.add_argument(
            "--debug",
            "-d",
            action="store_true",
            dest="debug",
            help="Bilgilendirici metinleri gösterme"
        )

    def parse_args(self):
        return self.parser.parse_args()


class ThemeOptions(common.SubOptions):

    ATTRIBUTES = [
        "name",
        "colors"
    ]

    def __init__(self, name: str, colors: Dict[str, str]):
        self.name = name
        self.colors = colors


class ExtensionOptions(common.SubOptions):

    ATTRIBUTES = [
        "postname",
        "postfix",
        "options"
    ]

    def __init__(self, postname: str, postfix: str, options: Dict[str, str]):
        self.postname = postname
        self.postfix = postfix
        self.options = options


class ConfigOptions(common.ConfigOptions):

    ATTRIBUTES = [
        "coreTheme",
        "outputDir",
        "themes",
        "extensions"
    ]

    def __init__(
        self,
        coretheme_path: Path,
        outdir_path: Path,
        themes_options: List[ThemeOptions],
        extensions_options: List[ExtensionOptions]
    ):
        self.coretheme_path = coretheme_path
        self.outdir_path = outdir_path
        self.themes_options = themes_options
        self.extensions_options = extensions_options

    @classmethod
    def from_file(cls, filepath: Path):
        config = filesystem.read_jsonc(filepath)

        cls.assert_config(config)

        coretheme_path = Path(config[cls.ATTRIBUTES[0]])
        if not coretheme_path.is_absolute():
            coretheme_path = filepath.parent / coretheme_path

        outdir_path = Path(config[cls.ATTRIBUTES[1]])
        if not outdir_path.is_absolute():
            outdir_path = filepath.parent / outdir_path

        themes_options = []
        theme_modules = config[cls.ATTRIBUTES[2]]
        for theme_module in theme_modules:
            themes_options.append(
                ThemeOptions.from_module(theme_module)
            )

        extensions_options = []
        extension_modules = config[cls.ATTRIBUTES[3]]
        for extension_module in extension_modules:
            extensions_options.append(
                ExtensionOptions.from_module(extension_module)
            )

        return cls(
            coretheme_path,
            outdir_path,
            themes_options,
            extensions_options
        )


class TokenColor(common.SubOptions):

    ATTRIBUTES = [
        "name",
        "scope",
        "settings"
    ]

    def __init__(
        self,
        name: str,
        scope: List[str],
        settings: Dict[str, str]
    ):
        self.name = name if name else ""
        self.scope = scope
        self.settings = settings

    def to_dict(self) -> Dict[str, str]:
        return vars(self)


class Theme(common.ConfigOptions):

    ATTRIBUTES = [
        "name",
        "type",
        "author",
        "colors",
        "tokenColors"
    ]

    def __init__(
        self,
        name: str,
        _type: str,
        author: str,
        colors: Dict[str, str],
        token_colors: List[TokenColor]
    ):
        self.name = name
        self.type = _type
        self.author = author
        self.colors = colors
        self.token_colors = token_colors

    @classmethod
    def from_theme(cls, theme):
        return cls(
            theme.name,
            theme.type,
            theme.author,
            theme.colors,
            theme.token_colors
        )

    @classmethod
    def from_file(cls, filepath: Path):
        theme_settings = filesystem.read_jsonc(filepath)

        cls.assert_config(theme_settings)

        name = theme_settings[cls.ATTRIBUTES[0]]
        _type = theme_settings[cls.ATTRIBUTES[1]]
        author = theme_settings[cls.ATTRIBUTES[2]]
        colors = theme_settings[cls.ATTRIBUTES[3]]

        token_colors = []
        token_modules = theme_settings[cls.ATTRIBUTES[4]]
        for token_module in token_modules:
            token_colors.append(
                TokenColor.from_module(token_module)
            )

        return cls(
            name,
            _type,
            author,
            colors,
            token_colors
        )

    def to_dict(self) -> Dict[str, str]:
        json_data = {}
        for key, value in vars(self).items():
            if key == "token_colors":
                value = [vars(_value) for _value in value]
                key = "tokenColors"
            json_data[key] = value
        return json_data

    def write_to_file(self, filepath: Path) -> bool:
        return filesystem.write_json_to_file(filepath, self.to_dict())
