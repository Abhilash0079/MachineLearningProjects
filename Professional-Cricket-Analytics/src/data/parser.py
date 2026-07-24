import json
from pathlib import Path
from typing import Any


def load_json_file(file_path: Path) -> dict[str, Any]:
    """
    Load one cricket match JSON file.

    Parameters
    ----------
    file_path : Path
        Path of the JSON file.

    Returns
    -------
    dict
        Parsed JSON data.

    Raises
    ------
    FileNotFoundError
        If the JSON file does not exist.

    ValueError
        If the file is not valid JSON.
    """

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.suffix.lower() != ".json":
        raise ValueError(f"Expected a JSON file, received: {file_path.suffix}")

    try:
        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON file: {file_path}") from error