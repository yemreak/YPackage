# 👨‍💻 Contributing Guide

* [👨‍🔬 PyTest](https://docs.pytest.org/en/latest/goodpractices.html#choosing-a-test-layout-import-rules)

## 👨‍💻 Kodlama Kurallarım

### 🏗️ Fonksiyon İsim Kalıplarım

| Metot Taslağı | Açıklama |
|-|-|
| `generate_<object_type>` | |
| `generate_<filetype>_for_<dir - project>` | Özel bir yer için dosya üretme |
| `generate_<something>_for_<something>` | Bir şey için bir şey üretme |
| `generate_<filter>_<object_type>_string` | Kısıtlanmış obje metni üretme|
| `generate_<filetype>_filelist_for_<dir - project>` | |
| `generate_<filetype>_<section>_section` | |
| `<filetype>_path_for_<dir - project>` | |
| `is_<something>` | Tip sorgulama |
| `has_<filetype>_file` | Dosya sahipliği kontrolü |
| `create_<filetype>_file` | Dosya oluşturma|
| `create_<filetype>_file_for_<dir - project>` | Özel bir yer için dosya oluşturma |
| `make_<object_type>_string` | Metin yapma |
| `<operation>_<to - from>_<somewhere>` | |
| `<change_operation>__<something>` | |
| `<search_operation>_<something>_from_<somewhere>` | |
| `change_<section>_<of>_<something>` | |
| `list_<filter>_<object_type>` | |

| Değişken | Açıklama |
|-|-|
| filetype | summary, readme |
| section | header, footer, description, title |
| filter | nonmarkdown, markdown, summary |
| object_type | filelink, dirlink, filelist, index, substring, file |
| operation | insert, write, read, copy |
| search_operation | find, find_all, find_first |
| change_operation | encode, decode |
| somewhere | file, content, string |
| something | link, header, file, name, markdown, readme, changelog |