"""Configuration management for GitHub Cleaner."""

from utils.env import get_bool_env, get_int_env


class CleanerConfig:
    """Configuration for GitHub Cleaner."""

    def __init__(self):
        """Initialize configuration from environment variables."""
        # Backward compatibility: workflow_runs and deployments default to True
        self.workflow_runs = get_bool_env("CLEAN_WORKFLOW_RUNS", True)
        self.deployments = get_bool_env("CLEAN_DEPLOYMENTS", True)
        self.artifacts = get_bool_env("CLEAN_ARTIFACTS", False)
        self.caches = get_bool_env("CLEAN_CACHES", False)
        self.pages = get_bool_env("CLEAN_PAGES", False)
        self.packages = get_bool_env("CLEAN_PACKAGES", False)
        self.release_assets = get_bool_env("CLEAN_RELEASE_ASSETS", False)

        # Retention settings
        self.keep_artifacts = get_int_env("KEEP_LATEST_ARTIFACTS", 1)
        self.keep_packages = get_int_env("KEEP_LATEST_PACKAGES", 3)
        self.keep_release_assets = get_int_env("KEEP_LATEST_RELEASES", 5)

    def print_config(self):
        """Print the current configuration."""
        print("\nConfiguration:")
        print(f"  Workflow runs: {self.workflow_runs}")
        print(f"  Deployments: {self.deployments}")
        print(
            f"  Artifacts: {self.artifacts} (keep latest {self.keep_artifacts})"
        )
        print(f"  Caches: {self.caches}")
        print(f"  Pages: {self.pages}")
        print(f"  Packages: {self.packages} (keep latest {self.keep_packages})")
        print(
            f"  Release assets: {self.release_assets} (keep latest {self.keep_release_assets} releases)"
        )