# Manan Arora — Projects Workspace

Six independent AI, Data Science, and Python engineering projects built during my
first year of a BTech in AI & Data Science at Middlesex University Dubai.

---

## 🚀 Projects

| Project | What it does | Main tech |
| :--- | :--- | :--- |
| 🔒 **[AI Toolkit Hub](./AI%20Toolkit%20Hub)** | Multi-page Streamlit dashboard with bcrypt/JWT auth, SQLite-backed incident and ticket data, and an LLM assistant. ~1,700 lines across models / services / pages. | Streamlit, SQLite, OpenAI API, Plotly, bcrypt, PyJWT |
| 🎬 **[CineScore](./CineScore%20Movie%20Rating%20Predictor)** | Compares three regression pipelines predicting IMDb ratings from pre-release metadata, using frequency encoding for high-cardinality features. | scikit-learn, pandas, matplotlib |
| 🔍 **[CrimeScope](./CrimeScope)** | Statistical analysis of 24 months of UK Metropolitan Police street crime — temporal trends, category distributions, normal PDF modelling. | pandas, SciPy, matplotlib |
| 🗺️ **[PathFinder](./PathFinder)** | Object-oriented Dijkstra implementation over JSON graph models, with input validation and path reconstruction. | Python 3 stdlib |
| 👨‍🍳 **[SmartChef](./SmartChef%20Recipe%20Recommendation%20System)** | CLI recommender scoring recipes by ingredient overlap, dietary preference, and allergen exclusion. | pandas |
| 📅 **[DayFlow](./DayFlow)** | CLI task manager with priorities, categories, due dates and JSON persistence. Cleanest module separation of the six. | Python 3 stdlib |

Each project has its own README with setup steps, results, and known limitations.

---

## 🛠️ Setup

Each project is independent and has its own `requirements.txt`. Create one shared
virtual environment at the workspace root:

```bash
cd path/to/projects          # wherever you cloned this
python3 -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
```

Then install whichever project you want to run:

```bash
cd "AI Toolkit Hub" && pip install -r requirements.txt
```

**Python 3.10+** is recommended. DayFlow and PathFinder need no third-party
packages at all.

---

## 📦 Datasets are not in this repository

Three large data files are deliberately **not** tracked by git:

| Project | File | Size | Where to get it |
| :--- | :--- | :--- | :--- |
| CrimeScope | `20XX-XX/*.csv` (24 months) | ~500 MB | [data.police.uk/data](https://data.police.uk/data/) — Metropolitan Police, Aug 2023–Jul 2025 |
| CrimeScope | `*.zip` archive | 95 MB | Same source, downloaded as a single archive |
| SmartChef | `recipes_final.csv` | 27 MB | ⚠️ Not currently reproducible — see that project's README |

GitHub rejects files over 100 MB, and nobody should have to clone half a gigabyte
of CSVs to read a 300-line script. CineScore's `imdb_top_1000.csv` is small enough
to keep in the repo.

---

## 🔐 Secrets

No API keys are stored in this repository. AI Toolkit Hub reads its keys from
`.streamlit/secrets.toml`, which is gitignored — copy
`.streamlit/secrets.toml.example` and fill in your own values. See that project's
README for details.

---

## 📝 Notes

- `FIXES.md` documents a security and repository-hygiene pass carried out on
  9 August 2026, including what was changed and why.
- CineScore and PathFinder were originally submitted as university coursework
  (Middlesex CST1450 / Assessment 2). The remaining four were self-directed.

---

## 👨‍💻 Author

**Manan Arora** — BTech AI & Data Science, Middlesex University Dubai
[mananarora836@gmail.com](mailto:mananarora836@gmail.com)
