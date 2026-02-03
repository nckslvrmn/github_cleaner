"""Environment variable parsing utilities."""

import os


def get_bool_env(var_name, default=False):
    """Parse boolean environment variable.

    Args:
        var_name (str): environment variable name
        default (bool): default value if not set

    Returns:
        bool: parsed boolean value
    """
    value = os.getenv(var_name, "").lower()
    if value in ("true", "1", "yes", "on"):
        return True
    elif value in ("false", "0", "no", "off", ""):
        return False if value else default
    return default


def get_int_env(var_name, default=1):
    """Parse integer environment variable.

    Args:
        var_name (str): environment variable name
        default (int): default value if not set

    Returns:
        int: parsed integer value
    """
    value = os.getenv(var_name)
    if value:
        try:
            return int(value)
        except ValueError:
            print(
                f"Warning: Invalid integer value for {var_name}, using default {default}"
            )
            return default
    return default