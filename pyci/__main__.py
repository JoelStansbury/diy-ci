import argparse
import os
from .git import Git, CACHE
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
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=60 * 60,  # every hour
        help="time to wait between querying the repo hosting service for changes. default = 3600 (seconds)",
    )
    args = parser.parse_args()
    repo = Git()
    while True:
        for b in repo.branches:
            if b.is_behind:
                with b:
                    pipeline = Path(args.file)
                    if pipeline.exists():
                        call([sys.executable, str(pipeline)])
                    else:
                        print("No pipeline to run")
        time.sleep(args.timeout)
