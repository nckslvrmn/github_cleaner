"""Base cleaner class with common functionality."""

from abc import ABC, abstractmethod
from github import GithubException

from utils.logger import log_info, log_error


class BaseCleaner(ABC):
    """Abstract base class for all cleaners."""

    def __init__(self, github, repo):
        """Initialize the cleaner.

        Args:
            github: GitHub API client object
            repo: GitHub repository object
        """
        self.github = github
        self.repo = repo
        self.deleted_count = 0
        self.total_size = 0

    @abstractmethod
    def clean(self, **kwargs):
        """Implement cleanup logic in subclasses.

        Args:
            **kwargs: cleaner-specific arguments
        """
        pass

    def safe_execute(self, func, item_id):
        """Execute function with standard error handling.

        Args:
            func: function to execute
            item_id: identifier for logging

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            func()
            return True
        except GithubException as e:
            log_error(
                f"Failed on {item_id}: {e.status} - {e.data.get('message', 'Unknown')}"
            )
            return False
        except Exception as e:
            log_error(f"Failed on {item_id}: {str(e)}")
            return False

    def api_get(self, endpoint):
        """Wrapper for GET requests.

        Args:
            endpoint (str): API endpoint path

        Returns:
            dict: response data or None on error
        """
        try:
            headers, data = self.github._Github__requester.requestJsonAndCheck(
                "GET", endpoint
            )
            return data
        except GithubException as e:
            if e.status == 404:
                log_info(f"Endpoint not found: {endpoint}")
            else:
                log_error(f"GET {endpoint} failed: {e.status}")
            return None

    def api_delete(self, endpoint):
        """Wrapper for DELETE requests.

        Args:
            endpoint (str): API endpoint path
        """
        self.github._Github__requester.requestJsonAndCheck("DELETE", endpoint)

    def api_post(self, endpoint):
        """Wrapper for POST requests.

        Args:
            endpoint (str): API endpoint path
        """
        self.github._Github__requester.requestJsonAndCheck("POST", endpoint)

    def format_size(self, bytes_size):
        """Convert bytes to MB.

        Args:
            bytes_size (int): size in bytes

        Returns:
            float: size in megabytes
        """
        return bytes_size / (1024 * 1024)

    def print_summary(self):
        """Print cleanup summary."""
        if self.total_size > 0:
            size_mb = self.format_size(self.total_size)
            log_info(f"Deleted {self.deleted_count} items, freed {size_mb:.2f} MB")
        else:
            log_info(f"Deleted {self.deleted_count} items")