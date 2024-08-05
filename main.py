# Pygit++ official source code
# see DOCS
# version 0.0.01

# TODO: Well right now the following commands will be implemented:
#   - -s, --show (Display full information of the git repository)
#   - -p, --push (A better way to push code into github)
#   - redo the --init flag
#       - TODO: We need to complete the other mini app
#       - that will display the current hierarchy that
#       - will be used for the user to select the files
#       - that they want to add to their .gitignore file
#
# WARN: Known bugs/problems:
#   -   (0)
#
# NOTE: see 'DOCS/roadmap.md'

from utils.debug import debug
from utils.debug import print_cf
from utils.tools import yes_or_no_menu
from utils.tools import multiple_selection_menu
from utils.tools import multiple_choice_menu
from utils.tools import miniCommitTypingApp
import argparse
import os
import sys
from git import Repo
import git
import asyncio


class Pygit:
    """
    Section: Setup of
    argparser plus its configuration
    """

    def __init__(self):
        self.path = os.getcwd()
        self.setup_arg_parser()
        self.handle_args()

    def setup_arg_parser(self) -> None:
        """
        Setting up argparser with all the
        commands that pygit++ support
        """

        self.parser = argparse.ArgumentParser(
            prog="PYGIT++",
            description="The tool to work better with git",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
    version 0.0.01
    please run 'pygit++ -man' to see the user manual"""
        )

        self.parser.add_argument(
            '-i',
            action='store_true',
            help='Starts a empty repo in the current direcory')

        self.parser.add_argument(
            '--init',
            action='store_true',
            help='Set up the current directory to be a git repo')

        self.parser.add_argument(
            '-c', '--commit',
            metavar='<commit msg>',
            nargs='*',
            help='A better way to commit your work')

        self.parser.add_argument(
            '-a', '--add',
            metavar='<file> <files>',
            nargs='*',
            help='A better way to add your work'
        )
        self.parser.add_argument(
            '-m', '-man',
            action='store_true',
            help="Displays the user manual"
        )

        self.args = self.parser.parse_args()

    def handle_args(self) -> None:
        """
        Check for flags are on
        """
        if self.args.i:
            self.create_empty_repo(self.path)

        if self.args.init:
            self.setup_current_work_dic(self.path)

        self.repo = self.create_repo_object(self.path)

        if self.args.commit is not None:
            self.commit_work(self.repo, self.args.commit)
            sys.exit()

        if self.args.add is not None:
            self.add_files_to_index(self.repo, self.args.add)
            sys.exit()

        if self.args.m:
            self.display_manual()

        else:
            self.show_info_from_repo(self.repo)
            sys.exit(0)
    """
    End of section:
    Argparser
    """

    """
    Section: init pygit++
    """

    def create_repo_object(self, path: str) -> Repo:
        """
        Creates the repo object
        """

        try:
            repo = Repo(path, search_parent_directories=True)
            if repo.bare:
                debug("Bare repository was found", "E")
            return repo

        except git.exc.InvalidGitRepositoryError:
            debug("No valid git repository could be found", "E")
            sys.exit()

    def create_empty_repo(self, path: str) -> None:
        """
        Main function

        handler for the -i flag
        """
        command = f"git -C {path} init"
        preffix = ">/dev/null"

        if os.system(command + preffix) == 0:
            debug("Repository created successfully!", "M")

        else:
            debug("Repository couldn't be created", "E")
        sys.exit(1)

    def setup_current_work_dic(self, path: str) -> None:
        """
        Main function:

        Handler for the '--init' flag
        """
        path_conf = "~/.pygitconf"

        # path = os.getcwd()
        # self.start_repo(path)

        debug("Setting up this repo based on your configuration...", "I")
        try:
            with open(path_conf, 'r') as file:
                data = file.readall()
                print(data)
                file.close()

        except FileNotFoundError:
            print()
            debug("Configuration file couln't be found", "W")
            debug("Run 'pygit++ --setup' to configure it", "I")
            sys.exit(1)

    def create_dot_gitignore(self, path: str):
        """
        Sub-function of 'setup_current_work_dict'
        """

        raise NotADirectoryError

    """
    End Section:
    init pygit++
    """

    """
    Section:
    Manual
    """

    def display_manual(self) -> None:
        path = "~/python/projects/pygit/DOCS/man/man.md"
        url = "https://github.com/thelibertti/pygit-/tree/main/DOCS/man/man.md"

        os.system(f"bat {path}")

        print_cf("Remember that the user manual is also aviable at:", "C")
        print_cf(url, 'C')

    """
    End Section:
    Manual
    """

    """
    Section:
    Diplay Information from current repo
    """

    def show_info_from_repo(self, repo: Repo) -> None:
        """
        Main funtion
        """
        try:
            last_commit = repo.head.commit
            commit_info = {
                "commit_id": last_commit.hexsha,
                "commit_abbr": repo.git.rev_parse(last_commit.hexsha,
                                                  short=7),
                "commit_message": last_commit.message.strip(),
                "committed_files": list(last_commit.stats.files.keys())
            }

            self.display_basic_repo_info(repo)
            self.display_commit_info(commit_info)

        except ValueError:
            debug("NOT ENOUGH INFORMATION ABOUT THIS REPO", "W")
            debug("TRY ADDING SOME FILES FIRST OR DOING YOUR FIRST COMMIT!!",
                  "I")
            sys.exit(1)

    def display_basic_repo_info(self, repo: Repo) -> None:
        """
        Sub-function of: show_info_from_repo

        handles the display of some information such as
        the files that were in the last commit
        """
        file_status = {
            "untracked": repo.untracked_files,
            "unstaged": [item.a_path for item in repo.index.diff(None)],
            "staged": [item.a_path for item in repo.index.diff("HEAD")]
        }

        branch_icon = " "
        git_icon = "󰊢 "
        clean_icon = " "
        path = os.getcwd()
        name = os.path.basename(path)

        print_cf(f"Information for: {git_icon}{name}", "G")
        print_cf(f"Current branch: {branch_icon}{repo.active_branch}", "B")

        if self.is_repo_clean(repo):
            print_cf(f"Branch status: {clean_icon}Clean", "G")
            print()

        else:
            self.display_dirty_status(file_status)

    def display_dirty_status(self, file_status: dict) -> None:
        """
        Sub-function of: display_basic_repo_info
        """
        dirty_icon = " "

        print_cf(f"branch status: {dirty_icon} Dirty", "R")
        print_cf(f"{'' * 3}dirty files:", "R")

        for status, files in file_status.items():
            for file in files:
                self.display_file_status(file, status)

        print()

    def display_file_status(self, file: str, status: int) -> None:
        """
        Sub-function of: display_dirty_status
        """
        file_icon = "  "
        untracked_ic = "  "
        unstaged_ic = "  "
        staged_ic = " 󰈖 "
        color = ""

        status_icons = {
            "untracked": untracked_ic,
            "unstaged": unstaged_ic,
            "staged": staged_ic
        }
        if status == "untracked":
            color = "M"
        if status == "unstaged":
            color = "Y"
        if status == "staged":
            color = "G"

        print_cf(
            f"  - {file_icon}{file} Status: {status}{status_icons[status]}",
            color
        )

    def display_commit_info(self, commit_info: dict) -> None:
        """
        Sub-function of: show_info_from_repo
        """
        file_icon = " "
        print_cf(f"Last commit: {commit_info['commit_abbr']}", "B")
        print_cf(f"Commit ID: {commit_info['commit_id']}", "B")
        print_cf(f"Message: {commit_info['commit_message']}", "B")
        print()

        print_cf("Files in the commit:", "B")
        for file in commit_info['committed_files']:
            print_cf(f" - {file_icon}{file}", "G")

        print()

    def is_repo_clean(self, repo: Repo) -> bool:
        return not (repo.untracked_files or
                    repo.index.diff(None) or
                    repo.index.diff("HEAD"))

    """
    End Section:
    Display Information from current repo
    """

    """
    Section:
    Commit work
    """

    def commit_work(self, repo: Repo, commit_msg: list[str]) -> None:
        """
        Main function

        Handles the flag -c --commit
        """
        common_prefixes = [
            "[Added]",
            "[Improved]",
            "[Solved]",
            "[Deleted]",
            "[Renamed]",
            "[Modified]",
            "[Hot Fix]",
            None,
            "No preffix",
            "Cancel Commit"
        ]

        try:
            staged_files = [item.a_path for item in repo.index.diff("HEAD")]
            if not staged_files:
                self.handle_no_staged_files(repo)

            if commit_msg:
                self.handler_commit_msg(repo, commit_msg)

            self.display_files_to_commit(repo, staged_files)
            prefix = self.get_commit_prefix(common_prefixes)
            commit = asyncio.run(self.get_commit_message(prefix))

            commit_msg = prefix + ' ' + commit

            repo.index.commit(commit_msg)
            debug("Commit Done!!", "I")

        except git.exc.BadName:
            if commit_msg:
                self.handler_commit_msg(repo, commit_msg)
            self.first_commit(repo)

    def handler_commit_msg(self, repo: Repo, msg: str) -> None:
        """Subfunction of 'commit_work'
        """
        file_icon = " "

        if len(msg) != 1:
            debug("Multiple commit messages were giving, aborting!", "E")
            debug("Usage: pygit++ -c [commit_msg]", "I")
            sys.exit(1)

        repo.index.commit(msg[0])
        affected_files = list(repo.head.commit.stats.files.keys())
        print_cf("Commited files:", "B")

        for file in affected_files:
            print_cf(f" -{file_icon} {file}", "G")
        print()

        debug("Commit Done!", "I")
        sys.exit(0)

    def handle_no_staged_files(self, repo: Repo) -> None:
        """ Subfunction of 'commit work'
        Handler for when there are not staged files.
        """

        debug("There are no files to commit!", "W")
        debug("Would you like to add files to commit?", "M")
        print()

        if yes_or_no_menu() == 'Y':
            self.add_files_to_index(repo)

        else:
            debug("Commit action cancelled by user", "I")
            sys.exit()

    def display_files_to_commit(self, repo: Repo,
                                staged_files: list[str]) -> None:
        """
        Sub-function of 'commit_work'
        """
        file_icon = " "

        print_cf("Files that will be committed:", "G")
        for item in staged_files:
            print_cf(f" - {file_icon} {item}", "B")

        print()

    def get_commit_prefix(self, common_prefixes: list[str]) -> str:
        """
        Sub-function of 'commit_work':
        """

        print_cf("Would you like to add a prefix to your commit", "Y")
        print()
        index = multiple_choice_menu(common_prefixes)
        if index != 8 and index != 9:
            return common_prefixes[index]
        elif index == 8:
            return ""
        else:
            debug("Commit canceled by user", "I")
            sys.exit()

    async def get_commit_message(self, prefix: str) -> str:
        """
        Sub-function of 'Commit work':
        """

        app = miniCommitTypingApp(prefix)
        return await app.run()

    def first_commit(self, repo: Repo) -> None:
        """
        Sub-function of 'commit_work':
        """

        staged_files = [item[0] for item in repo.index.entries.keys()]
        if not staged_files:
            self.add_files_to_index(repo)

        self.display_files_to_commit(repo, staged_files)

        print_cf("Please introduce your first commit message:", "C")
        commit = input(">> ")
        repo.index.commit(commit)
        print()
        debug("FIRST COMMIT DONE!!", "M")

    """
    End Section:
    Commit Work
    """

    """
    Section:
    Add files to index
    """

    def add_files_to_index(self, repo: Repo, files_to_add=[]) -> None:
        """
        Main function
        """
        title = "Please select the files you want to add to index"

        files = repo.untracked_files + \
            [item.a_path for item in repo.index.diff(None)]

        if len(files_to_add) == 1:
            if files_to_add[0] == '.':
                repo.index.add(files)
                self.display_files_added_to_index(files)
                sys.exit(0)

        if len(files_to_add) >= 1:
            repo.index.add(files_to_add)
            self.display_files_added_to_index(files_to_add)
            sys.exit(0)

        if files:
            index = multiple_selection_menu(files, title=title)
            files_to_commit = [os.path.join(
                os.getcwd(), files[item]) for item in index]

            self.display_files_added_to_index(files_to_commit)

            repo.index.add(files_to_commit)

        else:
            debug("No new files to add to the index", "E")
            sys.exit()

    def display_files_added_to_index(self, files: list[str],) -> None:
        """
        Sub-function of: 'add_files_to_index'
        """
        for counter, item in enumerate(files):
            debug(f"File added: {os.path.basename(item)}", "I")
        print()

        print_cf(f"{counter+1} New files were added to the index!!", "G")
        print()

    """
    End Section:
    Add files to index
    """


if __name__ == "__main__":
    app = Pygit()
