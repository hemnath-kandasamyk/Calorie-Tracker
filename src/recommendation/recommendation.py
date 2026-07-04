"""
=========================================================
AI Diet Recommendation System
Food Recommendation Engine
=========================================================
Description:
    This module recommends foods based on the
    user's nutritional requirements.

Version : 1.0

Recommendation Factors
----------------------
✓ Calories
✓ Protein
✓ Fat
✓ Carbohydrates
✓ Nutrition Density

Returns
-------
Top matching foods.
=========================================================
"""

import pandas as pd


# =====================================================
# Load Dataset
# =====================================================

def load_food_dataset(dataset_path):
    """
    Load processed food dataset.

    Parameters
    ----------
    dataset_path : str

    Returns
    -------
    pandas.DataFrame
    """

    try:

        df = pd.read_csv(dataset_path)

        print("✓ Food dataset loaded successfully.")

        return df

    except Exception as e:

        raise FileNotFoundError(e)


# =====================================================
# Food Recommendation
# =====================================================

def recommend_food(
    dataframe,
    target_calories,
    target_protein,
    target_fat,
    target_carbohydrates,
    calorie_tolerance=100
):
    """
    Recommend foods based on nutritional targets.

    Parameters
    ----------
    dataframe : DataFrame

    target_calories : float

    target_protein : float

    target_fat : float

    target_carbohydrates : float

    calorie_tolerance : int

    Returns
    -------
    DataFrame
    """

    recommendations = dataframe.copy()

    # -----------------------------------
    # Calories
    # -----------------------------------

    recommendations = recommendations[

        (recommendations["Caloric Value"] >=
         target_calories - calorie_tolerance)

        &

        (recommendations["Caloric Value"] <=
         target_calories + calorie_tolerance)

    ]

    # -----------------------------------
    # Protein
    # -----------------------------------

    recommendations = recommendations[

        recommendations["Protein"] >= target_protein * 0.70

    ]

    # -----------------------------------
    # Fat
    # -----------------------------------

    recommendations = recommendations[

        recommendations["Fat"] <= target_fat * 1.20

    ]

    # -----------------------------------
    # Carbohydrates
    # -----------------------------------

    recommendations = recommendations[

        recommendations["Carbohydrates"] <= target_carbohydrates * 1.20

    ]

    # -----------------------------------
    # Sort by Nutrition Density
    # -----------------------------------

    recommendations = recommendations.sort_values(

        by="Nutrition Density",

        ascending=False

    )

    return recommendations


# =====================================================
# Display Recommendations
# =====================================================

def display_recommendations(dataframe, top_n=10):
    """
    Display recommended foods.

    Parameters
    ----------
    dataframe : DataFrame

    top_n : int
    """

    if dataframe.empty:

        print("\nNo suitable foods found.")

        return

    columns = [

        "food",

        "Caloric Value",

        "Protein",

        "Fat",

        "Carbohydrates",

        "Dietary Fiber",

        "Sugars",

        "Nutrition Density"

    ]

    print("\n")
    print("=" * 70)
    print("TOP FOOD RECOMMENDATIONS")
    print("=" * 70)

    print(

        dataframe[columns]

        .head(top_n)

        .to_string(index=False)

    )

    print("=" * 70)


# =====================================================
# Main Program
# =====================================================

if __name__ == "__main__":

    print("=" * 60)
    print("AI Diet Recommendation System")
    print("Food Recommendation Engine")
    print("=" * 60)

    DATASET_PATH = "../../datasets/processed/processed_food_dataset.csv"

    food_df = load_food_dataset(DATASET_PATH)

    print("\nEnter Daily Nutrition Targets\n")

    calories = float(input("Calories (kcal): "))

    protein = float(input("Protein (g): "))

    fat = float(input("Fat (g): "))

    carbs = float(input("Carbohydrates (g): "))

    recommendations = recommend_food(

        dataframe=food_df,

        target_calories=calories,

        target_protein=protein,

        target_fat=fat,

        target_carbohydrates=carbs

    )

    display_recommendations(recommendations)
