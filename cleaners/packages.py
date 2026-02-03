"""Packages cleaner."""

from cleaners.base import BaseCleaner
from utils.logger import log_info


class PackagesCleaner(BaseCleaner):
    """Cleaner for GitHub Container Registry packages."""

    def clean(self, keep_latest=3):
        """Delete old package versions, keeping the most recent N.

        Args:
            keep_latest (int): number of package versions to keep
        """
        owner = self.repo.owner.login

        # Try both user and org endpoints
        packages = None
        endpoint_type = None
        for ep_type in ["users", "orgs"]:
            data = self.api_get(f"/{ep_type}/{owner}/packages")
            if data:
                packages = data if isinstance(data, list) else []
                endpoint_type = ep_type
                break

        if not packages or not endpoint_type:
            log_info("Unable to access packages endpoint")
            return

        log_info(f"Found {len(packages)} packages")

        for package in packages:
            pkg_type = package.get("package_type")
            pkg_name = package.get("name")

            versions_data = self.api_get(
                f"/{endpoint_type}/{owner}/packages/{pkg_type}/{pkg_name}/versions"
            )
            if not versions_data:
                continue

            versions = versions_data if isinstance(versions_data, list) else []
            versions.sort(key=lambda x: x.get("created_at", ""), reverse=True)

            log_info(f"Package {pkg_name} has {len(versions)} versions, keeping {keep_latest}")

            for version in versions[keep_latest:]:
                ver_id = version.get("id")
                endpoint = f"/{endpoint_type}/{owner}/packages/{pkg_type}/{pkg_name}/versions/{ver_id}"
                if self.safe_execute(lambda: self.api_delete(endpoint), ver_id):
                    log_info(f"Deleting package version: {pkg_name}@{version.get('name', ver_id)}")
                    self.deleted_count += 1

        log_info(f"Deleted {self.deleted_count} package versions")