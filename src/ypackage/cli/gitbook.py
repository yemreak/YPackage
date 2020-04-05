import logging
from glob import glob
from pathlib import Path
from typing import List

from ..cli import common
from ..core import filesystem, github, markdown
from ..core.gitbook import (create_changelog, generate_description_section,
                            generate_readme_for_project,
                            generate_summary_for_project,
                            read_summary_from_url)
from ..model.gitbook import OptionParser, Options

logger = logging.getLogger(__name__)


def generate_readmes_by_options(options: Options):
    if options.generate:
        generate_readme_for_project(
            options.workdir,
            options.index,
            ignore=options.ignore,
            must_inserted=True
        )


def recreate_summary_by_options(options: Options):
    if options.recreate:
        generate_summary_for_project(
            options.workdir,
            options.index,
            ignore=options.ignore,
            must_inserted=True
        )


def fix_title_of_subsummary(content: str) -> str:
    link = markdown.find_first_link(content)
    if link:
        content = markdown.update_title_of_markdown(link.name, content)
    return content


def fix_links_of_subsummary(content: str, url: str) -> str:

    def fix_link(link: markdown.Link):
        if not link.is_url():
            link.path = url + "/" + link.path
            link.path = link.path.replace(".md", "").replace("README", "")

    content = markdown.map_links_in_string(content, fix_link)
    return content


def insert_description(description: str, content: str) -> str:
    return generate_description_section(description) + content


def update_sub_summaries_by_options(options: Options) -> str:
    changed_filepaths = []
    if options.update:
        for submodule in options.submodules:
            content = read_summary_from_url(submodule.url)

            substring = markdown.find_substrings_by_commentstring(
                content,
                options.index
            )
            if substring:
                content = substring[0]

            content = fix_title_of_subsummary(content)
            content = fix_links_of_subsummary(content, submodule.root)

            if submodule.description:
                content = insert_description(submodule.description, content)

            if submodule.until:
                content = content[: content.find(submodule.until)]

            filesystem.write_to_file(submodule.path, content)

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

    # TODO: Summary ve README gitbook.yml dosyası ile oluşturulsun
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
