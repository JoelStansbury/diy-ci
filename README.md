# pyci
Package for continuous testing and deployment of git repositories independed of hosting service (gihub, bitbucket, ...)

## how it works
Reapeatedly pings remote repo for changes to branches. When a change/new branch is detected, a pipeline script is executed.

## setup
* on your remote testing machine
* clone the repository you wish to test
* cd into the repo
* run `python -m pyci [-f PIPELINE_SCRIPT.py]`
  * this will initiate the infinite loop

## TODO
* integrate with github and bitbucket ci to notify succesful deployment

change