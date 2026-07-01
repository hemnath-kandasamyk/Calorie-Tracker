# 📊 Nutrition Datasets

This folder contains the nutrition datasets used for the **AI-Based Personalized Diet Recommendation System**.

These datasets serve as the primary data source for training and evaluating the machine learning models that predict nutritional values and recommend suitable food items based on user requirements.

---

# 📁 Dataset Files

| File Name              | Description                            |
| ---------------------- | -------------------------------------- |
| `FOOD-DATA-GROUP1.csv` | Nutrition information for Food Group 1 |
| `FOOD-DATA-GROUP2.csv` | Nutrition information for Food Group 2 |
| `FOOD-DATA-GROUP3.csv` | Nutrition information for Food Group 3 |
| `FOOD-DATA-GROUP4.csv` | Nutrition information for Food Group 4 |
| `FOOD-DATA-GROUP5.csv` | Nutrition information for Food Group 5 |

---

# 🎯 Purpose

The datasets are used to:

* Train machine learning models.
* Analyze nutritional composition of food items.
* Predict nutritional values.
* Support personalized food recommendations.
* Build a nutrition recommendation engine.

---

# 📋 Expected Dataset Information

The datasets may contain nutritional attributes such as:

* Food Name
* Food Category
* Calories
* Protein
* Carbohydrates
* Fat
* Fiber
* Sugar
* Water Content
* Cholesterol
* Sodium
* Potassium
* Calcium
* Iron
* Vitamins
* Minerals
* Serving Size

> **Note:** The available columns may vary between dataset groups.

---

# 🔄 Data Processing Workflow

The datasets are processed using the following pipeline:

1. Load all CSV files.
2. Merge all datasets into a single DataFrame.
3. Remove duplicate records.
4. Handle missing values.
5. Clean and standardize column names.
6. Perform exploratory data analysis (EDA).
7. Prepare features for machine learning.
8. Train and evaluate prediction models.

---

# 🤖 Machine Learning Usage

These datasets are used to train models for:

* Nutrition prediction
* Calorie estimation
* Protein analysis
* Food recommendation
* Personalized diet planning

Algorithms that may be used include:

* Linear Regression
* Decision Tree
* Random Forest
* Gradient Boosting
* XGBoost
* Extra Trees

---

# 📂 Loading the Datasets

```python
import pandas as pd

df1 = pd.read_csv("datasets/FOOD-DATA-GROUP1.csv")
df2 = pd.read_csv("datasets/FOOD-DATA-GROUP2.csv")
df3 = pd.read_csv("datasets/FOOD-DATA-GROUP3.csv")
df4 = pd.read_csv("datasets/FOOD-DATA-GROUP4.csv")
df5 = pd.read_csv("datasets/FOOD-DATA-GROUP5.csv")

df = pd.concat([df1, df2, df3, df4, df5], ignore_index=True)
```

---

# 📊 Applications

The combined dataset can be used for:

* AI Diet Recommendation Systems
* Nutrition Analytics
* Health Monitoring
* Personalized Meal Planning
* Machine Learning Projects
* Data Science Research
* Educational Purposes

---

# 📌 Notes

* Ensure all CSV files are placed inside the `datasets/` directory.
* Verify column names before training machine learning models.
* Perform preprocessing before feature selection and model training.
* Keep the original datasets unchanged to maintain data integrity.

---

# 🚀 Future Improvements

Future versions of the dataset may include:

* Micronutrient information
* Food images
* Regional food varieties
* Glycemic Index (GI)
* Glycemic Load (GL)
* User dietary preferences
* Medical condition tags
* Allergen information
* Meal categories (Breakfast, Lunch, Dinner, Snacks)

---

# 👨‍💻 Project

**AI-Based Personalized Diet Recommendation System using Machine Learning**

This dataset folder is part of the project's data layer and provides the nutritional information required for model development, testing, and personalized recommendation generation.
