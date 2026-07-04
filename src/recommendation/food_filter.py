"""
food_filter.py
========================================================
Project   : AI-Based Personalized Diet Recommendation System
Module    : recommendation.food_filter
Author    : Senior ML / Backend Engineering Team
Purpose   : Filter food recommendations according to a user's
            dietary goal (Weight Loss, Maintenance, Muscle Gain,
            Diabetic), applying rule-based thresholds on calories,
            protein, fat, sugar, and fiber.
========================================================
"""

from __future__ import annotations

from typing import Dict

import pandas as pd

from recommendation_utils import validate_required_columns, validate_goal

# ------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------
VALID_GOALS = ["weight loss", "maintenance", "muscle gain", "diabetic"]

REQUIRED_COLUMNS = [
    "food",
    "Caloric Value",
    "Protein",
    "Fat",
    "Carbohydrates",
    "Dietary Fiber",
    "Sugars",
]

# Percentile thresholds used to define "low" / "high" relative to the
# distribution of the dataset itself, keeping the rules data-driven
# rather than hard-coded to arbitrary absolute values.
LOW_PERCENTILE = 0.40
HIGH_PERCENTILE = 0.60


def _threshold(dataframe: pd.DataFrame, column: str, percentile: float) -> float:
    """
    Compute a percentile-based threshold for a numeric column.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Source DataFrame.
    column : str
        Column name to compute the threshold for.
    percentile : float
        Percentile in the range [0, 1].

    Returns
    -------
    float
        The threshold value at the given percentile.
    """
    return float(dataframe[column].quantile(percentile))


