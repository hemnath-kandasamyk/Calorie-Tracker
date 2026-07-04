"""
meal_planner.py
========================================================
Project   : AI-Based Personalized Diet Recommendation System
Module    : recommendation.meal_planner
Author    : Senior ML / Backend Engineering Team
Purpose   : Divide a ranked list of recommended foods into a daily
            meal plan (Breakfast, Lunch, Dinner, Snacks), distributing
            the user's total daily calorie target across meals and
            assigning foods whose caloric value fits each meal slot.
========================================================
"""

from __future__ import annotations

from typing import Dict

import pandas as pd

from recommendation_utils import (
    validate_positive_number,
    validate_required_columns,
    calculate_percentage,
)

# ------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------
REQUIRED_COLUMNS = ["food", "Caloric Value", "Protein", "Fat", "Carbohydrates"]

# Default calorie distribution across meals. Values must sum to 1.0.
MEAL_CALORIE_DISTRIBUTION: Dict[str, float] = {
    "breakfast": 0.25,
    "lunch": 0.35,
    "dinner": 0.30,
    "snacks": 0.10,
}

# Tolerance band applied when matching a food's calories to a meal's
# calorie budget (fraction of the meal target).
MEAL_CALORIE_TOLERANCE = 0.40

# Maximum number of food items to assign per meal.
MAX_ITEMS_PER_MEAL = 4


def _validate_distribution(distribution: Dict[str, float]) -> None:
    """
    Validate a meal calorie distribution dictionary.

    Parameters
    ----------
    distribution : dict
        Mapping of meal name to fractional share of daily calories.

    Raises
    ------
    ValueError
        If the distribution values do not sum to 1.0, or contains
        non-positive shares.
    """
    if not distribution:
        raise ValueError("distribution must not be empty.")
    if any(share <= 0 for share in distribution.values()):
        raise ValueError("All meal distribution shares must be positive.")
    if not abs(sum(distribution.values()) - 1.0) < 1e-6:
        raise ValueError(
            f"Meal distribution shares must sum to 1.0, got {sum(distribution.values())}"
        )


def calculate_meal_targets(
    total_daily_calories: float,
    distribution: Dict[str, float] = None,
) -> Dict[str, float]:
    """
    Calculate the target calorie budget for each meal.

    Parameters
    ----------
    total_daily_calories : float
        The user's total required daily calories (from TDEE / goal
        adjustment).
    distribution : dict, optional
        Mapping of meal name to fractional share (must sum to 1.0).
        Defaults to MEAL_CALORIE_DISTRIBUTION.

    Returns
    -------
    dict
        Mapping of meal name to target calories for that meal.

    Raises
    ------
    ValueError
        If total_daily_calories is not positive or distribution is
        invalid.
    """
    total_daily_calories = validate_positive_number(
        total_daily_calories, "total_daily_calories"
    )
    if distribution is None:
        distribution = MEAL_CALORIE_DISTRIBUTION
    _validate_distribution(distribution)

    return {
        meal: round(total_daily_calories * share, 2)
        for meal, share in distribution.items()
    }


def _assign_foods_to_meal(
    dataframe: pd.DataFrame,
    target_calories: float,
    max_items: int = MAX_ITEMS_PER_MEAL,
) -> pd.DataFrame:
    """
    Select foods from a ranked dataset that fit within a meal's
    calorie budget.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Ranked food dataset (expects best candidates first).
    target_calories : float
        Calorie budget for this meal.
    max_items : int, optional
        Maximum number of items to select for this meal.

    Returns
    -------
    pd.DataFrame
        Subset of `dataframe` assigned to the meal, best-ranked first.
    """
    lower_bound = target_calories * (1 - MEAL_CALORIE_TOLERANCE)
    upper_bound = target_calories * (1 + MEAL_CALORIE_TOLERANCE)

    candidates = dataframe[
        dataframe["Caloric Value"].between(max(lower_bound, 0), upper_bound)
    ]

    if candidates.empty:
        # Fallback: pick the closest-calorie foods available so the
        # meal slot is never left completely empty.
        candidates = dataframe.assign(
            _cal_gap=(dataframe["Caloric Value"] - target_calories).abs()
        ).sort_values(by="_cal_gap").drop(columns="_cal_gap")

    return candidates.head(max_items).reset_index(drop=True)


def plan_meals(
    ranked_foods: pd.DataFrame,
    total_daily_calories: float,
    distribution: Dict[str, float] = None,
) -> Dict[str, Dict[str, object]]:
    """
    Build a full daily meal plan from a ranked food dataset.

    Parameters
    ----------
    ranked_foods : pd.DataFrame
        Foods ranked best-first (e.g. output of ranking.rank_foods).
    total_daily_calories : float
        The user's total required daily calories.
    distribution : dict, optional
        Custom meal calorie distribution. Defaults to
        MEAL_CALORIE_DISTRIBUTION (Breakfast 25%, Lunch 35%,
        Dinner 30%, Snacks 10%).

    Returns
    -------
    dict
        Dictionary keyed by meal name. Each value is itself a dict
        with keys:
          - 'target_calories': float, the calorie budget for the meal
          - 'target_percentage': float, percentage of daily calories
          - 'foods': pd.DataFrame, assigned foods for that meal

    Raises
    ------
    ValueError
        If ranked_foods is empty/missing columns, or
        total_daily_calories / distribution are invalid.
    """
    validate_required_columns(ranked_foods, REQUIRED_COLUMNS)
    if ranked_foods.empty:
        raise ValueError("ranked_foods must not be empty.")

    meal_targets = calculate_meal_targets(total_daily_calories, distribution)
    resolved_distribution = distribution or MEAL_CALORIE_DISTRIBUTION

    meal_plan: Dict[str, Dict[str, object]] = {}
    for meal_name, target_calories in meal_targets.items():
        assigned_foods = _assign_foods_to_meal(ranked_foods, target_calories)
        meal_plan[meal_name] = {
            "target_calories": target_calories,
            "target_percentage": calculate_percentage(
                resolved_distribution[meal_name] * 100, 100
            ),
            "foods": assigned_foods,
        }

    return meal_plan


# ------------------------------------------------------------------
# Example usage / smoke test
# ------------------------------------------------------------------
if __name__ == "__main__":
    sample_ranked_df = pd.DataFrame({
        "food": ["Oatmeal", "Grilled Chicken Salad", "Salmon & Rice",
                 "Greek Yogurt", "Almonds", "Steamed Broccoli"],
        "Caloric Value": [150, 350, 620, 100, 200, 55],
        "Protein": [5.0, 35.0, 40.0, 10.0, 7.5, 4.0],
        "Fat": [3.0, 12.0, 22.0, 2.0, 17.0, 0.6],
        "Carbohydrates": [27.0, 15.0, 45.0, 6.0, 7.5, 11.0],
    })

    try:
        plan = plan_meals(sample_ranked_df, total_daily_calories=2000)
        for meal, details in plan.items():
            print(f"\n{meal.upper()} (target: {details['target_calories']} kcal, "
                  f"{details['target_percentage']:.0f}% of daily calories)")
            print(details["foods"][["food", "Caloric Value", "Protein"]].to_string(index=False))
    except ValueError as error:
        print(f"Meal planning failed: {error}")
