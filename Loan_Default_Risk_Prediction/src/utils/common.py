from pathlib import Path
import yaml


def read_yaml(file_path: str) -> dict:
    """
    Read a YAML configuration file.

    Parameters
    ----------
    file_path : str
        Path to the YAML file.

    Returns
    -------
    dict
        Parsed configuration dictionary.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return config