def filter_weight_loss(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Filter foods suitable for a Weight Loss goal.

    Rules: Low Calories, High Protein, Low Fat, Low Sugar, High Fiber.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Candidate food dataset.

    Returns
    -------
    pd.DataFrame
        Filtered subset matching weight-loss criteria.
    """
    validate_required_columns(dataframe, REQUIRED_COLUMNS)

    low_calories = _threshold(dataframe, "Caloric Value", LOW_PERCENTILE)
    high_protein = _threshold(dataframe, "Protein", HIGH_PERCENTILE)
    low_fat = _threshold(dataframe, "Fat", LOW_PERCENTILE)
    low_sugar = _threshold(dataframe, "Sugars", LOW_PERCENTILE)
    high_fiber = _threshold(dataframe, "Dietary Fiber", HIGH_PERCENTILE)

    result = dataframe[
        (dataframe["Caloric Value"] <= low_calories)
        & (dataframe["Protein"] >= high_protein)
        & (dataframe["Fat"] <= low_fat)
        & (dataframe["Sugars"] <= low_sugar)
        & (dataframe["Dietary Fiber"] >= high_fiber)
    ]

    return result.reset_index(drop=True)


def filter_maintenance(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Filter foods suitable for a Maintenance goal (balanced nutrition).

    Rule: foods whose macros fall within the middle band (between the
    low and high percentile thresholds) across calories, protein, and
    fat, representing a balanced nutritional profile.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Candidate food dataset.

    Returns
    -------
    pd.DataFrame
        Filtered subset matching maintenance criteria.
    """
    validate_required_columns(dataframe, REQUIRED_COLUMNS)

    cal_low = _threshold(dataframe, "Caloric Value", LOW_PERCENTILE)
    cal_high = _threshold(dataframe, "Caloric Value", HIGH_PERCENTILE)
    protein_low = _threshold(dataframe, "Protein", LOW_PERCENTILE)
    protein_high = _threshold(dataframe, "Protein", HIGH_PERCENTILE)
    fat_low = _threshold(dataframe, "Fat", LOW_PERCENTILE)
    fat_high = _threshold(dataframe, "Fat", HIGH_PERCENTILE)

    result = dataframe[
        dataframe["Caloric Value"].between(cal_low, cal_high)
        & dataframe["Protein"].between(protein_low, protein_high)
        & dataframe["Fat"].between(fat_low, fat_high)
    ]

    return result.reset_index(drop=True)


def filter_muscle_gain(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Filter foods suitable for a Muscle Gain goal.

    Rules: High Protein, High Calories, Moderate Fat.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Candidate food dataset.

    Returns
    -------
    pd.DataFrame
        Filtered subset matching muscle-gain criteria.
    """
    validate_required_columns(dataframe, REQUIRED_COLUMNS)

    high_protein = _threshold(dataframe, "Protein", HIGH_PERCENTILE)
    high_calories = _threshold(dataframe, "Caloric Value", HIGH_PERCENTILE)
    fat_low = _threshold(dataframe, "Fat", LOW_PERCENTILE)
    fat_high = _threshold(dataframe, "Fat", HIGH_PERCENTILE)

    result = dataframe[
        (dataframe["Protein"] >= high_protein)
        & (dataframe["Caloric Value"] >= high_calories)
        & dataframe["Fat"].between(fat_low, fat_high)
    ]

    return result.reset_index(drop=True)


def filter_diabetic(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Filter foods suitable for a Diabetic-friendly goal.

    Rules: Low Sugar, High Fiber, Moderate Carbohydrates.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Candidate food dataset.

    Returns
    -------
    pd.DataFrame
        Filtered subset matching diabetic-friendly criteria.
    """
    validate_required_columns(dataframe, REQUIRED_COLUMNS)

    low_sugar = _threshold(dataframe, "Sugars", LOW_PERCENTILE)
    high_fiber = _threshold(dataframe, "Dietary Fiber", HIGH_PERCENTILE)
    carb_low = _threshold(dataframe, "Carbohydrates", LOW_PERCENTILE)
    carb_high = _threshold(dataframe, "Carbohydrates", HIGH_PERCENTILE)

    result = dataframe[
        (dataframe["Sugars"] <= low_sugar)
        & (dataframe["Dietary Fiber"] >= high_fiber)
        & dataframe["Carbohydrates"].between(carb_low, carb_high)
    ]

    return result.reset_index(drop=True)


# ------------------------------------------------------------------
# Dispatch table mapping goal -> filter function
# ------------------------------------------------------------------
_GOAL_FILTER_MAP = {
    "weight loss": filter_weight_loss,
    "maintenance": filter_maintenance,
    "muscle gain": filter_muscle_gain,
    "diabetic": filter_diabetic,
}


def filter_by_goal(dataframe: pd.DataFrame, goal: str) -> pd.DataFrame:
    """
    Apply the appropriate goal-based filter to a food dataset.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Candidate food dataset.
    goal : str
        One of: "Weight Loss", "Maintenance", "Muscle Gain", "Diabetic"
        (case-insensitive).

    Returns
    -------
    pd.DataFrame
        Filtered subset matching the goal's criteria. If the filter
        yields an empty result, the original (unfiltered) dataframe
        is returned as a graceful fallback so downstream stages still
        have candidates to work with.

    Raises
    ------
    ValueError
        If goal is not one of the recognized options, or if the
        dataframe is missing required columns.
    """
    validate_required_columns(dataframe, REQUIRED_COLUMNS)
    normalized_goal = validate_goal(goal, VALID_GOALS)

    filter_function = _GOAL_FILTER_MAP[normalized_goal]
    filtered = filter_function(dataframe)

    if filtered.empty:
        return dataframe.reset_index(drop=True)

    return filtered


def get_goal_summary(goal: str) -> Dict[str, str]:
    """
    Return a human-readable description of a goal's filtering rules.

    Parameters
    ----------
    goal : str
        One of the valid dietary goals (case-insensitive).

    Returns
    -------
    dict
        Dictionary with 'goal' and 'rules' description keys.

    Raises
    ------
    ValueError
        If goal is not recognized.
    """
    normalized_goal = validate_goal(goal, VALID_GOALS)

    descriptions = {
        "weight loss": "Low Calories, High Protein, Low Fat, Low Sugar, High Fiber",
        "maintenance": "Balanced Nutrition across Calories, Protein, and Fat",
        "muscle gain": "High Protein, High Calories, Moderate Fat",
        "diabetic": "Low Sugar, High Fiber, Moderate Carbohydrates",
    }

    return {"goal": normalized_goal, "rules": descriptions[normalized_goal]}


# ------------------------------------------------------------------
# Example usage / smoke test
# ------------------------------------------------------------------
if __name__ == "__main__":
    sample_df = pd.DataFrame({
        "food": ["Chicken Breast", "White Rice", "Almonds", "Broccoli", "Soda"],
        "Caloric Value": [165, 130, 579, 34, 150],
        "Protein": [31.0, 2.7, 21.2, 2.8, 0.0],
        "Fat": [3.6, 0.3, 49.9, 0.4, 0.0],
        "Carbohydrates": [0.0, 28.0, 21.6, 6.6, 39.0],
        "Dietary Fiber": [0.0, 0.4, 12.5, 2.6, 0.0],
        "Sugars": [0.0, 0.1, 4.4, 1.7, 39.0],
    })

    for goal_name in VALID_GOALS:
        try:
            summary = get_goal_summary(goal_name)
            filtered_result = filter_by_goal(sample_df, goal_name)
            print(f"\nGoal: {summary['goal']} ({summary['rules']})")
            print(filtered_result[["food", "Caloric Value", "Protein"]].to_string(index=False))
        except ValueError as error:
            print(f"Error filtering for goal '{goal_name}': {error}")
