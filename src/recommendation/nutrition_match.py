"""
nutrition_match.py
========================================================
Project   : AI-Based Personalized Diet Recommendation System
Module    : recommendation.nutrition_match
Author    : Senior ML / Backend Engineering Team
Purpose   : Compare a user's nutrition requirements against each
            food's nutrition profile and compute a similarity score.
            Higher scores indicate a better match between what the
            user needs and what the food provides.
========================================================
"""

from __future__ import annotations

import pandas as pd

from recommendation_utils import (
    validate_positive_number,
    validate_required_columns,
    normalize_score,
)

# ------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------
REQUIRED_COLUMNS = ["food", "Caloric Value", "Protein", "Fat", "Carbohydrates"]

# Relative weighting applied to each macro's difference when computing
# the aggregate similarity score. Weights sum to 1.0. Protein is
# weighted most heavily since it is typically the primary axis for
# dietary goals (satiety, muscle preservation/gain).
DEFAULT_WEIGHTS = {
    "calories": 0.30,
    "protein": 0.35,
    "fat": 0.15,
    "carbohydrates": 0.20,
}


def calculate_macro_differences(
    dataframe: pd.DataFrame,
    required_calories: float,
    required_protein: float,
    required_fat: float,
    required_carbohydrates: float,
) -> pd.DataFrame:
    """
    Calculate the absolute difference between each food's macros and
    the user's required macros.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Food dataset containing macro columns.
    required_calories : float
        Target caloric value.
    required_protein : float
        Target protein (grams).
    required_fat : float
        Target fat (grams).
    required_carbohydrates : float
        Target carbohydrates (grams).

    Returns
    -------
    pd.DataFrame
        A copy of `dataframe` with four new columns appended:
        'Calories Difference', 'Protein Difference', 'Fat Difference',
        and 'Carbohydrates Difference'.

    Raises
    ------
    ValueError
        If any required target is not positive, or the dataframe is
        missing required columns.
    """
    validate_required_columns(dataframe, REQUIRED_COLUMNS)
    required_calories = validate_positive_number(required_calories, "required_calories")
    required_protein = validate_positive_number(required_protein, "required_protein")
    required_fat = validate_positive_number(required_fat, "required_fat")
    required_carbohydrates = validate_positive_number(
        required_carbohydrates, "required_carbohydrates"
    )

    result = dataframe.copy()
    result["Calories Difference"] = (result["Caloric Value"] - required_calories).abs()
    result["Protein Difference"] = (result["Protein"] - required_protein).abs()
    result["Fat Difference"] = (result["Fat"] - required_fat).abs()
    result["Carbohydrates Difference"] = (
        result["Carbohydrates"] - required_carbohydrates
    ).abs()

    return result


def calculate_similarity_score(
    dataframe: pd.DataFrame,
    required_calories: float,
    required_protein: float,
    required_fat: float,
    required_carbohydrates: float,
    weights: dict | None = None,
) -> pd.DataFrame:
    """
    Calculate a similarity score for each food, representing how
    closely its nutrition profile matches the user's requirements.

    The score is computed by:
      1. Calculating absolute differences per macro.
      2. Normalizing each difference column to a 0-1 range.
      3. Inverting the normalized difference (1 - normalized_diff) so
         that smaller differences yield higher scores.
      4. Combining the inverted scores using weighted averaging.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Food dataset containing macro columns.
    required_calories : float
        Target caloric value.
    required_protein : float
        Target protein (grams).
    required_fat : float
        Target fat (grams).
    required_carbohydrates : float
        Target carbohydrates (grams).
    weights : dict, optional
        Custom weighting for each macro's contribution to the final
        score. Keys must be 'calories', 'protein', 'fat',
        'carbohydrates' and values must sum to 1.0. Defaults to
        DEFAULT_WEIGHTS if not provided.

    Returns
    -------
    pd.DataFrame
        A copy of `dataframe` with difference columns and a new
        'Similarity Score' column (0-1 scale, higher = better match),
        sorted descending by score.

    Raises
    ------
    ValueError
        If weights are invalid (missing keys or don't sum to ~1.0).
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS
    else:
        expected_keys = set(DEFAULT_WEIGHTS.keys())
        if set(weights.keys()) != expected_keys:
            raise ValueError(f"weights must contain exactly these keys: {expected_keys}")
        if not abs(sum(weights.values()) - 1.0) < 1e-6:
            raise ValueError(f"weights must sum to 1.0, got {sum(weights.values())}")

    scored = calculate_macro_differences(
        dataframe, required_calories, required_protein, required_fat, required_carbohydrates
    )

    diff_columns = {
        "calories": "Calories Difference",
        "protein": "Protein Difference",
        "fat": "Fat Difference",
        "carbohydrates": "Carbohydrates Difference",
    }

    # Normalize each difference column and invert so lower difference
    # translates to a higher partial score.
    partial_scores = pd.DataFrame(index=scored.index)
    for key, column in diff_columns.items():
        col_min = scored[column].min()
        col_max = scored[column].max()
        if col_max == col_min:
            partial_scores[key] = 1.0  # All foods equally distant -> neutral best score.
        else:
            normalized = (scored[column] - col_min) / (col_max - col_min)
            partial_scores[key] = 1.0 - normalized

    scored["Similarity Score"] = sum(
        partial_scores[key] * weight for key, weight in weights.items()
    )

    return scored.sort_values(by="Similarity Score", ascending=False).reset_index(drop=True)


# ------------------------------------------------------------------
# Example usage / smoke test
# ------------------------------------------------------------------
if __name__ == "__main__":
    sample_df = pd.DataFrame({
        "food": ["Chicken Breast", "White Rice", "Almonds", "Broccoli"],
        "Caloric Value": [165, 130, 579, 34],
        "Protein": [31.0, 2.7, 21.2, 2.8],
        "Fat": [3.6, 0.3, 49.9, 0.4],
        "Carbohydrates": [0.0, 28.0, 21.6, 6.6],
    })

    try:
        scored_df = calculate_similarity_score(
            sample_df,
            required_calories=150,
            required_protein=25,
            required_fat=5,
            required_carbohydrates=10,
        )
        print(scored_df[["food", "Similarity Score"]].to_string(index=False))
    except ValueError as error:
        print(f"Similarity scoring failed: {error}")
