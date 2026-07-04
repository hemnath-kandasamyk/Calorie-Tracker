"""
BMI Calculator Module
AI Diet Recommendation System
"""

def calculate_bmi(weight_kg, height_cm):
    """
    Calculate Body Mass Index (BMI)

    Parameters:
        weight_kg (float): Weight in kilograms
        height_cm (float): Height in centimeters

    Returns:
        float: BMI value
    """

    height_m = height_cm / 100

    bmi = weight_kg / (height_m ** 2)

    return round(bmi, 2)
