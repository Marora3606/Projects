# ============================================
# SMARTCHEF - Smart Recipe Recommendation System
# ============================================
"""Author: Manan Arora

Description: A Python-based recipe recommendation system that suggests
recipes based on user preferences, available ingredients, and allergies.

Features:
- Recipe recommendations
- Ingredient matching
- Allergy filtering
- Shopping list generation
"""

from pathlib import Path

import pandas as pd


PREFERENCES = {
    "1": "healthy",
    "2": "comfort food",
    "3": "vegetarian",
    "4": "vegan",
    "5": "high protein",
    "6": "surprise me",
    "7": "no preference",
}


# -----------------------------
# Load Recipe Dataset
# -----------------------------
def load_recipes():
    data_path = Path(__file__).resolve().parent / "recipes_final.csv"
    if not data_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {data_path}. Please put recipes_final.csv in the same folder as this script."
        )
    recipes = pd.read_csv(data_path, encoding="utf-8")

    def parse_ingredients(value):
        if pd.isna(value):
            return []
        if isinstance(value, list):
            return [str(item).strip().lower() for item in value]
        if isinstance(value, str):
            cleaned = value.replace("[", "").replace("]", "")
            parts = [part.strip() for part in cleaned.split(",") if part.strip()]
            return [part.strip().lower() for part in parts]
        return [str(value).strip().lower()]

    recipes["Cleaned_Ingredients"] = recipes["Cleaned_Ingredients"].apply(parse_ingredients)
    recipes["Instructions"] = recipes["Instructions"].fillna("")
    recipes["Category"] = recipes["Category"].fillna("")
    recipes["Title"] = recipes["Title"].fillna("Untitled Recipe")

    return recipes


# Load recipes once
recipes = load_recipes()


# -----------------------------
# User Profile Class
# -----------------------------
class UserProfile:
    def __init__(self, name, preference, allergies, available_ingredients):
        self.name = name
        self.preference = preference
        self.allergies = allergies
        self.available_ingredients = available_ingredients


# -----------------------------
# Create User Profile
# -----------------------------
def create_profile():
    print("\n========== SMARTCHEF ==========")
    name = input("Enter your name: ").strip()

    print("\nChoose your preference")
    for key, value in PREFERENCES.items():
        print(f"{key}. {value.title()}")

    choice = input("\nChoice: ").strip()
    preference = PREFERENCES.get(choice, "surprise me")

    allergies_input = input("\nEnter allergies (comma separated or press Enter): ").strip()
    allergies = [item.strip().lower() for item in allergies_input.split(",") if item.strip()]

    ingredients_input = input("\nEnter ingredients you have (comma separated): ").strip()
    ingredients = [item.strip().lower() for item in ingredients_input.split(",") if item.strip()]

    return UserProfile(name, preference, allergies, ingredients)


# -----------------------------
# Calculate Ingredient Match
# -----------------------------
def ingredient_match(user_ingredients, recipe_ingredients):
    """Calculate the percentage of recipe ingredients the user already has."""
    if not recipe_ingredients:
        return 0

    matches = sum(1 for ingredient in recipe_ingredients if ingredient in user_ingredients)
    score = (matches / len(recipe_ingredients)) * 100
    return round(score, 2)


# -----------------------------
# Allergy Checker
# -----------------------------
def contains_allergy(recipe_ingredients, allergies):
    allergy_set = {item.lower() for item in allergies}
    for ingredient in recipe_ingredients:
        if str(ingredient).lower() in allergy_set:
            return True
    return False


# -----------------------------
# Recommend Recipes
# -----------------------------
def recommend_recipes(user_profile):
    recommendations = []
    total_recipes = len(recipes)

    for _, recipe in recipes.iterrows():
        recipe_name = str(recipe["Title"])
        category_text = str(recipe["Category"]).lower()
        category_tags = [tag.strip().lower() for tag in category_text.split(",") if tag.strip()]
        recipe_ingredients = recipe["Cleaned_Ingredients"]
        instructions = str(recipe["Instructions"])

        if contains_allergy(recipe_ingredients, user_profile.allergies):
            continue

        if user_profile.preference not in {"surprise me", "no preference"}:
            if user_profile.preference not in category_tags:
                continue

        score = ingredient_match(user_profile.available_ingredients, recipe_ingredients)
        if (
            user_profile.preference not in {"surprise me", "no preference"}
            and user_profile.preference in category_tags
        ):
            score += 15
        score = min(score, 100)

        recommendations.append(
            {
                "title": recipe_name,
                "score": score,
                "ingredients": recipe_ingredients,
                "instructions": instructions,
                "category": category_text,
            }
        )

    recommendations.sort(key=lambda recipe: recipe["score"], reverse=True)
    return recommendations, total_recipes


# -----------------------------
# Display Results
# -----------------------------
def show_recommendations(user_profile, recommendations, total_recipes):
    filtered_count = len(recommendations)
    print(f"\n📊 Found {total_recipes} recipes.")
    print(f"After filtering allergies, {filtered_count} recipes remain.")

    if not recommendations:
        print("\nNo recipes matched your preferences.")
        print("Try changing your ingredients or selecting 'No Preference'.")
        return None

    print("\n🍽 Recommended Recipes")
    top_recommendations = recommendations[:5]

    for index, recipe in enumerate(top_recommendations, 1):
        print(f"\n{'=' * 37}")
        print(f"{index}. {recipe['title']}")
        print(f"Ingredient Match: {recipe['score']}%")
        print(f"Category: {recipe['category'].title()}")

    try:
        choice = int(input("\nChoose a recipe: "))
    except (ValueError, EOFError):
        print("Please enter a number.")
        return None

    if 1 <= choice <= len(top_recommendations):
        selected_recipe = top_recommendations[choice - 1]
        print(f"\n{'=' * 37}")
        print(f"🍽 {selected_recipe['title']}")

        matching = sum(
            1
            for ingredient in selected_recipe["ingredients"]
            if ingredient in user_profile.available_ingredients
        )
        total = len(selected_recipe["ingredients"])
        print(f"\nYou already have {matching}/{total} ingredients.")

        print("\nIngredients:")
        for ingredient in selected_recipe["ingredients"]:
            print(f"• {ingredient.title()}")
        print("\nInstructions:")
        print(selected_recipe["instructions"])

        print(f"\n🛒 Shopping List")
        shopping_list = [
            ingredient for ingredient in selected_recipe["ingredients"]
            if ingredient not in user_profile.available_ingredients
        ]
        if shopping_list:
            for ingredient in shopping_list:
                print(f"• {ingredient}")
        else:
            print("You already have everything needed for this recipe.")

        return selected_recipe

    print("Please choose a valid recipe number.")
    return None


# -----------------------------
# Main Program
# -----------------------------
def main():
    print("👋 Welcome to SMARTCHEF!")
    user_profile = create_profile()
    print(f"\n👋 Welcome {user_profile.name}!")

    recommendations, total_recipes = recommend_recipes(user_profile)
    show_recommendations(user_profile, recommendations, total_recipes)


if __name__ == "__main__":
    main()
