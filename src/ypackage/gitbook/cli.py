import logging
from glob import glob
from pathlib import Path
from typing import List

from .. import common, github, markdown
from .core import (create_changelog, generate_description_section,
                   generate_readme_for_project, generate_summary_for_project,
                   read_summary_from_url)
from .entity import OptionParser, Options

logger = logging.getLogger(__name__)


def generate_readmes_by_options(options: Options):
    if options.generate:
        generate_readme_for_project(
            options.workdir,
            options.index,
            ignored_folders=options.ignored_folders,
            must_inserted=True
        )


def recreate_summary_by_options(options: Options):
    if options.recreate:
        generate_summary_for_project(
            options.workdir,
            options.index,
            ignored_folders=options.ignored_folders,
            must_inserted=True
        )


def fix_title_of_subsummary(content: str) -> str:
    title = f"# {markdown.find_first_link(content).name}"
    content = markdown.change_title_of_string(title, content)
    return content


def fix_links_of_subsummary(content: str) -> str:

    def fix_link(link: markdown.Link) -> markdown.Link:
        if not markdown.is_url(link.path):
            link.path = link.path.replace(".md", "").replace("README", "")
            return link

    content = markdown.map_links(content, fix_link)
    return content


def insert_description(description: str, content: str) -> str:
    return generate_description_section(description) + content


def update_sub_summaries_by_options(options: Options) -> str:
    changed_filepaths = []
    if options.update:
        for submodule in options.submodules:
            content = read_summary_from_url(submodule.url)

            substring = markdown.generate_substrings(content, options.index)
            if substring:
                content = substring[0]

            content = fix_title_of_subsummary(content)
            content = fix_links_of_subsummary(content)

            if submodule.description:
                content = insert_description(submodule.description, content)

            if submodule.until:
                content = content[: content.find(submodule.until)]

            changed_filepaths.append(submodule.path)

    return changed_filepaths


def push_changed_files_to_github_by_options(changed_filepaths: List[Path], options: Options):
    if options.push:
        return github.push_to_github(options.workdir, changed_filepaths, options.commit_msg)


def create_changelog_by_options(options: Options):
    if options.changelog:
        return create_changelog(
            options.workdir,
            repo_url=options.repo_url,
            push=options.push,
            ignore_commits=options.ignore_commits,
            commit_msg=options.commit_msg
        )


def integrate(options: Options):
    logger.info(f"Entegrasyon başlatıldı: {options.workdir.absolute()}")

    generate_readmes_by_options(options)
    recreate_summary_by_options(options)

    changed_filepaths = update_sub_summaries_by_options(options)
    push_changed_files_to_github_by_options(changed_filepaths, options)

    create_changelog_by_options(options)

    logger.info(f"Entegrasyon tamamlandı: {options.workdir.absolute()}")


def main():
    args = OptionParser().parse_args()

    use_system_args = any([
        args.generate,
        args.recreate,
        args.update,
        args.changelog
    ])

    log_level = logging.DEBUG if args.debug else logging.INFO
    common.initialize_logging(level=log_level)

    for path in args.paths:
        paths = [Path(p) for p in glob(path)]
        for path in paths:
            if path.is_dir():
                options = Options.from_workdir(path, use_system_args)
                integrate(options)
            else:
                logger.error(f"Geçerli bir yol değil: {path.name}")


if __name__ == "__main__":
    main()
