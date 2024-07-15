# Pygit++ official source code
# see DOCS
# version 0.0.01

# TODO: Well right now the following commands will be implemented:
#   - -s, --show (Display full information of the git repository)
#   - -p, --push (A better way to push code into github)
#
# WARN: Known bugs/problems:
#   -   (0)
#
# NOTE: see 'DOCS/roadmap.md'

from debug import debug
from debug import print_cf
from tools import yes_or_no_menu
from tools import multiple_selection_menu
from tools import multiple_choice_menu
from tools import miniCommitTypingApp
import argparse
import os
import sys
from git import Repo
import git
from typing import List, Optional
import asyncio


class Pygit:
    def __init__(self):
        self.path = os.getcwd()
        self.setup_arg_parser()
        self.handle_args()

    def setup_arg_parser(self) -> None:
        """
        Setting up argparser with all its
        commands
        """

        self.parser = argparse.ArgumentParser(
            prog="PYGIT++",
            description="Tool to work better with git",
            epilog="version 0.0.0.01"
        )
        self.parser.add_argument(
            '-i', '--init',
            action='store_true',
            help="Starts an empty git repo")

        self.parser.add_argument(
            '-c', '--commit',
            action='store_true',
            help="A better way to commit your work")

        self.parser.add_argument(
            '-a', '--add',
            action='store_true',
            help='A better way to add your work'
        )

        self.args = self.parser.parse_args()

    def handle_args(self) -> None:
        """
        See what flags are on
        """
        if self.args.init:
            self.start_repo(self.path)

        self.repo = self.create_repo_object(self.path)

        if self.args.commit:
            self.commit_work(self.repo)
            sys.exit()

        if self.args.add:
            self.add_files_to_index(self.repo)
            sys.exit()

        else:
            self.show_info_from_repo(self.repo)
            sys.exit()

    def create_repo_object(self, path: str) -> Repo:
        """
        Creates the repo object
        """

        try:
            repo = Repo(path)
            if repo.bare:
                debug("Bare repository was found", "E")
            return repo

        except git.exc.InvalidGitRepositoryError:
            debug("No valid git repository could be found", "E")
            sys.exit()

    def show_info_from_repo(self, repo: Repo) -> None:
        """
        Main funtion

        displays the basic information
        of the current repo
        """
        try:
            last_commit = repo.head.commit
            commit_info = {
                "commit_id": last_commit.hexsha,
                "commit_abbr": repo.git.rev_parse(last_commit.hexsha, short=7),
                "commit_message": last_commit.message.strip(),
                "committed_files": list(last_commit.stats.files.keys())
            }

            self.display_basic_repo_info(repo)
            self.display_commit_info(commit_info)

        except ValueError:
            debug("NOT ENOUGH INFORMATION ABOUT THIS REPO", "W")
            debug("TRY ADDING SOME FILES FIRST OR DOING YOUR FIRST COMMIT!!",
                  "I")
            sys.exit()

    def start_repo(self, path: str) -> None:
        """
        Main function

        handles the 'init' repo
        flag
        """
        command = f"git -C {path} init"
        preffix = ">/dev/null"

        if os.system(command + preffix) == 0:
            debug("Repository created successfully!", "M")

        else:
            debug("Repository couldn't be created", "E")
        sys.exit()

    def display_basic_repo_info(self, repo: Repo) -> None:
        """
        Sub-function from: show_info_from_repo

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
        Sub-function from: display_basic_repo_info

        handles the diplay of information in case
        the current repo is dirty
        """
        dirty_icon = " "

        print_cf(f"branch status: {dirty_icon}Dirty", "R")
        print_cf(f"{'' * 3}dirty files:", "R")

        for status, files in file_status.items():
            for file in files:
                self.display_file_status(file, status)

        print()

    def display_file_status(self, file: str, status: int) -> None:
        """
        Sub-function from: display_dirty_status

        displays the files that are dirty plus their current status
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
        Sub-function from: show_info_from_repo

        handles the display of the information
        of very last commit
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

    def commit_work(self, repo: Repo) -> None:
        """
        Main function

        Handles the flag -c --commit
        in order to commit work
        """
        common_prefixes = [
            "[Added]",
            "[Improved]",
            "[Solved]",
            "[Deleted]",
            "[Renamed]",
            "[Modified]",
            None,
            "No preffix",
            "Cancel Commit"
        ]
        file_icon = " "

        try:
            staged_files = [item.a_path for item in repo.index.diff("HEAD")]
            if not staged_files:
                self.handle_no_staged_files(repo)

            staged_files = [item.a_path for item in repo.index.diff("HEAD")]
            self.display_files_to_commit(staged_files, file_icon)
            prefix = self.get_commit_prefix(common_prefixes)
            commit = asyncio.run(self.get_commit_message(prefix))

            commit_msg = prefix + ' ' + commit

            repo.index.commit(commit_msg)
            debug("Commit Done!!", "I")

        except git.exc.BadName:
            self.first_commit(repo)

    def handle_no_staged_files(self, repo: Repo) -> bool:
        debug("There are no files to commit!", "W")
        debug("Would you like to add files to commit?", "M")
        print()

        if yes_or_no_menu() == 'Y':
            self.add_files_to_index(repo)

        else:
            debug("Commit action cancelled by user", "I")
            exit()

    def display_files_to_commit(self,
                                staged_files: List[str],
                                file_icon: str) -> None:

        print_cf("Files that will be committed:", "G")
        for item in staged_files:
            print_cf(f" - {file_icon} {item}", "B")

        print()

    def get_commit_prefix(self, common_prefixes: List[Optional[str]]) -> str:
        print_cf("Would you like to add a prefix to your commit", "Y")
        print()
        index = multiple_choice_menu(common_prefixes)
        if index != 7 and index != 8:
            return common_prefixes[index]
        elif index == 7:
            return ""
        else:
            debug("Commit canceled by user", "I")
            exit()

    async def get_commit_message(self, prefix: str) -> str:
        app = miniCommitTypingApp(prefix)
        return await app.run()

    def first_commit(self, repo: Repo) -> None:
        staged_files = [item[0] for item in repo.index.entries.keys()]
        if not staged_files:
            self.add_files_to_index(repo)

        self.display_files_to_commit(staged_files, " ")

        print_cf("Please introduce your first commit message:", "C")
        commit = input(">> ")
        repo.index.commit(commit)
        print()
        debug("FIRST COMMIT DONE!!", "M")

    def add_files_to_index(self, repo: Repo) -> None:
        debug("Please select the files you want to add to index", "M")
        print()

        files = repo.untracked_files + \
            [item.a_path for item in repo.index.diff(None)]

        if files:
            index = multiple_selection_menu(files)
            files_to_commit = [os.path.join(
                os.getcwd(), files[item]) for item in index]
            for counter, item in enumerate(files_to_commit):
                debug(f"file added: {os.path.basename(item)}", "I")

            print()
            repo.index.add(files_to_commit)
            print_cf(f"{counter+1} New files were added to index!!", "G")

            print()

        else:
            debug("No new files to add to index", "E")
            sys.exit()


if __name__ == "__main__":
    app = Pygit()
