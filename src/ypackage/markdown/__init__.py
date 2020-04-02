"""Markdown yönetim paketi
"""
from .core import (change_title_of_file, change_title_of_string,
                   changelog_path_for_dir, check_links,
                   code_of_conduct_path_for_dir, contributing_path_for_dir,
                   create_markdown_file, encode_filepath, find_all_headers,
                   find_all_headers_from_file, find_all_links,
                   find_first_header, find_first_header_from_file,
                   find_first_link, generate_dirlink_string,
                   generate_filelink_string, generate_header_section,
                   generate_link_string, generate_name_for_file,
                   generate_substrings, has_changelog_file,
                   has_code_of_conduct_file, has_contributing_file,
                   has_license_file, has_readme_file, insert_to_file,
                   is_markdown, is_readme, is_url, license_path_for_dir,
                   list_markdown_files, list_nonmarkdown_files, map_links,
                   readme_path_for_dir, replace_in_links)
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
    'generate_link_string',
    'generate_filelink_string',
    'generate_dirlink_string',
    'is_url',
    'check_links',
    'map_links',
    'replace_in_links',
    'replace_link',
    'list_nonmarkdown_files',
    'encode_filepath',
    'readme_path_for_dir',
    'changelog_path_for_dir',
    'license_path_for_dir',
    'code_of_conduct_path_for_dir',
    'contributing_path_for_dir',
    'has_readme_file',
    'has_changelog_file',
    'has_code_of_conduct_file',
    'has_contributing_file',
    'has_license_file',
    'is_markdown',
    'list_markdown_files',
    'is_readme'
]
