github_cleaner
===

# Introduction

This is a simple github action that cleans up old github action runs and deployment packages. It will retain the most recent/active of each.

# Installation

To use this, simply define an action configuration yaml in the `.github/workflows` directory of your repository with the following contents.
It can run on any trigger, but I prefer to run it on a cron schedule.

```
name: github_cleaner
on:
  schedule:
    - cron: "0 * * * *"
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Bump version and push tag
      uses: nckslvrmn/github_cleaner@master
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

The default Github token created for the action to use has enough permissions on the repo that this action is defined in.

# Local Testing

To test the semver component locally, install the python dependencies by running `pip install -r requirements.txt` where auto-tagger is checked out.

Then run the below command:
```
GITHUB_TOKEN=PAT_TOKEN GITHUB_REPO=NAME_OF_REPO ./entrypoint.py
```