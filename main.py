# Pygit++ official source code
# see DOCS
# version 0.1

# TODO: Well right now the following commands will be implemented:
#   - -s, --show (Display full information of the git repository)
#   - -p, --push (A better way to push code into github)
#   - -c, --commit (A better way todo commits)
# NOTE: see 'DOCS/roadmap.md'

from debug import debug
from debug import print_colorful
import argparse
import os
from git import Repo
import git


class pygit:
    def __init__(self):
        self.path = os.getcwd()
        self.parser = argparse.ArgumentParser(
            prog="PYGIT++",
            description="Tool to work better with git",
            epilog="version 0.01"
        )
        self.parser.add_argument('--init', action='store_true')

        self.parser.add_argument('-c', '--commit', action='store_true')
        self.args = self.parser.parse_args()

        if self.args.init:
            self.start_repo(self.path)

        self.repo = self.create_repo_object(self.path)
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
        branch_icon = " "
        git_icon = "󰊢 "
        file_icon = " "
        path = os.getcwd()
        name = os.path.basename(path)

        self.repo_name = name
        self.repo_branch = repo.active_branch
        self.last_commit = repo.head.commit
        self.commit_id = self.last_commit.hexsha
        self.commit_abbr = repo.git.rev_parse(self.commit_id, short=7)
        self.commit_message = self.last_commit.message.strip()
        self.committed_files = list(self.last_commit.stats.files.keys())

        print_colorful(f"Information for: {git_icon}{self.repo_name}", "G")
        print_colorful(f"Current branch: {branch_icon}{self.repo_branch}", "B")
        print()

        print_colorful(f"Last commit: {self.commit_abbr}", "B")
        print_colorful(f"Commit ID: {self.commit_id}", "B")
        print_colorful(f"Message: {self.commit_message}", "B")
        print()
        print_colorful("Files in the commit:", "B")
        for file in self.committed_files:
            print_colorful(f" - {file_icon}{file}", "G")

    def start_repo(self, path: str) -> None:
        command = f"git -C {path} init"
        preffix = ">/dev/null"

        if os.system(command + preffix) == 0:
            debug("Repository created succedfully!", "M")
        else:
            debug("Repository couldn't be created", "E")
        exit()


app = pygit()
