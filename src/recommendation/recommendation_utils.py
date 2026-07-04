"""
recommendation_utils.py
========================================================
Project   : AI-Based Personalized Diet Recommendation System
Module    : recommendation.recommendation_utils
Author    : Senior ML / Backend Engineering Team
Purpose   : Shared utility functions used across the recommendation
            package (dataset I/O, validation, scoring helpers, and
            console-friendly reporting).

This module intentionally contains NO business logic specific to any
single recommendation step. Anything used by two or more modules in
`recommendation/` (or `health/`) should live here to avoid duplicated
code, per project coding standards.
========================================================
"""

from __future__ import annotations

import os
import logging
from typing import Any, Dict, Iterable, List, Optional, Union

import pandas as pd

# ------------------------------------------------------------------
# Module-level logger
# ------------------------------------------------------------------
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


# ------------------------------------------------------------------
# Dataset I/O
# ------------------------------------------------------------------
def load_dataset(file_path: str) -> pd.DataFrame:
    """
    Load a CSV dataset into a pandas DataFrame.

    Parameters
    ----------
    file_path : str
        Absolute or relative path to the CSV file.

    Returns
    -------
    pd.DataFrame
        The loaded dataset.

    Raises
    ------
    FileNotFoundError
        If the file does not exist at the given path.
    ValueError
        If the file is empty or cannot be parsed as CSV.
    """
    if not isinstance(file_path, str) or not file_path.strip():
        raise ValueError("file_path must be a non-empty string.")

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Dataset not found at path: {file_path}")

    try:
        dataframe = pd.read_csv(file_path)
    except pd.errors.EmptyDataError as exc:
        raise ValueError(f"Dataset at {file_path} is empty.") from exc
    except pd.errors.ParserError as exc:
        raise ValueError(f"Dataset at {file_path} could not be parsed.") from exc

    if dataframe.empty:
        raise ValueError(f"Dataset at {file_path} contains no rows.")

    logger.info("Loaded dataset '%s' with shape %s", file_path, dataframe.shape)
    return dataframe


def save_dataset(dataframe: pd.DataFrame, file_path: str) -> None:
    """
    Save a pandas DataFrame to a CSV file.

    Parameters
    ----------
    dataframe : pd.DataFrame
        The DataFrame to persist.
    file_path : str
        Destination path for the CSV file.

    Raises
    ------
    ValueError
        If `dataframe` is not a DataFrame or `file_path` is invalid.
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise ValueError("dataframe must be a pandas DataFrame.")
    if not isinstance(file_path, str) or not file_path.strip():
        raise ValueError("file_path must be a non-empty string.")

    directory = os.path.dirname(file_path)
    if directory and not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=True)

    dataframe.to_csv(file_path, index=False)
    logger.info("Saved dataset to '%s' with shape %s", file_path, dataframe.shape)


# ------------------------------------------------------------------
# Validation helpers
# ------------------------------------------------------------------
def validate_positive_number(value: Union[int, float], field_name: str) -> float:
    """
    Validate that a value is numeric and strictly positive.

    Parameters
    ----------
    value : int or float
        The value to validate.
    field_name : str
        Name of the field, used for descriptive error messages.

    Returns
    -------
    float
        The validated value, cast to float.

    Raises
    ------
    TypeError
        If value is not numeric.
    ValueError
        If value is not strictly positive.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{field_name} must be a number, got {type(value).__name__}.")
    if value <= 0:
        raise ValueError(f"{field_name} must be a positive number, got {value}.")
    return float(value)


