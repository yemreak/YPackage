import logging
import re
from argparse import ArgumentParser
from copy import deepcopy
from pathlib import Path

from ..lib.common import initialize_logging
from ..lib.filesystem import copy_file, read_jsonc, write_json

logger = logging.getLogger(__name__)


def initialize_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description="VSCode temaları için renk çevirici"
    )

    parser.add_argument(
        "paths",
        nargs="+",
        metavar="paths",
        help="settings.json dosyasının yolları"
    )

    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        dest="debug",
        help="Bilgilendirici metinleri gösterme"
    )

    return parser


def generate_path_from_name(theme_name: str, postfix: str = "") -> str:
    return theme_name.replace(" ", "-").lower() + postfix + ".json"


def generate_theme(coretheme: dict, theme_settings: dict, outdir: Path, coretheme_info=()):
    # Copy core theme to remove referance
    new_theme = deepcopy(coretheme)

    # Replace colors with new ones
    for core_key, core_value in new_theme['colors'].items():
        for old_color, new_color in theme_settings['colors'].items():

            # Replace with new color if old color exists
            if old_color.lower() in core_value.lower():
                new_theme['colors'][core_key] = re.sub(
                    old_color,
                    new_color,
                    core_value,
                    flags=re.IGNORECASE
                )

    if not coretheme_info:
        # Refresh new theme name
        new_theme['name'] = theme_settings['name']

        # Generate path for new theme
        new_theme_filename = generate_path_from_name(theme_settings['name'])
        new_theme_path = outdir / new_theme_filename
    else:
        # Refresh new extension theme name
        new_theme['name'] = re.sub(
            coretheme_info[0],
            theme_settings['name'],
            new_theme['name']
        )

        new_theme_path = Path(
            str(coretheme_info[1]).replace(
                coretheme_info[0].lower(),
                theme_settings['name'].lower()
            ).replace(" ", "-")
        )

    # Write theme to file
    write_json(new_theme_path, new_theme)

    return new_theme, new_theme_path


def generate_extension(coretheme: dict, extension_setting: dict, outdir: Path):
    # Copy new theme to extend
    ext_theme = deepcopy(coretheme)

    # Insert or replace new options
    for option_key, option_value in extension_setting['options'].items():
        ext_theme['colors'][option_key] = option_value

    # Refresh extension name
    ext_theme['name'] = coretheme['name'] + extension_setting['postname']

    # Generate path for extension
    ext_theme_filename = generate_path_from_name(
        coretheme['name'], postfix=extension_setting['postfix']
    )
    ext_theme_path = outdir / ext_theme_filename

    # Write extension to file
    write_json(ext_theme_path, ext_theme)

    return ext_theme, ext_theme_path


def main():
    args = initialize_parser().parse_args()

    # Gettings args
    PATHS, DEBUG = args.paths, args.debug

    initialize_logging(detailed=DEBUG)

    for path in PATHS:
        path = Path(path)
        if not path.is_file():
            logger.error(f"{path} dosya yolu geçersiz")
            exit(-1)

        # Load settings
        settings = read_jsonc(path)

        if not all(
            key in ["coreTheme", "outputDir", "themes", "extensions"]
            for key in settings
        ):
            logger.error(f"{path} geçerli bir ayar dosyası değil")
            exit(-1)

        # Store necesssary path setttings
        coretheme_path = path.parent / Path(settings['coreTheme'])
        outdir_path = path.parent / Path(settings['outputDir'])

        # Store necesssary convertion setttings
        themes_settings = settings['themes']
        extension_settings = settings['extensions']

        # Copy core theme to outdir
        copy_file(coretheme_path, outdir_path / coretheme_path.name)

        # Load core theme setttings
        coretheme = read_jsonc(coretheme_path)

        # Generate new themes
        for theme_settings in themes_settings:
            generate_theme(coretheme, theme_settings, outdir_path)

        # Generate extensions
        for extension_setting in extension_settings:
            ext_theme, ext_theme_path = generate_extension(
                coretheme, extension_setting, outdir_path
            )

            # Generate new themes from extensions
            for theme_settings in themes_settings:
                generate_theme(
                    ext_theme, theme_settings,
                    outdir_path, coretheme_info=(coretheme['name'], ext_theme_path)
                )

            # Delete copied theme to avoid memory leak
            del ext_theme


if __name__ == "__main__":
    main()
