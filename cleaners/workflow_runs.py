"""Workflow runs cleaner."""

from cleaners.base import BaseCleaner
from utils.logger import log_info


class WorkflowRunsCleaner(BaseCleaner):
    """Cleaner for workflow runs."""

    def clean(self):
        """Delete all but the most recent workflow run."""
        runs = list(self.repo.get_workflow_runs())
        log_info(f"Found {len(runs)} workflow runs, keeping the most recent one")

        for run in runs[1:]:
            if self.safe_execute(lambda: run.delete(), run.id):
                log_info(f"Deleting workflow run: {run.id} ({run.name})")
                self.deleted_count += 1

        log_info(f"Deleted {self.deleted_count} workflow runs")