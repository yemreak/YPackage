import logging
import shlex
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import List

from ..core import filesystem
from . import common

logger = logging.getLogger(__name__)


class IntegrationOptions(common.Base):

    ATTR_ARGS = "args"

    def __init__(self, name: str = "", args: list = []):
        self.name = name
        self.args = args

    @staticmethod
    def from_module(name: str, module: dict):
        return IntegrationOptions(
            name,
            shlex.split(module[IntegrationOptions.ATTR_ARGS])
        )


class SubmoduleOptions(common.Base):

    ATTR_DESCRIPTION = "description"
    ATTR_PATH = "path"
    ATTR_URL = "url"
    ATTR_ROOT = "root"
    ATTR_UNTIL = "until"

    def __init__(
        self,
        name: str,
        description: str,
        path: str,
        url: str,
        root: str,
        until: str
    ):
        self.name = name
        self.description = description
        self.path = path
        self.url = url
        self.root = root
        self.until = until

    @staticmethod
    def from_module(name: str, module: dict, root="."):
        path = root / module[SubmoduleOptions.ATTR_PATH]
        url = module[SubmoduleOptions.ATTR_URL]
        root = module[SubmoduleOptions.ATTR_ROOT]

        description = ""
        if SubmoduleOptions.ATTR_DESCRIPTION in module:
            description = module[SubmoduleOptions.ATTR_DESCRIPTION]

        until = ""
        if SubmoduleOptions.ATTR_UNTIL in module:
            until = module[SubmoduleOptions.ATTR_UNTIL]

        return SubmoduleOptions(
            name,
            description,
            path,
            url,
            root,
            until
        )


class ConfigOptions(common.Base):

    FILENAME = ".ygitbookintegration"

    ATTR_INTEGRATION = "integration"
    ATTR_SUBMODULE = "submodule"

    def __init__(
        self,
        workdir: Path,
        integration_options: IntegrationOptions,
        submodule_options: List[SubmoduleOptions]
    ):
        """Configuration file settings for GitBook Integration

        The configuration file name is `.ygitbookintegration`
        """

        self.workdir = workdir
        self.integration = integration_options
        self.submodules = submodule_options

    @property
    def filepath(self) -> Path:
        return self.workdir / ConfigOptions.FILENAME

    @staticmethod
    def from_workdir(workpath: Path):
        return ConfigOptions.from_file(workpath / ConfigOptions.FILENAME)

    @staticmethod
    def from_file(filepath: Path):
        workdir = filepath.parent

        config = filesystem.read_config(filepath)

        integration = IntegrationOptions()
        submodules = []

        for section in config.sections():
            module_type, module_name = shlex.split(section)
            module = config[section]

            if module_type == ConfigOptions.ATTR_INTEGRATION:
                integration = IntegrationOptions.from_module(
                    module_name,
                    module
                )

            elif module_type == ConfigOptions.ATTR_SUBMODULE:
                submodules.append(
                    SubmoduleOptions.from_module(
                        module_name,
                        module,
                        root=workdir
                    )
                )

        return ConfigOptions(workdir, integration, submodules)


