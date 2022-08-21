import argparse
import os
from .git import Git


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--path",
        type=str, 
        default=os.getcwd(),
        help="directory of the repo, default=cwd"
    )
    parser.add_argument(
        "-f", "--file",
        default="pyci.yml",
        help="instruction set for pyci, default='pyci.yml'"
    )
    args = parser.parse_args()
    repo = Git()
    for b in repo.branches:
        print(f"{b.name}: behind={b.is_behind}")
    # repo.fetch()
    # repo.checkout("new-branch")
    # print(branches.decode())