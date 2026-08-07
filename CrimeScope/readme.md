# CrimeScope - Crime Data Analysis & Knowledge Representation

A Python-based data analysis and statistical visualization project that analyzes UK police crime data across monthly archives to identify temporal trends, category distributions, and statistical normal probability density functions.

---

## 🌟 Key Features

* 📦 **Automated Archive Extraction:** Automatically locates and extracts monthly crime CSV archives (`.zip`) across multiple year-month directories.
* 🧹 **Data Aggregation & Cleaning:** Combines multi-month CSV records into unified Pandas DataFrames while handling missing location coordinates and unclassified categories.
* 📈 **Temporal Trend Analysis:** Computes monthly crime counts and plots time-series evolution over multi-year periods.
* 📊 **Categorical Breakdown:** Aggregates crime distribution by type (e.g., Anti-social behaviour, Burglary, Violent crime) and visualizes frequency distributions.
* 📐 **Statistical Modeling:** Uses `SciPy` normal distributions (`scipy.stats.norm`) to model crime rate probability density functions.

---

## 📁 Project Structure

```text
CrimeScope/
├── Crime Data Analysis & Knowledge Representation.py  # Main data processing script
├── 27d1328a9d866c8330c411a3a9e5b517314b8bea.zip         # Raw crime dataset archive
├── q1c_graph1_time.png                                 # Output: Temporal trend plot
├── q1c_graph2_crime_types.png                          # Output: Crime category bar chart
├── requirements.txt                                    # Project dependencies
└── readme.md                                           # Project documentation
```

---

## 🛠️ Setup & Installation

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Analysis:**
   ```bash
   python "Crime Data Analysis & Knowledge Representation.py"
   ```

---

## 📋 Requirements (`requirements.txt`)

* `pandas` - Data manipulation and multi-CSV concatenation
* `numpy` - Vectorized calculations
* `matplotlib` - Chart generation (`q1c_graph1_time.png`, `q1c_graph2_crime_types.png`)
* `scipy` - Statistical calculations (`scipy.stats.norm`)

---

## 👨‍💻 Author

**Manan Arora**
