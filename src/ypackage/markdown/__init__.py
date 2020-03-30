
"""Markdown yönetim paketi
"""

from .core import (
    change_title_of_file, change_title_of_string, check_links,
    create_markdown_file, find_all_headers,
    find_all_headers_from_file, find_all_links,
    find_first_header, find_first_header_from_file,
    find_first_link, generate_custom_link_string,
    generate_dir_link_string, generate_file_link_string,
    generate_header_section, generate_name_for_file,
    generate_substrings, insert_to_file, is_url, map_links,
    replace_in_links
)
from .entity import Comment, Header, Indent, Link, SpecialFile

__all__ = [
    'Comment',
    'Indent',
    'Link',
    'Header',
    'SpecialFile',
    'insert_to_file',
    'create_markdown_file',
    'generate_substrings',
    'find_all_headers',
    'find_all_headers_from_file',
    'find_first_header',
    'find_first_header_from_file',
    'change_title_of_string',
    'change_title_of_file',
    'generate_header_section',
    'generate_name_for_file',
    'find_all_links',
    'find_first_link',
    'generate_custom_link_string',
    'generate_file_link_string',
    'generate_dir_link_string',
    'is_url',
    'check_links',
    'map_links',
    'replace_in_links',
    'replace_link'
]
