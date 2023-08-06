import importlib.resources
import json
from pathlib import Path
from typing import Any

from framework_detector import frameworks, dockerfiles


def detect(path: Path) -> dict[str, Any]:
    """Detects the framework of a given path.

    Args:
        path (Path): The path to the file or directory to detect.

    Raises:
        KeyError: Raised when a framework is not found.

    Returns:
        str: The framework name.
    """
    for value in importlib.resources.contents(frameworks):
        if value.endswith(".json") and importlib.resources.is_resource(
            frameworks, value
        ):
            data = json.loads(importlib.resources.read_text(frameworks, value))
            if check_match(path, data):
                return data

    # Not the nice way to do this, but it is the easiest way I could think of
    raise KeyError("No known framework found")


def check_match(path: Path, data: dict[str, Any]) -> bool:
    """Checks if the path matches the given framework.

    Args:
        path (Path): The path to the file or directory to check.
        data (dict[str, Any]): The data to check against.

    Returns:
        bool: Whether the framework matches the path.
    """
    for file in data["detect"]:
        if (path / file).exists():
            if data["detect"][file] is None:
                return True
            else:
                # It is needed to check whether the contents of the file match
                file_text = (path / file).read_text()
                for substring in data["detect"][file]:
                    if substring in file_text:
                        return True
    return False


def get_dockerfile(file_name: str) -> str:
    """Gets the dockerfile from the given file name.

    Args:
        file_name (str): The file name to get the dockerfile from.

    Returns:
        str: The dockerfile.
    """
    return importlib.resources.read_text(
        dockerfiles, file_name
    )


if __name__ == "__main__":
    print(detect(Path.cwd()))