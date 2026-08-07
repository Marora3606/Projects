# SmartChef - Recipe Recommendation System

A Python recommendation engine that suggests recipes based on user dietary preferences, available ingredients, and allergy exclusions.

---

## 🌟 Key Features

* 🥗 **Dietary Preference Filtering:** Filters recipes by preference (`Healthy`, `Comfort food`, `Vegetarian`, `Vegan`, `Quick & easy`, `Low carb`, `Desserts`).
* 🍅 **Ingredient Matching Engine:** Matches user-input pantry ingredients against recipe ingredient lists and calculates match scores.
* ⚠️ **Allergy Exclusion Filter:** Excludes recipes containing user-specified allergens (e.g. `nuts`, `gluten`, `dairy`, `seafood`).
* 🛒 **Shopping List Generation:** Identifies missing ingredients for selected recipes and exports a shopping list.
* 🧹 **Automated Dataset Cleaning:** Preprocesses raw recipe data via `clean_dataset.py` to standardize categories and ingredients into `recipes_final.csv`.

---

## 📁 Project Structure

```text
SmartChef Recipe Recommendation System/
├── recipe recommender.py  # Interactive CLI recommendation system
├── clean_dataset.py       # Dataset cleaning & category classification script
├── recipes_final.csv      # Cleaned recipes dataset (~26.8 MB)
├── requirements.txt       # Python dependencies
└── readme.md              # Project documentation
```

---

## 🛠️ Setup & Installation

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run SmartChef:**
   ```bash
   python "recipe recommender.py"
   ```

3. *(Optional)* **Re-run Dataset Preprocessing:**
   ```bash
   python clean_dataset.py
   ```

---

## 📋 Requirements (`requirements.txt`)

* `pandas` - Data manipulation, CSV parsing, ingredient filtering, and keyword processing

---

## 👨‍💻 Author

**Manan Arora**
