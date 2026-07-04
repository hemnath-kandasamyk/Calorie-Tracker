"""
=========================================
AI Diet Recommendation System
TDEE Calculator Module
=========================================

Author : Hemnath

Description:
    Calculates Total Daily Energy Expenditure (TDEE)
    using BMR and Activity Level.
"""

# ==========================================
# Activity Multipliers
# ==========================================

ACTIVITY_LEVELS = {
    "sedentary": 1.20,
    "lightly active": 1.375,
    "moderately active": 1.55,
    "very active": 1.725,
    "extra active": 1.90
}


# ==========================================
# TDEE Calculator
# ==========================================

def calculate_tdee(bmr, activity_level):
    """
    Calculate Total Daily Energy Expenditure (TDEE)

    Parameters
    ----------
    bmr : float
        Basal Metabolic Rate

    activity_level : str
        sedentary
        lightly active
        moderately active
        very active
        extra active

    Returns
    -------
    float
        TDEE
    """

    if bmr <= 0:
        raise ValueError("BMR must be greater than zero.")

    activity_level = activity_level.lower()

    if activity_level not in ACTIVITY_LEVELS:
        raise ValueError(
            "Invalid activity level.\n"
            "Choose from:\n"
            "- Sedentary\n"
            "- Lightly Active\n"
            "- Moderately Active\n"
            "- Very Active\n"
            "- Extra Active"
        )

    multiplier = ACTIVITY_LEVELS[activity_level]

    tdee = bmr * multiplier

    return round(tdee, 2)


# ==========================================
# Complete TDEE Report
# ==========================================

def tdee_analysis(bmr, activity_level):

    tdee = calculate_tdee(bmr, activity_level)

    result = {
        "BMR": bmr,
        "Activity Level": activity_level.title(),
        "TDEE": tdee
    }

    return result


# ==========================================
# Main Program
# ==========================================

if __name__ == "__main__":

    print("=" * 50)
    print("AI Diet Recommendation System")
    print("TDEE Calculator")
    print("=" * 50)

    try:

        bmr = float(input("Enter BMR: "))

        print("\nActivity Levels")
        print("----------------------")
        print("Sedentary")
        print("Lightly Active")
        print("Moderately Active")
        print("Very Active")
        print("Extra Active")

        activity = input("\nEnter Activity Level: ")

        result = tdee_analysis(
            bmr,
            activity
        )

        print("\n========== TDEE REPORT ==========")

        print(f"BMR             : {result['BMR']} Calories/day")
        print(f"Activity Level  : {result['Activity Level']}")
        print(f"TDEE            : {result['TDEE']} Calories/day")

        print("=" * 35)

    except ValueError as e:
        print("Error:", e)
