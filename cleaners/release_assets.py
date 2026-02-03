"""Release assets cleaner."""

from cleaners.base import BaseCleaner
from utils.logger import log_info


class ReleaseAssetsCleaner(BaseCleaner):
    """Cleaner for release assets."""

    def clean(self, keep_latest_releases=5):
        """Delete assets from old releases.

        Args:
            keep_latest_releases (int): number of recent releases to keep assets for
        """
        releases = list(self.repo.get_releases())
        log_info(f"Found {len(releases)} releases")

        if len(releases) <= keep_latest_releases:
            log_info(f"Keeping assets for all {len(releases)} releases")
            return

        for release in releases[keep_latest_releases:]:
            assets = list(release.get_assets())
            log_info(f"Release {release.tag_name} has {len(assets)} assets")

            for asset in assets:
                if self.safe_execute(lambda: asset.delete_asset(), asset.name):
                    size_mb = self.format_size(asset.size)
                    log_info(
                        f"Deleting asset: {asset.name} from {release.tag_name} (Size: {size_mb:.2f} MB)"
                    )
                    self.deleted_count += 1
                    self.total_size += asset.size

        self.print_summary()