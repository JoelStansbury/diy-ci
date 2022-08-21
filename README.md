# pyci
Package for continuous testing and deployment of git repositories independent of hosting service (gihub, bitbucket, ...)

## When it is useful
This is useful when you want quick, easy, and free CI testing. If you can create a python script to execute what you want to be done then this will work for you. There is no requirement for port forwarding and will work on any git repo hosting service (even locally hosted repositories).

## Pitfalls
* Currently no integration with GitHub or Bitbucket, so it will not prevent PRs from merging unless you get creative with the `on_success` and `on_failure` functions.
* "No port-forwarding" means there is no avenue for queued deployments, which means the testing instance must continuously ping the repo host for changes.

## How it works
Reapeatedly pings remote repo for changes to branches. When a change/new branch is detected, a pipeline script is executed.

> NOTE: You should not use this on public repos as a Pull-Request from a fork can be used to run malicious code on your machine. This is also true with self-hosted GitHub runners


## setup
* on your remote testing machine
* clone the repository you wish to test
* cd into the repo
* run `python -m pyci [-f PIPELINE_SCRIPT.py]`
  * this will initiate the infinite loop

## TODO
* integrate with github and bitbucket ci to notify succesful deployment
