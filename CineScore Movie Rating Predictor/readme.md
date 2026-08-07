# CineScore - Movie Rating Predictor

A machine learning regressor built in Python that predicts IMDb movie ratings using pre-release metadata and feature engineering techniques.

---

## 🌟 Key Features

* 📊 **Feature Selection:** Focuses on pre-release movie attributes (`Runtime`, `Director`, `Star1`, `Certificate`) to simulate real-world rating prediction prior to release.
* 🧹 **Data Preprocessing:** Cleans runtime string attributes (`'142 min'` → `142`), handles categorical values, and handles missing metadata.
* 📈 **Frequency Encoding:** Encodes high-cardinality categorical features (`Director` and `Star1`) based on mention frequencies to capture artist popularity without overfitting small datasets.
* ⚙️ **Multi-Model Pipeline Comparison:** Builds and evaluates three Scikit-learn pipelines:
  * **Ridge Regression** (L2 Regularization)
  * **Linear Regression** (Ordinary Least Squares)
  * **Random Forest Regressor** (Ensemble Trees with max depth constraints)
* 📉 **Performance Metrics:** Evaluates predictions using Coefficient of Determination ($R^2$) and Mean Absolute Error (MAE).

---

## 📁 Project Structure

```text
CineScore Movie Rating Predictor/
├── IMDB rating and movie prediction sytem.py  # Main ML script
├── imdb_top_1000.csv                           # IMDb Top 1000 dataset
├── requirements.txt                            # Python dependencies
└── readme.md                                   # Project documentation
```

---

## 🛠️ Setup & Installation

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Prediction Pipeline:**
   ```bash
   python "IMDB rating and movie prediction sytem.py"
   ```

---

## 📋 Requirements (`requirements.txt`)

* `pandas` - Data manipulation and CSV loading
* `numpy` - Numerical array operations
* `matplotlib` - Rating visualization and plot output
* `scikit-learn` - Pipeline preprocessing, feature transformers, regression models, and evaluation metrics

---

## 👨‍💻 Author

**Manan Arora**
