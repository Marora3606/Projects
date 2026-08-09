# SmartChef — Recipe Recommendation System

A command-line recommender that ranks recipes by how well they match the
ingredients you already have, filtered by dietary preference and allergen
exclusions. Also generates a shopping list of what you are missing.

---

## 🌟 What it does

* 🥗 **Preference filtering** — healthy, comfort food, vegetarian, vegan, quick
  & easy, low carb, desserts, or no preference.
* 🍅 **Ingredient scoring** — compares your pantry against each recipe's
  ingredient list and computes a percentage match, used to rank results.
* ⚠️ **Allergen exclusion** — drops any recipe containing a listed allergen
  (nuts, gluten, dairy, seafood, and so on). Applied as a hard filter *before*
  scoring, so an unsafe recipe can never surface no matter how well it matches.
* 🛒 **Shopping list** — for a chosen recipe, lists the ingredients you do not
  have.
* 🧹 **Dataset preprocessing** — `clean_dataset.py` standardises raw recipe data
  into `recipes_final.csv`.

---

## 📦 Getting the data

**`recipes_final.csv` (27 MB, 58,782 recipes) is not tracked by git**, because
large data files bloat a repository and slow every clone.

> ⚠️ **The preprocessing step is not currently reproducible.**
> `clean_dataset.py` reads `recipes_edited.csv`, and that file is not in this
> project. Running the script as-is will fail with a `FileNotFoundError`.
>
> That makes the local `recipes_final.csv` the only copy — **back it up before
> relying on this**, and restore the raw source (or commit it, if it is small
> enough) so the pipeline can be run end to end again.

Once the raw file is restored:

```bash
python clean_dataset.py     # recipes_edited.csv -> recipes_final.csv
```

---

## 📁 Structure

```text
SmartChef Recipe Recommendation System/
├── recipe recommender.py   # Interactive CLI recommender
├── clean_dataset.py        # Preprocessing → recipes_final.csv
├── recipes_final.csv       # Cleaned dataset (~27 MB, gitignored)
├── requirements.txt
└── readme.md
```

---

## 🔧 Setup

```bash
cd "SmartChef Recipe Recommendation System"
pip install -r requirements.txt
python "recipe recommender.py"
```

`recipes_final.csv` must be present in this folder — see **Getting the data**
above.

**Dependencies:** pandas.

The program asks for your name, preference, allergies and available ingredients,
then prints ranked recommendations with match percentages.

---

## ⚠️ Known limitations

- **Matching is string-based.** `"tomato"` and `"tomatoes"` are treated as
  different ingredients, and `"chicken breast"` will not match `"chicken"`.
  Stemming, or an ingredient synonym table, would fix most of this.
- **Allergen detection is keyword-based**, so it can miss things. `"almond
  flour"` is caught by a `nuts` filter, but `"marzipan"` and `"frangipane"` are
  not. **This is a safety-relevant limitation and the recommender should not be
  relied on for real allergy decisions.**
- **The whole CSV is loaded into memory** on every run — fine at 27 MB, wasteful
  beyond that.
- **No persistence.** Preferences are re-entered every session.
- **Scoring ignores quantities** — having one of ten ingredients counts the same
  per-item as having nine.

---

## 👨‍💻 Author

**Manan Arora**
