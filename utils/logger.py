"""Logging utilities for GitHub Cleaner."""


def log_info(message):
    """Log an informational message.

    Args:
        message (str): message to log
    """
    print(message)


def log_error(message):
    """Log an error message.

    Args:
        message (str): error message to log
    """
    print(f"Error: {message}")


def log_deletion(item_type, item_id, details=""):
    """Log a deletion operation.

    Args:
        item_type (str): type of item being deleted
        item_id: identifier of the item
        details (str): optional additional details
    """
    if details:
        log_info(f"Deleting {item_type}: {item_id} ({details})")
    else:
        log_info(f"Deleting {item_type}: {item_id}")