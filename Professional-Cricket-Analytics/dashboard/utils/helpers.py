from typing import Any, Iterable, List
import pandas as pd
import html

# ==========================================================
# General value-cleaning helpers
# ==========================================================
def clean_unique_values(values:Iterable[Any])-> List[Any]:
    """
    Return sorted unique values after removing missing values
    and blank strings.

    Parameters
    ----------
    values : Iterable[Any]
        Collection of values from a Series, list or array.

    Returns
    -------
    List[Any]
        Cleaned and sorted unique values.
    """
    cleaned_values = []
    for value in values:
        if pd.isna(value):
            continue

        if isinstance(value, str):
            value = value.strip()

            if value == "":
                continue

        cleaned_values.append(value)

    unique_values = list(set(cleaned_values))

    try:
        return sorted(unique_values)

    except TypeError:
        return sorted(
            unique_values,
            key=lambda item: str(item)
        )

def add_all_option(
    options: List[Any],
    all_label: str = "All"
) -> List[Any]:
    """
    Add an 'All' option at the beginning of a filter list.

    Parameters
    ----------
    options : List[Any]
        Existing filter options.

    all_label : str, default="All"
        Label used for the complete unfiltered selection.

    Returns
    -------
    List[Any]
        Filter options beginning with the All label.
    """

    filtered_options = [
        option
        for option in options
        if option != all_label
    ]

    return [all_label] + filtered_options

# ==========================================================
# Column validation
# ==========================================================
def validate_required_columns(
    dataframe: pd.DataFrame,
    required_columns: List[str],
    dataframe_name: str = "DataFrame"
) -> None:
    """
    Validate that all required columns exist in a DataFrame.

    Parameters
    ----------
    dataframe : pd.DataFrame
        DataFrame to validate.

    required_columns : List[str]
        Columns required by the operation.

    dataframe_name : str, default="DataFrame"
        Name used in the error message.

    Raises
    ------
    KeyError
        If one or more required columns are missing.
    """

    missing_columns = []

    for column in required_columns:
        if column not in dataframe.columns:
            missing_columns.append(column)

    if missing_columns:
        raise KeyError(
            f"{dataframe_name} is missing required columns: "
            f"{missing_columns}"
        )

# ==========================================================
# Numeric formatting
# ==========================================================
def format_integer(value: Any) -> str:
    """
    Format a value as a comma-separated integer.
    """

    if pd.isna(value):
        return "0"

    try:
        return f"{int(round(float(value))):,}"

    except (TypeError, ValueError):
        return "0"

def format_decimal(
    value: Any,
    decimal_places: int = 2
) -> str:
    """
    Format a value using a fixed number of decimal places.
    """

    if pd.isna(value):
        return f"{0:.{decimal_places}f}"

    try:
        return f"{float(value):,.{decimal_places}f}"

    except (TypeError, ValueError):
        return f"{0:.{decimal_places}f}"

def format_percentage(
    value: Any,
    decimal_places: int = 1
) -> str:
    """
    Format a numeric value as a percentage.

    The function expects the supplied value to already represent
    a percentage.

    Example
    -------
    62.45 becomes '62.5%'.
    """

    if pd.isna(value):
        return f"{0:.{decimal_places}f}%"

    try:
        return f"{float(value):.{decimal_places}f}%"

    except (TypeError, ValueError):
        return f"{0:.{decimal_places}f}%"

# ==========================================================
# Safe calculations
# ==========================================================
def safe_divide(
    numerator: float,
    denominator: float,
    default: float = 0.0
) -> float:
    """
    Divide two values safely.

    Returns the default value when the denominator is zero,
    missing or invalid.
    """

    if pd.isna(denominator) or denominator == 0:
        return default

    try:
        return numerator / denominator

    except (TypeError, ValueError, ZeroDivisionError):
        return default

def calculate_percentage(
    numerator: float,
    denominator: float
) -> float:
    """
    Calculate a percentage safely.
    """

    return safe_divide(
        numerator=numerator * 100,
        denominator=denominator,
        default=0.0
    )

def create_page_header(
    title: str,
    subtitle: str,
    icon: str = "🏏"
) -> str:
    """
    Create a reusable styled dashboard page header.

    User-supplied text is escaped before being inserted into HTML.
    """

    safe_title = html.escape(str(title))
    safe_subtitle = html.escape(str(subtitle))
    safe_icon = html.escape(str(icon))

    return f"""
    <div class="cv-page-header">
        <div class="cv-section-label">
            CricVision AI
        </div>

        <h1>
            {safe_icon} {safe_title}
        </h1>

        <p>
            {safe_subtitle}
        </p>
    </div>
    """

def create_information_card(
    title: str,
    description: str,
    icon: str = "📊"
) -> str:
    """
    Create a reusable information card.
    """

    safe_title = html.escape(str(title))
    safe_description = html.escape(str(description))
    safe_icon = html.escape(str(icon))

    return f"""
    <div class="cv-card">
        <h3>
            {safe_icon} {safe_title}
        </h3>

        <p>
            {safe_description}
        </p>
    </div>
    """