from pathlib import Path

import streamlit as st

from config import ASSETS_DIR


STYLE_FILE = ASSETS_DIR / "style.css"


def load_custom_css(
    css_file: Path = STYLE_FILE
) -> None:
    """
    Load the dashboard's custom CSS file.

    Parameters
    ----------
    css_file : Path
        Path to the CSS file.

    Raises
    ------
    FileNotFoundError
        If the CSS file does not exist.

    ValueError
        If the CSS file is empty.
    """

    if not css_file.exists():
        raise FileNotFoundError(
            f"CSS file not found: {css_file}"
        )

    if css_file.stat().st_size == 0:
        raise ValueError(
            f"CSS file is empty: {css_file}"
        )

    st.html(css_file)