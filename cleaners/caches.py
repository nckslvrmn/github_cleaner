"""Caches cleaner."""

from cleaners.base import BaseCleaner
from utils.logger import log_info


class CachesCleaner(BaseCleaner):
    """Cleaner for GitHub Actions caches."""

    def clean(self):
        """Delete all GitHub Actions caches."""
        data = self.api_get(f"/repos/{self.repo.full_name}/actions/caches")
        if not data:
            return

        caches = data.get("actions_caches", [])
        log_info(f"Found {len(caches)} caches")

        for cache in caches:
            endpoint = f"/repos/{self.repo.full_name}/actions/caches/{cache['id']}"
            if self.safe_execute(lambda: self.api_delete(endpoint), cache["id"]):
                size_mb = self.format_size(cache["size_in_bytes"])
                log_info(f"Deleting cache: {cache['key']} (ID: {cache['id']}, Size: {size_mb:.2f} MB)")
                self.deleted_count += 1
                self.total_size += cache["size_in_bytes"]

        self.print_summary()