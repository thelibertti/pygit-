# Pygit++ official source code
# see DOCS
# version 0.1

# TODO: Well right now the following commands will be implemented:
#   - -s, --show (Display full information of the git repository)
#   - -p, --push (A better way to push code into github)
#   - -c, --commit (A better way todo commits)
#   - -a, --add (Adding files to the workarea)
# NOTE: see 'DOCS/roadmap.md'

from debug import debug
from debug import print_cf
from tools import yes_or_no_menu
from tools import multiple_selection_menu
from tools import multiple_choice_menu
from tools import miniCommitTypingApp
import argparse
import os
from git import Repo
import git
import asyncio


class pygit:
    def __init__(self):
        self.path = os.getcwd()
        self.parser = argparse.ArgumentParser(
            prog="PYGIT++",
            description="Tool to work better with git",
            epilog="version 0.01"
        )
        self.parser.add_argument('-i', '--init',
                                 action='store_true',
                                 help="starts a empty git repo")

        self.parser.add_argument('-c', '--commit',
                                 action='store_true',
                                 help="better way to commit your work")

        self.args = self.parser.parse_args()
        self.repo = self.create_repo_object(self.path)

        if self.args.init:
            self.start_repo(self.path)

        if self.args.commit:
            self.commit_work(self.repo)

        else:
            self.show_info_from_repo(self.repo)

    def create_repo_object(self, path: str) -> object:
        try:
            self.repo = Repo(path)

            if self.repo.bare:
                debug("Bare repository was found", "E")
            else:
                return self.repo
        except git.exc.InvalidGitRepositoryError:
            debug("No valid git repository could be found", "E")
            exit()

    def show_info_from_repo(self, repo: object) -> None:
        file_icon = " "

        self.last_commit = repo.head.commit
        self.commit_id = self.last_commit.hexsha
        self.commit_abbr = repo.git.rev_parse(self.commit_id, short=7)
        self.commit_message = self.last_commit.message.strip()
        self.committed_files = list(self.last_commit.stats.files.keys())

        self.basic_information_from_repo(repo)

        print_cf(f"Last commit: {self.commit_abbr}", "B")
        print_cf(f"Commit ID: {self.commit_id}", "B")
        print_cf(f"Message: {self.commit_message}", "B")
        print()
        print_cf("Files in the commit:", "B")
        for file in self.committed_files:
            print_cf(f" - {file_icon}{file}", "G")

    def start_repo(self, path: str) -> None:
        """
        Starts a git repo
        """
        command = f"git -C {path} init"
        preffix = ">/dev/null"

        if os.system(command + preffix) == 0:
            debug("Repository created succedfully!", "M")
        else:
            debug("Repository couldn't be created", "E")
        exit()

    def basic_information_from_repo(self, repo: object) -> None:
        """
        Gets and display basic information from the current
        repo
        """
        branch_icon = " "
        git_icon = "󰊢 "
        clean_icon = " "
        dirty_icon = " "
        path = os.getcwd()
        name = os.path.basename(path)

        self.repo_name = name
        self.repo_branch = repo.active_branch

        print_cf(f"Information for: {git_icon}{self.repo_name}", "G")
        print_cf(f"Current branch: {branch_icon}{self.repo_branch}", "B")

        if self.is_repo_clean(repo):
            print_cf(f"Branch status: {clean_icon}Clean", "G",)
        else:
            print_cf(f"branch status: {dirty_icon}Dirty", "R",)
        print()

    def is_repo_clean(self, repo: object) -> bool:
        """
        Check if repo is clean or not

        returns True if yes or False if not
        """
        untracked_files = repo.untracked_files
        unstaged_files = [item.a_path for item in repo.index.diff(None)]
        staged_files = [item.a_path for item in repo.index.diff("HEAD")]

        return not (untracked_files or unstaged_files or staged_files)

    def commit_work(self, repo: object):
        commom_prefixes = [
            "[ADDED]",
            "[IMPROVED]",
            "[SOLVED]",
            "[DELETED]",
            "[RENAMED]",
            "[MODIFIED]",
            None,
            "NO"

        ]
        file_icon = " "

        staged_files = [item.a_path for item in repo.index.diff("HEAD")]

        if not staged_files:
            debug("There are not files to commit!", "W")
            debug("Would you like to add files to commit?", "M")
            print()
            if yes_or_no_menu() == 'Y':
                self.add_files_to_commit(repo)
            else:
                debug("Commit action cancelled by user", "I")
                exit()

        print_cf("Files that will be committed:", "G")
        for item in staged_files:
            print_cf(f" - {file_icon} {item}", "C")

        print()

        print_cf("Would you like to add a preffix to your commit", "Y")
        print()

        index = multiple_choice_menu(commom_prefixes)

        if index == 7:
            prefix = ""
        else:
            prefix = commom_prefixes[index]

        app = miniCommitTypingApp(prefix)
        commit = asyncio.run(app.run())
        commit_msg = f"{prefix} {commit}"
        repo.index.commit(commit_msg)

        debug("Commit Done!!", "I")

    def add_files_to_commit(self, repo: object) -> tuple:
        """
        Displays a menu for the user to select the files
        they want

        then will print some debug information into the console
        """

        current_path = os.getcwd()
        files = []
        files_to_commit = []

        untracked_files = repo.untracked_files
        unstaged_files = [item.a_path for item in repo.index.diff(None)]

        files.extend(untracked_files)
        files.extend(unstaged_files)
        index = multiple_selection_menu(files)

        for item in index:
            file_path = current_path + '/' + files[item]
            files_to_commit.append(file_path)

        for item in files_to_commit:
            debug(f"file added {item}", "W")

        print()

        repo.index.add(files_to_commit)


app = pygit()
