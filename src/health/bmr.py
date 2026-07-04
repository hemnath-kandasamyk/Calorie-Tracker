# ==========================================
# BMR CALCULATOR
# ==========================================

def calculate_bmr(age, gender, weight_kg, height_cm):
    """
    Calculate Basal Metabolic Rate (BMR)

    Parameters
    ----------
    age : int
    gender : str
        Male / Female
    weight_kg : float
    height_cm : float

    Returns
    -------
    float
        BMR
    """

    gender = gender.lower()

    if weight_kg <= 0:
        raise ValueError("Weight must be greater than zero.")

    if height_cm <= 0:
        raise ValueError("Height must be greater than zero.")

    if age <= 0:
        raise ValueError("Age must be greater than zero.")

    if gender == "male":

        bmr = (
            10 * weight_kg
            + 6.25 * height_cm
            - 5 * age
            + 5
        )

    elif gender == "female":

        bmr = (
            10 * weight_kg
            + 6.25 * height_cm
            - 5 * age
            - 161
        )

    else:
        raise ValueError("Gender must be Male or Female.")

    return round(bmr, 2)


# ==========================================
# COMPLETE BMR REPORT
# ==========================================

def bmr_analysis(age, gender, weight_kg, height_cm):

    bmr = calculate_bmr(
        age,
        gender,
        weight_kg,
        height_cm
    )

    result = {
        "Age": age,
        "Gender": gender,
        "Weight": weight_kg,
        "Height": height_cm,
        "BMR": bmr
    }

    return result


# ==========================================
# MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    print("=" * 50)
    print("AI Diet Recommendation System")
    print("BMR Calculator")
    print("=" * 50)

    try:

        age = int(input("Enter Age: "))
        gender = input("Enter Gender (Male/Female): ")

        weight = float(input("Enter Weight (kg): "))
        height = float(input("Enter Height (cm): "))

        result = bmr_analysis(
            age,
            gender,
            weight,
            height
        )

        print("\n========== BMR REPORT ==========")

        print(f"Age      : {result['Age']}")
        print(f"Gender   : {result['Gender']}")
        print(f"Weight   : {result['Weight']} kg")
        print(f"Height   : {result['Height']} cm")
        print(f"BMR      : {result['BMR']} Calories/day")

        print("=" * 35)

    except ValueError as e:
        print("Error:", e)
