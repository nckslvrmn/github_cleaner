#!/usr/bin/env python3

import os
import sys
from github import Github, GithubException

from utils.config import CleanerConfig
from cleaners.workflow_runs import WorkflowRunsCleaner
from cleaners.deployments import DeploymentsCleaner
from cleaners.artifacts import ArtifactsCleaner
from cleaners.caches import CachesCleaner
from cleaners.pages import PagesCleaner
from cleaners.packages import PackagesCleaner
from cleaners.release_assets import ReleaseAssetsCleaner


def main():
    """Main function orchestrating the cleaning of old resources in a Github repo."""
    # Validate required environment variables
    token = os.getenv("GITHUB_TOKEN")
    repository = os.getenv("GITHUB_REPOSITORY")

    if not token or not repository:
        print(
            "Error: GITHUB_TOKEN and GITHUB_REPOSITORY environment variables must be set"
        )
        sys.exit(1)

    print(f"Starting cleanup for repository: {repository}")

    # Load configuration
    config = CleanerConfig()
    config.print_config()

    try:
        github = Github(token)
        repo = github.get_repo(repository)

        if config.workflow_runs:
            print("\n=== Deleting old workflow runs ===")
            WorkflowRunsCleaner(github, repo).clean()

        if config.deployments:
            print("\n=== Deleting inactive deployments ===")
            DeploymentsCleaner(github, repo).clean()

        if config.artifacts:
            print("\n=== Deleting old artifacts ===")
            ArtifactsCleaner(github, repo).clean(config.keep_artifacts)

        if config.caches:
            print("\n=== Deleting old caches ===")
            CachesCleaner(github, repo).clean()

        if config.pages:
            print("\n=== Deleting old Pages deployments ===")
            PagesCleaner(github, repo).clean()

        if config.packages:
            print("\n=== Deleting old packages ===")
            PackagesCleaner(github, repo).clean(config.keep_packages)

        if config.release_assets:
            print("\n=== Deleting old release assets ===")
            ReleaseAssetsCleaner(github, repo).clean(config.keep_release_assets)

        print("\n=== Cleanup completed successfully ===")
    except GithubException as e:
        print(
            f"GitHub API error: {e.status} - {e.data.get('message', 'Unknown error')}"
        )
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
