"""Artifacts cleaner."""

from cleaners.base import BaseCleaner
from utils.logger import log_info


class ArtifactsCleaner(BaseCleaner):
    """Cleaner for GitHub Actions artifacts."""

    def clean(self, keep_latest=1):
        """Delete old artifacts, keeping the most recent N per workflow.

        Args:
            keep_latest (int): number of artifacts to keep per workflow
        """
        data = self.api_get(f"/repos/{self.repo.full_name}/actions/artifacts")
        if not data:
            return

        artifacts = data.get("artifacts", [])
        log_info(f"Found {len(artifacts)} artifacts")

        # Group artifacts by workflow run
        workflow_artifacts = {}
        for artifact in artifacts:
            workflow_run = artifact.get("workflow_run") or {}
            wf_id = workflow_run.get("id")
            workflow_artifacts.setdefault(wf_id, []).append(artifact)

        for wf_id, arts in workflow_artifacts.items():
            # Sort by created date, newest first
            arts.sort(key=lambda x: x["created_at"], reverse=True)

            # Delete all but the most recent N artifacts
            for artifact in arts[keep_latest:]:
                endpoint = f"/repos/{self.repo.full_name}/actions/artifacts/{artifact['id']}"
                if self.safe_execute(lambda: self.api_delete(endpoint), artifact["id"]):
                    log_info(
                        f"Deleting artifact: {artifact['name']} (ID: {artifact['id']}, Size: {artifact['size_in_bytes']} bytes)"
                    )
                    self.deleted_count += 1

        log_info(f"Deleted {self.deleted_count} artifacts")