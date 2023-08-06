"""Gear toolkit utilities module."""
import json
import logging
import math
import subprocess
import sys
import typing as t

log = logging.getLogger(__name__)

try:
    # Make numpy optional
    import numpy as np

    NUMPY = True
except ImportError:
    NUMPY = False


def install_requirements(req_file):
    """Install requirements from a file programatically

    Args:
        req_file (str): Path to requirements file

    Raises:
        SystemExit: If there was an error from pip
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
    except subprocess.CalledProcessError as e:
        log.error(f"Could not install requirements, pip exit code {e.returncode}")
        sys.exit(1)


class MetadataEncoder(json.JSONEncoder):
    # Overwrite default handler for bytes objects
    def default(self, obj: t.Any) -> t.Any:
        """Default json encoder when not handled.

        Handle bytes objects and pass everything else to the default JSONEncoder.

        For bytes, convert to hex and return the first 10 characters, or truncate.

        Args:
            obj (Any): Object to be encoded, can be anything, this only handles bytes.

        Returns:
            str: encoded obj.
        """
        if isinstance(obj, bytes):
            return (
                obj.hex()
                if len(obj) < 10
                else f"{obj.hex()[:10]} ... truncated byte value."
            )

        if NUMPY:  # only if numpy is available
            if type(obj).__module__ == np.__name__:
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                else:
                    return obj.item()

        return json.JSONEncoder.default(self, obj)


def convert_nan_in_dict(d: dict) -> dict:
    # Note: convert_nan_in_dict is borrowed from core-api
    return {key: _convert_nan(value) for key, value in d.items()}


def _convert_nan(
    d: t.Optional[t.Union[dict, str, list, float, int]]
) -> t.Optional[t.Union[dict, str, list, float, int]]:
    # Note: _convert_nan is borrowed from core-api
    """Return converted values"""
    if d is None:
        return None
    if isinstance(d, (str, int)):
        return d
    if isinstance(d, float):
        if math.isnan(d) or math.isinf(d):
            return None
        return d
    if isinstance(d, dict):
        return {key: _convert_nan(value) for key, value in d.items()}
    if isinstance(d, list):
        return [_convert_nan(item) for item in d]
    return d
