"""
Description:
Calculates daily nutritional requirements
based on Total Daily Energy Expenditure (TDEE).

Nutrition Split:
Carbohydrates : 50%
Protein       : 20%
Fat           : 30%
"""

# ==========================================
# Nutrition Calculator
# ==========================================

def calculate_nutrition(tdee):
    """
    Calculate daily nutrition requirements.

    Parameters
    ----------
    tdee : float
        Total Daily Energy Expenditure

    Returns
    -------
    dict
        Calories
        Protein
        Fat
        Carbohydrates
    """

    if tdee <= 0:
        raise ValueError("TDEE must be greater than zero.")

    # Calories allocated to each macronutrient
    protein_calories = tdee * 0.20
    fat_calories = tdee * 0.30
    carb_calories = tdee * 0.50

    # Convert calories to grams
    protein = protein_calories / 4
    fat = fat_calories / 9
    carbohydrates = carb_calories / 4

    return {
        "Calories": round(tdee, 2),
        "Protein (g)": round(protein, 2),
        "Fat (g)": round(fat, 2),
        "Carbohydrates (g)": round(carbohydrates, 2)
    }


# ==========================================
# Display Nutrition Report
# ==========================================

def nutrition_report(tdee):

    result = calculate_nutrition(tdee)

    print("\n========== DAILY NUTRITION ==========")
    print(f"Calories       : {result['Calories']} kcal")
    print(f"Protein        : {result['Protein (g)']} g")
    print(f"Fat            : {result['Fat (g)']} g")
    print(f"Carbohydrates  : {result['Carbohydrates (g)']} g")
    print("=" * 38)

    return result


# ==========================================
# Main Program
# ==========================================

if __name__ == "__main__":

    print("=" * 50)
    print("AI Diet Recommendation System")
    print("Nutrition Requirement Calculator")
    print("=" * 50)

    try:

        tdee = float(input("Enter TDEE: "))

        nutrition_report(tdee)

    except ValueError as e:

        print("Error:", e)
