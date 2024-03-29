from ...ypackage.core.common import update_string_by_stringindexes


def test_update_string_by_stringindexes():

    long_content = (
        "##  Harici Bağlantılar\n\n"
        "* [Python ~ YEmreAk]"
        "(https://python.yemreak.com)\n\n"
        "<!-- Autogenerated with YPackage Integration tool -->\n\n"
        "* [YEmreAk]"
        "(https://yemreak.com)\n\n"
        "<!-- Autogenerated with YPackage Integration tool -->\n"
    )

    long_sindex = '\n<!-- Autogenerated with YPackage Integration tool -->\n\n'
    long_eindex = '\n\n<!-- Autogenerated with YPackage Integration tool -->\n'

    long_result = (
        "##  Harici Bağlantılar\n\n"
        "* [Python ~ YEmreAk]"
        "(https://python.yemreak.com)\n\n"
        "<!-- Autogenerated with YPackage Integration tool -->\n\n"
        "YPackage\n\n<!-- Autogenerated with YPackage Integration tool -->\n"
    )

    result = update_string_by_stringindexes(
        'YPackage',
        long_content,
        long_sindex,
        long_eindex
    )

    assert result == long_result
