# 🥗 AI Diet Recommendation System

An AI-powered Diet Recommendation System that generates personalized nutrition and meal recommendations based on a user's health profile, body metrics, activity level, and nutritional requirements.

This project combines **Machine Learning**, **Nutrition Science**, and **Web Technologies** to recommend healthy foods and balanced meal plans.

---

# 📖 Table of Contents

- Project Overview
- Features
- Project Architecture
- Folder Structure
- Machine Learning Models
- Technologies Used
- Installation
- Usage
- Project Workflow
- Future Improvements
- Contributors
- License

---

# 🚀 Project Overview

The AI Diet Recommendation System helps users:

- Calculate Body Mass Index (BMI)
- Calculate Basal Metabolic Rate (BMR)
- Calculate Total Daily Energy Expenditure (TDEE)
- Generate Daily Nutrition Requirements
- Recommend Healthy Foods
- Create Personalized Meal Plans
- Provide AI-assisted Nutrition Recommendations

The recommendation engine uses processed food datasets together with user health information to generate customized diet plans.

---

# ✨ Features

## Health Analysis

- ✅ BMI Calculator
- ✅ BMI Classification
- ✅ BMR Calculator
- ✅ TDEE Calculator
- ✅ Daily Nutrition Calculator

## AI Recommendation Engine

- ✅ Food Recommendation
- ✅ Goal-Based Food Filtering
- ✅ Nutrition Matching
- ✅ Food Ranking
- ✅ Meal Planning

## Machine Learning

- ✅ Linear Regression
- ✅ Decision Tree Regressor
- ✅ Random Forest Regressor
- ✅ Gradient Boosting Regressor
- ✅ Extra Trees Regressor

## Data Processing

- ✅ Data Cleaning
- ✅ Data Preprocessing
- ✅ Duplicate Removal
- ✅ Missing Value Handling
- ✅ Feature Selection

---

# 🏗 Project Architecture

```text
                    User
                      │
                      ▼
            Enter Health Details
                      │
                      ▼
               BMI Calculator
                      │
                      ▼
               BMR Calculator
                      │
                      ▼
              TDEE Calculator
                      │
                      ▼
        Daily Nutrition Requirement
                      │
                      ▼
          Food Recommendation Engine
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
     Food Filtering          Nutrition Matching
          │                       │
          └───────────┬───────────┘
                      ▼
                Food Ranking
                      ▼
               Meal Planner
                      ▼
         Personalized Diet Plan
```

---

# 📂 Project Structure

```text
AI-Diet-Recommendation-System/

│
├── backend/
│
│   ├── app.py
│
│   ├── health/
│   │   ├── bmi.py
│   │   ├── bmr.py
│   │   ├── tdee.py
│   │   └── nutrition.py
│   │
│   ├── recommendation/
│   │   ├── recommendation.py
│   │   ├── food_filter.py
│   │   ├── nutrition_match.py
│   │   ├── ranking.py
│   │   ├── meal_planner.py
│   │   └── recommendation_utils.py
│   │
│   ├── models/
│   │   ├── linear_regression_model.pkl
│   │   ├── decision_tree_model.pkl
│   │   ├── random_forest_model.pkl
│   │   ├── gradient_boosting_model.pkl
│   │   └── extra_trees_model.pkl
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── assets/
│
├── datasets/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│
├── diagrams/
│
├── README.md
│
└── LICENSE
```

---

# 🤖 Machine Learning Models

The project evaluates multiple regression models to determine the best predictor for nutritional recommendations.

| Model | Purpose |
|--------|----------|
| Linear Regression | Baseline regression model |
| Decision Tree | Non-linear prediction |
| Random Forest | Ensemble learning |
| Gradient Boosting | Boosted regression |
| Extra Trees | Randomized ensemble model |

Each model is trained, evaluated, and stored as a `.pkl` file for later integration into the recommendation engine.

---

# 📊 Datasets Used

### 🍎 Food Nutrition Dataset

Contains nutritional information including:

- Calories
- Protein
- Fat
- Carbohydrates
- Fiber
- Sugar
- Vitamins
- Minerals
- Nutrition Density

---

### 💪 Body Fat Dataset

Contains:

- Age
- Height
- Weight
- Body Fat
- Body Measurements

---

### ❤️ Healthy Lifestyle Dataset

Contains:

- Age
- Gender
- Height
- Weight
- BMI
- Smoking Status
- Exercise Frequency
- Diet Quality
- Alcohol Consumption

---

# ⚙ Technologies Used

## Programming

- Python
- HTML5
- CSS3
- JavaScript

## Machine Learning

- Scikit-learn
- Pandas
- NumPy
- Joblib

## Visualization

- Matplotlib

## Backend

- FastAPI *(Planned)*

## Version Control

- Git
- GitHub

---

# 📈 Project Workflow

```text
Raw Datasets
      │
      ▼
Data Cleaning
      │
      ▼
Data Preprocessing
      │
      ▼
Feature Selection
      │
      ▼
Machine Learning Models
      │
      ▼
Health Calculations
(BMI, BMR, TDEE)
      │
      ▼
Nutrition Requirement
      │
      ▼
Recommendation Engine
      │
      ▼
Meal Planner
      │
      ▼
Web Application
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/your-username/AI-Diet-Recommendation-System.git
```

Move into the project

```bash
cd AI-Diet-Recommendation-System
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r backend/requirements.txt
```

---

# ▶ Usage

Run the application

```bash
python backend/app.py
```

*(When the FastAPI backend is complete, this command may change to start the API server.)*

---

# 🎯 Future Improvements

- User Authentication
- User Profiles
- Progress Tracking
- AI Chat Assistant
- Weekly Meal Planner
- Grocery List Generator
- Nutrition Dashboard
- Mobile Application
- Cloud Deployment
- Wearable Device Integration

---

# 📌 Project Status

| Phase | Status |
|--------|--------|
| Data Collection | ✅ Completed |
| Data Preprocessing | ✅ Completed |
| Machine Learning Models | ✅ Completed |
| Health Modules | ✅ Completed |
| Recommendation Engine | ✅ Completed |
| Meal Planner | ✅ Completed |
| Backend Integration | 🚧 In Progress |
| Frontend Development | 🚧 In Progress |
| Deployment | ⏳ Planned |

---

# 👨‍💻 Author

**Hemnath K**

B.Tech – Artificial Intelligence and Data Science

Final Year Machine Learning Project

---

# 📄 License

This project is licensed under the MIT License.

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