class OptionParser(common.Base):

    def __init__(self):
        self.parser = ArgumentParser(
            description="Helpfully scripts helps to synchronize GitBook & GitHub"
        )
        self.parser.add_argument(
            "paths",
            nargs="+",
            metavar="paths",
            help="Path of GitHub repositories",
        )
        self.parser.add_argument(
            "--update",
            "-u",
            action="store_true",
            dest="update",
            help="Update submodules `README.md` with their original `SUMMARY.md` files",
        )
        self.parser.add_argument(
            "--recreate",
            "-r",
            action="store_true",
            dest="recreate",
            help="Create `SUMMARY.md` file even if exists",
        )
        self.parser.add_argument(
            "--generate",
            "-g",
            action="store_true",
            dest="generate",
            help="Insert link that target file path for non-markdown files to `README.md`",
        )
        self.parser.add_argument(
            "--changelog",
            "-c",
            action="store_true",
            dest="changelog",
            help="Create for `CHANGELOG.md` file for given GitHub repo url",
        )
        self.parser.add_argument(
            "--depth-limit",
            "-dl",
            default=-1,
            dest="depth_limit",
            help="The depth limit of any methods works `0` for only main folder",
            type=int
        )
        self.parser.add_argument(
            "--debug",
            "-d",
            action="store_true",
            dest="debug",
            help="Shows debug log",
        )
        self.parser.add_argument(
            "--store",
            "-s",
            action="store_true",
            dest="store",
            help="Save last arguments that is used to configuration `.ygitbookintegration` file",
        )
        self.parser.add_argument(
            "--push",
            "-p",
            action="store_true",
            dest="push",
            help="Push all commits to GitHub",
        )
        self.parser.add_argument(
            "--repo-url",
            "-ru",
            dest="repo_url",
            help="The url of relevant GitHub repo",
        )
        self.parser.add_argument(
            "--commit-msg",
            "-cm",
            dest="commit_msg",
            help="Commit message for push event",
        )
        self.parser.add_argument(
            "--ignore-commits",
            "-ic",
            nargs="+",
            metavar="ignore_commits",
            default=[],
            help="The commit title which won't be added to `CHANGELOG.md` file",
        )
        self.parser.add_argument(
            "--index",
            "-ix",
            dest="index",
            default="Auto generated with YPackage Integration tool",
            help="Generated links will be inserted between given indexes",
        )
        self.parser.add_argument(
            "--ignore",
            "-ig",
            nargs="+",
            metavar="ignore",
            default=[],
            help="List of folder and file names that will ignored",
        )
        self.parser.add_argument(
            "--footer-path",
            "-fp",
            dest="footer_path",
            help="Append to the given file by filepath to end of the output",
        )
        self.parser.add_argument(
            "--new-index",
            "-nix",
            dest="new_index",
            default="Autogenerated with YPackage Integration tool",
            help="Generated links will be inserted between given new indexes instead of old one"
        )

    def parse_args(self):
        return self.parser.parse_args()


class Options(common.Options):

    LOG_LOAD_CONFIG = "Yapılandırma dosyası"

    def __init__(
        self,
        workdir=Path(""),
        update=False,
        recreate=False,
        generate=False,
        changelog=False,
        depth_limit=-1,
        debug=False,
        store=False,
        push=False,
        repo_url="",
        commit_msg="",
        ignore_commits: List[str] = [],
        ignore: List[str] = [],
        index="",
        new_index="",
        footer_path="",
        submodules: List[SubmoduleOptions] = []
    ):
        """Options for GitBook Integration
        """

        self.workdir = workdir
        self.update = update
        self.recreate = recreate
        self.generate = generate
        self.changelog = changelog
        self.depth_limit = depth_limit
        self.debug = debug
        self.store = store
        self.push = push
        self.repo_url = repo_url
        self.commit_msg = commit_msg
        self.ignore_commits = ignore_commits
        self.ignore = ignore
        self.index = index
        self.new_index = new_index
        self.footer_path = footer_path

        self.submodules = submodules

    def load_integration_from_config(self, config: ConfigOptions):
        sys.argv = [__file__, str(self.workdir)] + config.integration.args
        return self.load_system_args(config.workdir)

    def load_submodules_from_config(self, config: ConfigOptions):
        self.submodules = config.submodules

    def load_workdir_from_config(self, config: ConfigOptions):
        self.workdir = config.workdir

    def load_config(self, config: ConfigOptions):
        self.load_workdir_from_config(config)
        self.load_submodules_from_config(config)
        self.load_integration_from_config(config)

        self.log_load(self.LOG_LOAD_CONFIG)

    def load_config_from_workdir(self, workdir: Path):
        config = ConfigOptions.from_workdir(workdir)
        return self.load_config(config)

    def load_config_from_file(self, filepath: Path):
        config = ConfigOptions.from_file(filepath)
        return self.load_config(config)

    def load_system_args(self, workdir: Path):
        args = OptionParser().parse_args()

        self.workdir = workdir
        self.update = args.update
        self.recreate = args.recreate
        self.generate = args.generate
        self.changelog = args.changelog
        self.depth_limit = args.depth_limit
        self.debug = args.debug
        self.store = args.store
        self.push = args.push
        self.repo_url = args.repo_url
        self.commit_msg = args.commit_msg
        self.ignore_commits = args.ignore_commits
        self.ignore = args.ignore
        self.index = args.index
        self.new_index = args.new_index
        self.footer_path = args.footer_path

        self.log_load(self.LOG_LOAD_SYSTEM_ARGS)

    @staticmethod
    def from_config(config: ConfigOptions):
        options = Options()
        options.load_config(config, True)
        return options

    @staticmethod
    def from_workdir(workdir: Path, use_system_args=False):
        options = Options()

        if use_system_args:
            options.load_system_args(workdir)
        else:
            options.load_config_from_workdir(workdir)

        return options