def validate_non_negative_number(value: Union[int, float], field_name: str) -> float:
    """
    Validate that a value is numeric and non-negative (allows zero).

    Parameters
    ----------
    value : int or float
        The value to validate.
    field_name : str
        Name of the field, used for descriptive error messages.

    Returns
    -------
    float
        The validated value, cast to float.

    Raises
    ------
    TypeError
        If value is not numeric.
    ValueError
        If value is negative.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{field_name} must be a number, got {type(value).__name__}.")
    if value < 0:
        raise ValueError(f"{field_name} must be a non-negative number, got {value}.")
    return float(value)


def validate_required_columns(dataframe: pd.DataFrame, required_columns: Iterable[str]) -> None:
    """
    Ensure a DataFrame contains all required columns.

    Parameters
    ----------
    dataframe : pd.DataFrame
        The DataFrame to inspect.
    required_columns : Iterable[str]
        Column names that must be present.

    Raises
    ------
    ValueError
        If any required column is missing.
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise ValueError("dataframe must be a pandas DataFrame.")

    missing = [col for col in required_columns if col not in dataframe.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")


def validate_goal(goal: str, allowed_goals: Iterable[str]) -> str:
    """
    Validate a user's dietary goal against an allowed set.

    Parameters
    ----------
    goal : str
        The goal supplied by the user (case-insensitive).
    allowed_goals : Iterable[str]
        The set of valid goal identifiers.

    Returns
    -------
    str
        The normalized (lower-case, stripped) goal string.

    Raises
    ------
    ValueError
        If goal is empty or not part of allowed_goals.
    """
    if not isinstance(goal, str) or not goal.strip():
        raise ValueError("goal must be a non-empty string.")

    normalized_goal = goal.strip().lower()
    normalized_allowed = {g.strip().lower() for g in allowed_goals}

    if normalized_goal not in normalized_allowed:
        raise ValueError(
            f"Invalid goal '{goal}'. Expected one of: {sorted(normalized_allowed)}"
        )
    return normalized_goal


# ------------------------------------------------------------------
# Numeric / scoring helpers
# ------------------------------------------------------------------
def calculate_percentage(part: Union[int, float], whole: Union[int, float]) -> float:
    """
    Calculate what percentage `part` is of `whole`.

    Parameters
    ----------
    part : int or float
        The partial value.
    whole : int or float
        The total value.

    Returns
    -------
    float
        Percentage value (0-100 scale, may exceed 100 if part > whole).

    Raises
    ------
    ValueError
        If whole is zero (division by zero) or values are negative.
    """
    part = validate_non_negative_number(part, "part")
    whole = validate_non_negative_number(whole, "whole")

    if whole == 0:
        raise ValueError("whole must not be zero when calculating a percentage.")

    return (part / whole) * 100.0


def calculate_calorie_difference(required_calories: float, food_calories: float) -> float:
    """
    Calculate the absolute difference between required and actual calories.

    Parameters
    ----------
    required_calories : float
        The target/required caloric value.
    food_calories : float
        The caloric value of the food item being evaluated.

    Returns
    -------
    float
        Absolute difference between the two values.
    """
    required_calories = validate_non_negative_number(required_calories, "required_calories")
    food_calories = validate_non_negative_number(food_calories, "food_calories")
    return abs(required_calories - food_calories)


def normalize_score(value: float, min_value: float, max_value: float) -> float:
    """
    Normalize a value into a 0-1 range using min-max scaling.

    Parameters
    ----------
    value : float
        The value to normalize.
    min_value : float
        The minimum value in the distribution.
    max_value : float
        The maximum value in the distribution.

    Returns
    -------
    float
        Normalized value between 0.0 and 1.0. Returns 0.5 if
        min_value == max_value (avoids division by zero, treats the
        distribution as flat).
    """
    if not all(isinstance(v, (int, float)) and not isinstance(v, bool)
               for v in (value, min_value, max_value)):
        raise TypeError("value, min_value, and max_value must all be numeric.")

    if max_value == min_value:
        return 0.5

    normalized = (value - min_value) / (max_value - min_value)
    return max(0.0, min(1.0, normalized))


def safe_column_normalize(dataframe: pd.DataFrame, column: str) -> pd.Series:
    """
    Normalize an entire DataFrame column to a 0-1 range.

    Parameters
    ----------
    dataframe : pd.DataFrame
        The source DataFrame.
    column : str
        The column name to normalize.

    Returns
    -------
    pd.Series
        A new Series with normalized values.

    Raises
    ------
    ValueError
        If the column does not exist in the DataFrame.
    """
    validate_required_columns(dataframe, [column])

    min_value = dataframe[column].min()
    max_value = dataframe[column].max()

    if max_value == min_value:
        return pd.Series([0.5] * len(dataframe), index=dataframe.index)

    return (dataframe[column] - min_value) / (max_value - min_value)


# ------------------------------------------------------------------
# Reporting helpers
# ------------------------------------------------------------------
def print_recommendation(recommendations: Union[pd.DataFrame, Dict[str, Any]]) -> None:
    """
    Print a human-readable summary of recommendation results to console.

    Parameters
    ----------
    recommendations : pd.DataFrame or dict
        Either a ranked DataFrame of foods, or a meal-plan dictionary
        (as produced by meal_planner.plan_meals).

    Raises
    ------
    TypeError
        If recommendations is neither a DataFrame nor a dict.
    """
    if isinstance(recommendations, pd.DataFrame):
        if recommendations.empty:
            print("No recommendations available.")
            return
        print("\n" + "=" * 60)
        print("TOP FOOD RECOMMENDATIONS")
        print("=" * 60)
        display_columns = [
            col for col in ("food", "Caloric Value", "Protein", "Fat",
                             "Carbohydrates", "Nutrition Density")
            if col in recommendations.columns
        ]
        print(recommendations[display_columns].to_string(index=False))
        print("=" * 60 + "\n")

    elif isinstance(recommendations, dict):
        print("\n" + "=" * 60)
        print("PERSONALIZED MEAL PLAN")
        print("=" * 60)
        for meal_name, meal_data in recommendations.items():
            print(f"\n-- {meal_name.upper()} --")
            if isinstance(meal_data, dict) and "foods" in meal_data:
                foods_df = meal_data["foods"]
                target_cal = meal_data.get("target_calories", "N/A")
                print(f"Target Calories: {target_cal}")
                if isinstance(foods_df, pd.DataFrame) and not foods_df.empty:
                    cols = [c for c in ("food", "Caloric Value", "Protein")
                            if c in foods_df.columns]
                    print(foods_df[cols].to_string(index=False))
                else:
                    print("No foods assigned.")
        print("=" * 60 + "\n")
    else:
        raise TypeError(
            "recommendations must be a pandas DataFrame or a dictionary."
        )


def get_top_n(dataframe: pd.DataFrame, n: int, sort_column: str,
              ascending: bool = False) -> pd.DataFrame:
    """
    Return the top N rows of a DataFrame sorted by a given column.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Source DataFrame.
    n : int
        Number of rows to return.
    sort_column : str
        Column name to sort by.
    ascending : bool, optional
        Sort order. Defaults to False (descending / best-first).

    Returns
    -------
    pd.DataFrame
        Top N rows, sorted.

    Raises
    ------
    ValueError
        If n is not positive or sort_column is missing.
    """
    validate_required_columns(dataframe, [sort_column])
    if not isinstance(n, int) or n <= 0:
        raise ValueError(f"n must be a positive integer, got {n}.")

    return dataframe.sort_values(by=sort_column, ascending=ascending).head(n).reset_index(drop=True)


# ------------------------------------------------------------------
# Example usage / smoke test
# ------------------------------------------------------------------
if __name__ == "__main__":
    # Demonstrate core utility behaviors with lightweight sample data.
    sample_df = pd.DataFrame({
        "food": ["Apple", "Chicken Breast", "Almonds", "Broccoli"],
        "Caloric Value": [52, 165, 579, 34],
        "Protein": [0.3, 31.0, 21.2, 2.8],
        "Nutrition Density": [45.2, 88.7, 60.1, 92.4],
    })

    print("Percentage example (25 of 200):", calculate_percentage(25, 200))
    print("Calorie difference example:", calculate_calorie_difference(2000, 1850))
    print("Normalize example (75 in [0, 100]):", normalize_score(75, 0, 100))

    top_2 = get_top_n(sample_df, n=2, sort_column="Nutrition Density")
    print_recommendation(top_2)
