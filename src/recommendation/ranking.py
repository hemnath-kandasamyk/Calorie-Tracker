"""
ranking.py
========================================================
Project   : AI-Based Personalized Diet Recommendation System
Module    : recommendation.ranking
Author    : Senior ML / Backend Engineering Team
Purpose   : Compute a final composite ranking score for each food,
            combining Nutrition Density, Protein, macro differences,
            Fiber, Sugar, and the pre-computed Similarity Score.
            Returns foods sorted by the final score (best first).
========================================================
"""

from __future__ import annotations

from typing import Dict, Optional

import pandas as pd

from recommendation_utils import validate_required_columns, safe_column_normalize

# ------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------
REQUIRED_COLUMNS = [
    "food",
    "Nutrition Density",
    "Protein",
    "Calories Difference",
    "Fat Difference",
    "Carbohydrates Difference",
    "Dietary Fiber",
    "Sugars",
    "Similarity Score",
]

# Default weighting for each ranking factor. Positive weights reward
# higher values (e.g. Nutrition Density, Protein, Fiber, Similarity
# Score); factors that represent "distance from target" are inverted
# before weighting so that smaller differences score higher.
DEFAULT_RANKING_WEIGHTS: Dict[str, float] = {
    "nutrition_density": 0.20,
    "protein": 0.15,
    "calories_difference": 0.15,
    "fat_difference": 0.10,
    "carbohydrates_difference": 0.10,
    "fiber": 0.10,
    "sugar": 0.10,
    "similarity_score": 0.10,
}

_FACTOR_TO_COLUMN = {
    "nutrition_density": "Nutrition Density",
    "protein": "Protein",
    "calories_difference": "Calories Difference",
    "fat_difference": "Fat Difference",
    "carbohydrates_difference": "Carbohydrates Difference",
    "fiber": "Dietary Fiber",
    "sugar": "Sugars",
    "similarity_score": "Similarity Score",
}

# Factors where a LOWER raw value is better (distances / sugar).
# Their normalized value is inverted (1 - normalized) before weighting.
_INVERT_FACTORS = {"calories_difference", "fat_difference", "carbohydrates_difference", "sugar"}


def _validate_weights(weights: Dict[str, float]) -> None:
    """
    Validate that a ranking weights dictionary is well-formed.

    Parameters
    ----------
    weights : dict
        Mapping of ranking factor name to weight.

    Raises
    ------
    ValueError
        If keys don't match expected factors or weights don't sum to 1.0.
    """
    expected_keys = set(DEFAULT_RANKING_WEIGHTS.keys())
    if set(weights.keys()) != expected_keys:
        raise ValueError(f"weights must contain exactly these keys: {expected_keys}")
    if not abs(sum(weights.values()) - 1.0) < 1e-6:
        raise ValueError(f"weights must sum to 1.0, got {sum(weights.values())}")


def calculate_final_score(
    dataframe: pd.DataFrame,
    weights: Optional[Dict[str, float]] = None,
) -> pd.DataFrame:
    """
    Compute a weighted composite 'Final Score' for each food.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Food dataset that already contains macro-difference columns
        (from nutrition_match.calculate_macro_differences) and a
        'Similarity Score' column (from
        nutrition_match.calculate_similarity_score).
    weights : dict, optional
        Custom weighting for each ranking factor. Keys must match
        DEFAULT_RANKING_WEIGHTS and values must sum to 1.0.

    Returns
    -------
    pd.DataFrame
        A copy of `dataframe` with a new 'Final Score' column
        (0-1 scale, higher = better).

    Raises
    ------
    ValueError
        If the dataframe is missing required columns, or if custom
        weights are invalid.
    """
    validate_required_columns(dataframe, REQUIRED_COLUMNS)

    if weights is None:
        weights = DEFAULT_RANKING_WEIGHTS
    else:
        _validate_weights(weights)

    scored = dataframe.copy()
    weighted_components = pd.DataFrame(index=scored.index)

    for factor, column in _FACTOR_TO_COLUMN.items():
        normalized = safe_column_normalize(scored, column)
        if factor in _INVERT_FACTORS:
            normalized = 1.0 - normalized
        weighted_components[factor] = normalized * weights[factor]

    scored["Final Score"] = weighted_components.sum(axis=1)
    return scored


def rank_foods(
    dataframe: pd.DataFrame,
    weights: Optional[Dict[str, float]] = None,
) -> pd.DataFrame:
    """
    Rank foods by their composite Final Score, best first.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Food dataset containing all columns required by
        `calculate_final_score`.
    weights : dict, optional
        Custom ranking weights. See `calculate_final_score`.

    Returns
    -------
    pd.DataFrame
        Foods sorted descending by 'Final Score', index reset.

    Raises
    ------
    ValueError
        If the dataframe is missing required columns or is empty.
    """
    if dataframe.empty:
        raise ValueError("Cannot rank an empty dataset.")

    scored = calculate_final_score(dataframe, weights)
    ranked = scored.sort_values(by="Final Score", ascending=False).reset_index(drop=True)
    return ranked


# ------------------------------------------------------------------
# Example usage / smoke test
# ------------------------------------------------------------------
if __name__ == "__main__":
    sample_df = pd.DataFrame({
        "food": ["Chicken Breast", "White Rice", "Almonds", "Broccoli"],
        "Nutrition Density": [88.7, 40.1, 60.1, 92.4],
        "Protein": [31.0, 2.7, 21.2, 2.8],
        "Calories Difference": [15.0, 20.0, 429.0, 116.0],
        "Fat Difference": [1.4, 4.7, 44.9, 4.6],
        "Carbohydrates Difference": [10.0, 18.0, 11.6, 3.4],
        "Dietary Fiber": [0.0, 0.4, 12.5, 2.6],
        "Sugars": [0.0, 0.1, 4.4, 1.7],
        "Similarity Score": [0.91, 0.55, 0.40, 0.72],
    })

    try:
        ranked_df = rank_foods(sample_df)
        print(ranked_df[["food", "Final Score"]].to_string(index=False))
    except ValueError as error:
        print(f"Ranking failed: {error}")
