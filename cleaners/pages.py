"""Pages deployments cleaner."""

from cleaners.base import BaseCleaner
from utils.logger import log_info


class PagesCleaner(BaseCleaner):
    """Cleaner for GitHub Pages deployments."""

    def clean(self):
        """Delete old Pages deployments, keeping only the most recent."""
        data = self.api_get(f"/repos/{self.repo.full_name}/pages/deployments")
        if not data:
            return

        deployments = data if isinstance(data, list) else data.get("deployments", [])
        log_info(f"Found {len(deployments)} Pages deployments")

        if len(deployments) <= 1:
            log_info("Keeping the only or most recent Pages deployment")
            return

        # Sort by created_at, newest first
        deployments.sort(key=lambda x: x.get("created_at", ""), reverse=True)

        for deployment in deployments[1:]:
            dep_id = deployment.get("id")
            endpoint = f"/repos/{self.repo.full_name}/pages/deployments/{dep_id}/cancel"
            if self.safe_execute(lambda: self.api_post(endpoint), dep_id):
                log_info(f"Canceling Pages deployment: {dep_id}")
                self.deleted_count += 1

        log_info(f"Canceled {self.deleted_count} Pages deployments")