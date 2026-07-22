from pathlib import Path
import yaml


def read_yaml(file_path: str | Path) -> dict:
    """
    Read and return the contents of a YAML configuration file.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {file_path}"
        )
    with file_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if config is None:
        raise ValueError(
            f"Configuration file is empty: {file_path}"
        )

    return config