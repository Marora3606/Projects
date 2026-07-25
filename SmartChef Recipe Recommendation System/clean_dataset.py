import pandas as pd

# Load the original dataset
recipes = pd.read_csv("recipes_edited.csv", encoding="utf-8")

# Words that indicate meat or seafood
non_vegan_words = [
    "chicken", "beef", "pork", "bacon", "ham", "turkey",
    "lamb", "fish", "salmon", "tuna", "shrimp", "prawn",
    "crab", "lobster", "sausage", "pepperoni", "anchovy",
    "duck", "goat", "veal", "mutton", "oyster", "clam",
    "mussel", "squid", "octopus"
]

# Words that indicate dairy or eggs
vegetarian_not_vegan = [
    "egg", "milk", "cheese", "butter", "cream",
    "yogurt", "yoghurt", "mayonnaise", "honey"
]


def fix_category(row):
    title = str(row["Title"]).lower()
    ingredients = str(row["Cleaned_Ingredients"]).lower()
    text = title + " " + ingredients

    categories = str(row["Category"]).lower()

    # Remove incorrect Vegan tag
    if "vegan" in categories:
        if any(word in text for word in non_vegan_words + vegetarian_not_vegan):
            categories = categories.replace("vegan", "")

    # Remove incorrect Vegetarian tag
    if "vegetarian" in categories:
        if any(word in text for word in non_vegan_words):
            categories = categories.replace("vegetarian", "")

    # Clean commas
    categories = ",".join(
        part.strip()
        for part in categories.split(",")
        if part.strip()
    )

    return categories


# Apply cleaning
recipes["Category"] = recipes.apply(fix_category, axis=1)

# Save cleaned dataset
recipes.to_csv("recipes_final.csv", index=False, encoding="utf-8")

print("Done!")
print("Saved as recipes_final.csv")