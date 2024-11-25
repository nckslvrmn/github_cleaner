#!/usr/bin/env python3

import os

from github import Github


def delete_old_action_runs(repo):
    """Deletes all but the most recent Github action workflow runs.

    Args:
        repo (object): github repo object

    Returns:
        None
    """
    for run in repo.get_workflow_runs()[1:]:
        print(run)
        run.delete()


def delete_inactive_deployments(github, repo):
    """Deletes all inactive Github deployments.

    Args:
        github (object): github api client object
        repo (object): github repo object

    Returns:
        None
    """
    for deployment in repo.get_deployments():
        for status in deployment.get_statuses():
            if deployment.get_status(status.id).state == "inactive":
                print(deployment)
                github._Github__requester.requestJsonAndCheck("DELETE", deployment.url)
                break


def main():
    """Main function orchestrating the cleaning of old resources in a Github repo.

    Args:
        None

    Returns:
        None
    """
    github = Github(os.getenv("GITHUB_TOKEN"))
    repo = github.get_repo(os.getenv("GITHUB_REPOSITORY"))
    delete_old_action_runs(repo)
    delete_inactive_deployments(github, repo)


if __name__ == "__main__":
    main()
