# CineScore — Movie Rating Predictor

Compares three regression pipelines that predict a film's IMDb rating from
**pre-release metadata only** — runtime, certificate, director and lead actor.
No post-release signals such as vote counts or box office are used, so the setup
mirrors what you would actually know before a film comes out.

Built on the IMDb Top 1000 dataset.

---

## 🌟 What it does

* 🎯 **Pre-release feature selection** — `Runtime`, `Certificate`, `Director`,
  `Star1`. Deliberately excludes anything only knowable after release, which
  would leak the target.
* 🧹 **Preprocessing** — parses `"142 min"` → `142`, handles missing
  certificates, one-hot encodes `Certificate`.
* 📈 **Frequency encoding** for `Director` and `Star1`. These are
  high-cardinality (hundreds of distinct values), so one-hot encoding would
  create hundreds of sparse columns on only 1,000 rows. Encoding each name by
  how often it appears captures "star power" in a single numeric feature.
* ⚙️ **Three pipelines compared** — Ridge (L2, `alpha=1.0`), ordinary Linear
  Regression, and Random Forest (`n_estimators=100`, `max_depth=5` to limit
  overfitting).
* 📊 **Evaluation** — R² and MAE on a held-out 20% test split
  (`random_state=42`), plus a worked prediction for a hypothetical film.

---

## 📉 Results — and why they look the way they do

| Model | R² | MAE |
| :--- | ---: | ---: |
| Linear Regression | 0.056 | 0.204 |
| Ridge Regression | 0.044 | 0.205 |
| Random Forest | **−0.035** | 0.207 |

**These are poor R² scores, and that is the interesting part of the project.**

R² measures how much variance the model explains relative to simply predicting
the mean every time. A negative R² — as Random Forest produces here — means the
model performs *worse than the mean baseline*.

The cause is the dataset, not the pipeline. The IMDb Top 1000 is pre-filtered to
highly rated films, so ratings cluster between 7.6 and 9.3. There is very little
variance to explain, and pre-release metadata explains almost none of the little
that exists. MAE tells the complementary story: predictions are off by only ~0.2
rating points on average, which sounds good until you realise that guessing the
mean does nearly as well.

**The conclusion the project actually supports:** runtime, certificate, director
and lead actor are weak predictors of rating *within an already-acclaimed set of
films*. Testing this on a full IMDb sample with genuine rating spread would be
the natural next step.

Reporting a model that barely beats the baseline, and explaining why, is more
useful than tuning until a number looks good.

---

## 📁 Structure

```text
CineScore Movie Rating Predictor/
├── IMDB rating and movie prediction sytem.py   # Full pipeline
├── imdb_top_1000.csv                           # Dataset (1,000 rows)
├── requirements.txt
└── readme.md
```

---

## 🔧 Setup

```bash
cd "CineScore Movie Rating Predictor"
pip install -r requirements.txt
python "IMDB rating and movie prediction sytem.py"
```

Prints the metrics table, a prediction for a hypothetical film, a list of
similar films from the dataset, and opens comparison plots.

**Dependencies:** pandas, numpy, matplotlib, scikit-learn.

---

## ⚠️ Known limitations

- **Dataset is pre-filtered**, which caps achievable R². See above.
- **Frequency encoding leaks slightly.** Frequencies are computed over the whole
  dataset before the train/test split, so test-set rows contribute to their own
  encodings. Computing them on the training fold only would be more rigorous.
- **No cross-validation.** A single 80/20 split on 1,000 rows makes metrics
  sensitive to which rows landed where. K-fold would give a more stable estimate.
- **No hyperparameter search.** Ridge `alpha` and the forest depth were chosen by
  hand, not tuned.
- **Genre is unused**, despite being available and plausibly predictive.

---

## 📝 Context

Originally submitted as university coursework (Assessment 2, Middlesex
University Dubai).

---

## 👨‍💻 Author

**Manan Arora**
