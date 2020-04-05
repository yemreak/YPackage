import re
from pathlib import Path
from typing import List, Tuple, Union

from ..model.theme import ConfigOptions, ExtensionOptions, Theme, ThemeOptions
from . import filesystem


def generate_filename_from_themename(themename: str, postfix="") -> str:
    """Tema isminden dosya adı üretir

    Arguments:
        themename {str} -- Tema ismi

    Keyword Arguments:
        postfix {str} -- Tema son eki (default: {""})

    Returns:
        str -- Dosya adı

    Examles:
        >>> generate_filename_from_themename('DarkCode Theme')
        'darkcode-theme.json'
        >>> generate_filename_from_themename('DarkCode Theme', '-plus-plus')
        'darkcode-theme-plus-plus.json'
    """
    return themename.replace(" ", "-").lower() + postfix + ".json"


def generate_coretheme(config: ConfigOptions):
    """Çekirdek temayı tema dizinine kopyalar

    Arguments:
        config {ConfigOptions} -- Yapılandırma ayarları

    Returns:
        [AnyPath] -- Kopyalama sonucu
    """
    return filesystem.copy_file(
        config.coretheme_path,
        config.outdir_path / config.coretheme_path.name
    )


def generate_theme_from_theme(
    basetheme: Theme,
    theme_options: ThemeOptions,
    outdirpath: Path,
    additional: Tuple[Theme, Path] = ()
) -> Tuple[Theme, Path]:
    """Tema üretir ve dosyaya yazar

    Arguments:
        corethemepath {Path} -- Üretim yapılacak çekirdek temanın yolu
        theme_options {ThemeOptions} -- Tema ayarları
        outdirpath {Path} -- Temaların çıktı dizini

    Keyword Arguments:
        additional {Tuple[Theme, Path]} -- Ek tema ve çıktı yolu (default: {None})

    Returns:
        Tuple[Theme, Path] -- Oluşturulan tema ve onun yolu
    """
    newtheme = Theme.from_theme(basetheme)
    for corekey, corevalue in newtheme.colors.items():
        for oldcolor, newcolor in theme_options.colors.items():
            if oldcolor.lower() in corevalue.lower():
                newtheme.colors[corekey] = re.sub(
                    oldcolor,
                    newcolor,
                    corevalue,
                    flags=re.IGNORECASE
                )

    if not additional:
        newtheme.name = theme_options.name
        newtheme_filename = generate_filename_from_themename(theme_options.name)
        newthemepath = outdirpath / newtheme_filename
    else:
        newtheme.name = re.sub(
            additional[0].name,
            theme_options.name,
            newtheme.name
        )
        newthemepath = Path(
            str(additional[1]).replace(
                additional[0].name.lower(),
                theme_options.name.lower()
            ).replace(" ", "-")
        )

    newtheme.write_to_file(newthemepath)
    return newtheme, newthemepath


def generate_theme(
    corethemepath: Path,
    theme_options: ThemeOptions,
    outdirpath: Path,
    additional: Tuple[Theme, Path] = ()
) -> Tuple[Theme, Path]:
    """Tema üretir ve dosyaya yazar

    Arguments:
        corethemepath {Path} -- Üretim yapılacak çekirdek temanın yolu
        theme_options {ThemeOptions} -- Tema ayarları
        outdirpath {Path} -- Temaların çıktı dizini

    Keyword Arguments:
        additional {Tuple[Theme, Path]} -- Ek tema ve çıktı yolu (default: {None})

    Returns:
        Tuple[Theme, Path] -- Oluşturulan tema ve onun yolu
    """
    coretheme = Theme.from_file(corethemepath)
    return generate_theme_from_theme(
        coretheme,
        theme_options,
        outdirpath,
        additional=additional
    )


def generate_themes(config: ConfigOptions) -> List[Tuple[Theme, Path]]:
    """Temeları üretir ve dosyaya yazar

    Arguments:
        config {ConfigOptions} -- Temaların üretilmesi için yapılandırma ayarları

    Returns:
        List[Tuple[Theme, Path]] -- Oluşturulan tüm temalar ve onların yolları
    """
    themes_with_paths = []
    for theme_options in config.themes_options:
        themes_with_paths.append(
            generate_theme(
                config.coretheme_path,
                theme_options,
                config.outdir_path,
            )
        )
    return themes_with_paths


def generate_extension(
    corethemepath: Path,
    extension_options: ExtensionOptions,
    outdirpath: Path
) -> Tuple[Theme, Path]:
    """Temayı geliştirir ve yeni dosyaya yazar

    Arguments:
        corethemepath {Path} -- Üretim yapılacak çekirdek temanın yolu
        extension_options {ThemeOptions} -- Geliştirme ayarları
        outdirpath {Path} -- Temaların çıktı dizini

    Returns:
        Tuple[Theme, Path] -- Oluşturulan tema ve onun yolu
    """
    extendedtheme = Theme.from_file(corethemepath)
    for optionkey, optionvalue in extension_options.options.items():
        extendedtheme.colors[optionkey] = optionvalue

    extendedtheme_filename = generate_filename_from_themename(
        extendedtheme.name,
        postfix=extension_options.postfix
    )
    extendedtheme.name += extension_options.postname
    extendedthemepath = outdirpath / extendedtheme_filename

    extendedtheme.write_to_file(extendedthemepath)
    return extendedtheme, extendedthemepath


def generate_themes_with_extensions(config: ConfigOptions):
    """Temeları geliştirir ve dosyaya yazar

    Arguments:
        config {ConfigOptions} -- Temaların geliştirilmesi için yapılandırma ayarları

    Returns:
        List[Tuple[Theme, Path]] -- Oluşturulan tüm temalar ve onların yolları
    """
    themes_with_paths = []
    for extensions_option in config.extensions_options:
        extendedtheme, extendedthemepath = generate_extension(
            config.coretheme_path,
            extensions_option,
            config.outdir_path
        )

        for theme_options in config.themes_options:
            themes_with_paths.append(
                generate_theme_from_theme(
                    extendedtheme,
                    theme_options,
                    config.outdir_path,
                    additional=(
                        Theme.from_file(config.coretheme_path),
                        extendedthemepath
                    )
                )
            )
    return themes_with_paths
