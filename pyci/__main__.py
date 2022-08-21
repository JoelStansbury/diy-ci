import argparse
import os
from .git import Git
import time
import sys
from subprocess import call
from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        default=os.getcwd(),
        help="directory of the repo, default=cwd",
    )
    parser.add_argument(
        "-f",
        "--file",
        default="pyci_pipeline.py",
        help="instruction set for pyci, default='pyci.yml'",
    )
    args = parser.parse_args()
    repo = Git()
    while True:
        for b in repo.branches:
            if b.is_behind:
                print(f"  {b.name}: behind={b.is_behind}")
                with b:
                    pipeline = Path("pyci_pipeline.py")
                    if pipeline.exists():
                        call([sys.executable, "pyci_pipeline.py"])
                    else:
                        print("No pipeline to run")
        time.sleep(10)
