"""Deployments cleaner."""

from cleaners.base import BaseCleaner
from utils.logger import log_info


class DeploymentsCleaner(BaseCleaner):
    """Cleaner for inactive deployments."""

    def clean(self):
        """Delete all inactive deployments."""
        deployments = list(self.repo.get_deployments())
        log_info(f"Found {len(deployments)} deployments")

        for deployment in deployments:
            try:
                statuses = list(deployment.get_statuses())
                if statuses and statuses[0].state == "inactive":
                    if self.safe_execute(
                        lambda: self.api_delete(deployment.url), deployment.id
                    ):
                        log_info(
                            f"Deleting inactive deployment: {deployment.id} (environment: {deployment.environment})"
                        )
                        self.deleted_count += 1
            except Exception as e:
                log_info(f"Skipping deployment {deployment.id}: {str(e)}")

        log_info(f"Deleted {self.deleted_count} inactive deployments")