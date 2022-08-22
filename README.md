# pyci
Script for starting a CI/CD service for git repositories independent of hosting service (gihub, bitbucket, ...)

## How it works
Reapeatedly pings remote repo for changes to branches. When a change/new branch is detected, a pipeline script `ci/pipeline.py` is executed.

Because there is no dependence on the remote host, there is no way to interface with the PR-blocking we've come to expect from CI pipelines. However, the example pipeline adds a file called `ci/result` which is updated after each run to show if it failed or passed. IMO this is sufficient.

> NOTE: You should not use this on public repos as a Pull-Request from a fork can be used to run malicious code on your machine. This is also true for self-hosted GitHub runners

## When it is useful
This is useful when you want quick, easy, and free CI testing. If you can create a python script to do what you need then this will work for you. There is no requirement for port forwarding and will work for any git repo hosting service (even locally hosted repositories).

## Pitfalls
* Currently no integration with GitHub or Bitbucket, so it will not prevent PRs from merging unless you get creative with the `on_success` and `on_failure` functions.
* "No port-forwarding" means there is no avenue for queued deployments, which means the testing instance must continuously ping the repo host for changes.
* With the current pipeline example, you get a ton of unnecesary commits (basically double what you would have without). This can be mitigated by squashing prior to merge however

## Setup
On your remote testing machine
* copy the `ci` folder into your repo
* clone the repository you wish to test on the system that will do the testing
  * This new copy of the repo should not be edited directly as it may cause checkout errors and stop the CI process
* cd into the repo
* run `python ci/runner.py [-f PATH/TO/SCRIPT] [-t POLLING_INTERVAL_SECONDS]`

That's it, you'll have a CI pipeline until it fails or you stop it. When it does fail, please let me know in the Issues section.
