# pyci
Pure python CI/CD service for git repositories independent of hosting service (gihub, bitbucket, ...)

## How it works
Reapeatedly pings remote repo for changes to branches. When a change/new branch is detected, a pipeline script `ci/pipeline.py` is executed.

Because there is no dependence on the remote host, there is no way to interface with the PR-blocking we've come to expect from CI pipelines. However, the example pipeline adds a file called `ci/result` which is updated after each run to show if it failed or passed. IMO this is sufficient.

## When it is useful
This is useful when you want quick, easy, and free CI testing. If you can create a python script to do what you need then this will work for you. There is no requirement for port forwarding and will work for any git repo hosting service (even locally hosted repositories).

It does not suffer from the same vulnerability w.r.t. malicious pull-requests like self-hosted github runners do. Forks do not show up in `git for-each-ref` so they wont trigger a run. Meaning it should be fine to use on public repos (see [self-hosted-runner-security](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners#self-hosted-runner-security)).

## Pitfalls
* Currently no integration with GitHub or Bitbucket, so it will not prevent PRs from merging.
* "No port-forwarding" means there is no avenue for queued deployments, which means the testing instance must continuously ping the repo host for changes.
* With the current pipeline example, you get a ton of unnecesary commits (basically double what you would have without). This can be entirely mitigated with squash merges however.

## Setup
On your remote testing machine
* copy the `ci` folder into your repo
* clone the repository you wish to test on the system that will do the testing
  * This new copy of the repo should not be edited directly as it may cause checkout errors and stop the CI process
* cd into the repo
* run `python ci/runner.py [-f PATH/TO/SCRIPT] [-t POLLING_INTERVAL_SECONDS]`

That's it, you'll have a CI pipeline until it fails or you stop it.
