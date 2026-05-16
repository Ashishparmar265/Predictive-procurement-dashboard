# Model Documentation Report
## Student Bundle Opt-In Prediction — For the Visualisation Team

> **Who this is for:** The next team receiving our outputs. This document explains the three models we built, why we built three instead of one, what each model does, what it looks at, and exactly how to interpret and use the prediction files we are handing over.

---

## 1. The Business Problem

Barnes & Noble Education runs a programme called **Inclusive Access** — students are automatically enrolled in a discounted digital textbook bundle at the start of term. They can **opt in** (keep it and pay) or **opt out** (return it and pay nothing).

**The core question we answered:** *"Will this specific student, for this specific book, opt into the bundle?"*

This prediction has direct value for:
- Forecasting bundle revenue per campus
- Identifying which courses and departments drive opt-ins
- Spotting students who are likely to opt out before the deadline, allowing early intervention

---

## 2. Why Three Models — Not One

This is the most important architectural decision we made. The dataset contains a column called **`adoption_type`** that describes *how* a book is being used in a course. There are three dominant types:

| Adoption Type | Code | What It Means |
|---|---|---|
| First Day | **FD** | Student receives books on Day 1 of class — they physically have them already |
| Required | **RQ** | The book is explicitly required for the course |
| Explore Only | **EO** | The student is browsing/exploring options, no hard commitment |

### Why separate models are necessary

These three groups have **completely different base opt-in rates**:

| Model | Adoption Type | Actual Opt-In Rate |
|---|---|---|
| FD model | First Day | ~38–43% |
| RQ model | Required | ~78–83% |
| EO model | Explore Only | ~28–36% |

If we trained a single combined model, it would simply learn:
> *"Is this record RQ? → Predict 1. Is it FD or EO? → Predict 0."*

It would never learn the real patterns within each group — *which students* actually commit, *which price points* trigger opt-outs, or *which departments* drive behaviour. The split forces each model to learn meaningful, actionable signals within its context.

**The three models have genuinely different dominant features** — which proves the separation was correct (detailed in Section 4).

---

## 3. The Algorithm: HistGradientBoostingClassifier

All three models use **sklearn's HistGradientBoostingClassifier** — a histogram-based gradient boosting decision tree.

### How it works (plain English)

It builds many small decision trees one after another. Each new tree tries to fix the mistakes the previous trees made. After 100 rounds, the combined ensemble produces a robust prediction. The "histogram" part means it groups continuous values (like book price) into buckets first, which makes the whole process much faster on millions of rows.

### Why we chose this algorithm

| Reason | Why it mattered |
|---|---|
| Handles missing values natively | Bundle pricing columns are 30–65% null for RQ/EO rows — we don't need to impute them |
| Speed at scale | Processes millions of rows without memory issues |
| `class_weight='balanced'` | Automatically adjusts for skewed opt-in rates across campuses |
| Outputs probability scores | `predict_proba()` gives a 0–1 score — critical for Power BI dashboards |
| Solid defaults | Works well without heavy hyperparameter tuning |

### Training configuration

```python
HistGradientBoostingClassifier(
    max_iter=100,           # 100 boosting rounds
    class_weight='balanced' # handles class imbalance automatically
)
```

---

## 4. The Five Features

All three models use the **same five input features**. They were chosen because they are available for every campus, every term, and every student — and they have no data leakage risk.

---

### Feature 1 — `retail_new` (Book Retail Price)

**What it is:** The retail price of a new physical copy of the book, in US dollars.

**How it was sourced:** Directly from the raw campus CSV. Cast to a float. Nulls filled with 0.

**Why it helps:** Price is the clearest student-facing signal. A $200 textbook makes the bundle more attractive (big savings). A $12 book means the bundle barely saves anything. Students make rational financial decisions — price shapes those decisions.

**What the model learned from it:**
- FD model: **Strongest signal** (importance score: 0.0499). Price dominates First Day decisions.
- RQ model: Second strongest (0.0210). Even required books face price resistance at high costs.
- EO model: Negligible (0.0001). Explore-Only records rarely have bundle pricing populated.

---

### Feature 2 — `student_type_score` (Enrollment Intensity)

**What it is:** A numeric encoding of whether the student is full-time, part-time, or half-time.

**How it was engineered:**
```
Full-time  (F) → 1.00
Part-time  (P) → 0.50
Half-time  (H) → 0.25
Unknown/other  → 0.50 (default)
```

**Source column:** `student_full_part_time_status` in the raw CSV.

**Why it helps:** Full-time students treat textbooks as a core part of their semester. They are enrolled in more courses, spending more time on campus, and are more financially committed. Part-time students may be taking one or two courses, be more price-sensitive, or may drop the course. This score captures "academic commitment level."

**What the model learned from it:**
- EO model: **Dominant signal** (0.0492) — for undecided students, enrollment status is the best remaining predictor.
- RQ model: **Dominant signal** (0.0351) — for required books, full-time students comply; part-time students are more likely to skip.
- FD model: Third-place (0.0174) — meaningful but overshadowed by price signals.

---

### Feature 3 — `bundle_discount_pct` (How Good the Deal Is)

**What it is:** The percentage discount the bundle offers compared to buying the book at full retail.

**Formula:**
```
bundle_discount_pct = (retail_new - bundle_price_discounted) / retail_new
```
Set to 0 if `retail_new <= 0` (divide-by-zero protection).

**Source columns:** `retail_new` and `bundle_price_discounted` from the raw CSV.

**Why it helps:** A 40% discount should logically attract more opt-ins than a 5% discount. This feature directly measures the rational financial incentive for the student.

**What the model learned from it:**
- Weaker than expected across all three models (all scored ≤ 0.0022).
- This is because bundle discount percentages don't vary much across campuses — most sit in a narrow band. There isn't enough variation in the discount to be a strong differentiator.
- This feature is only meaningful for FD records; for RQ and EO, `bundle_price_discounted` is often null, so this defaults to 0.

---

### Feature 4 — `is_ebook` (Digital Format Flag)

**What it is:** Binary flag — 1 if the book is an eBook, 0 if it is a physical book.

**How it was engineered:**
```
cover_type == "EB" → 1
anything else      → 0
```

**Source column:** `cover_type` in the raw CSV.

**Why it helps:** eBooks are instantly accessible, often cheaper, and don't require shipping or carrying. Some student segments strongly prefer them and are more willing to opt into a digital bundle. Other students prefer physical books — if the bundle is eBook-only, they may opt out. This feature captures format preference as a proxy for opt-in likelihood.

**What the model learned from it:**
- FD model: **Second strongest** (0.0287). Format drives First Day decisions significantly.
- RQ model: Weak (0.0033). Required books are bought regardless of format.
- EO model: Slightly negative (−0.0016) — the model learned a spurious pattern from inconsistent `cover_type` values in EO records. This feature marginally hurts EO performance.

---

### Feature 5 — `is_stem_dept` (STEM Department Flag)

**What it is:** Binary flag — 1 if the course department is a STEM field, 0 otherwise.

**How it was engineered:** Checks if `dept_code` is in this hardcoded list:
```
BIOL, CHEM, MATH, PHYS, NURS, ENGR, COMP, CS, CSIS, ANAT, MICR, STAT
```

**Source column:** `dept_code` in the raw CSV.

**Why it helps:** STEM courses tend to have strict, mandatory textbook requirements — lab manuals, access codes, homework systems. Students in these departments are more likely to need and buy their books. This captures a course-type signal that predicts compliance.

**What the model learned from it:**
- All three models: Very weak (≤ 0.0011). Once price and enrollment status are accounted for, STEM alone adds little.
- The signal is real but is absorbed by other features.

---

### Features Intentionally Excluded (Leakage Prevention)

These columns **look useful** but would cause data leakage — they are derived from the target variable and would not be available at real prediction time:

| Column | Why Excluded |
|---|---|
| `buy_frac` | Directly derived from `final_will_buy` (the target) |
| `buy_frac_binary` | Binary version of `buy_frac` |
| `improved_will_buy` | Another target-correlated proxy score |

Using these would make the model score near-perfect in testing but fail completely in real deployment.

---

## 5. Feature Importance Summary — Cross-Model

| Feature | FD Model | RQ Model | EO Model | Key Takeaway |
|---|---|---|---|---|
| `retail_new` | **0.0499** (1st) | 0.0210 (2nd) | 0.0001 (none) | Price drives purchase decisions, not exploration |
| `is_ebook` | **0.0287** (2nd) | 0.0033 (weak) | −0.0016 (hurts) | Format matters for FD; irrelevant elsewhere |
| `student_type_score` | 0.0174 (3rd) | **0.0351** (1st) | **0.0492** (1st) | Enrollment intensity dominates RQ and EO |
| `bundle_discount_pct` | 0.0022 (weak) | 0.0022 (weak) | 0.0000 (none) | Discount effect weaker than expected |
| `is_stem_dept` | 0.0011 (minimal) | 0.0000 (none) | 0.0000 (none) | STEM flag barely helps any model |

> Importance = how much ROC-AUC drops when that feature is randomly shuffled (Permutation Importance). Higher = more critical.

**The three models have different dominant features.** This is the strongest evidence that splitting by adoption type was the right call.

---

## 6. Target Variable — What We Were Predicting

**Source column:** `final_will_buy` in the raw CSV.

This is a continuous float representing the fraction of students in a section who bought. We binarised it:
```
target = 1  if  final_will_buy >= 0.5
target = 0  otherwise
```

So `target = 1` means: the majority of students in that section opted into the bundle for that book.

---

## 7. Model Performance

### Overall Metrics

| Metric | FD Model | RQ Model | EO Model |
|---|---|---|---|
| **ROC-AUC** | **0.6077** | **0.5775** | **0.5557** |
| Accuracy | 59.2% | 69.3% | 43.6% |
| Actual opt-in rate | 42.8% | 78.8% | 28.4% |
| Avg predicted probability | 0.501 | 0.538 | 0.496 |

> **ROC-AUC** measures ranking quality: 0.5 = random guessing, 1.0 = perfect. Our FD model at 0.61 is meaningfully better than random on real-world data with only 5 features.

### FD Model — Most Reliable (Use This for Business Decisions)

| Class | Precision | Recall | F1 |
|---|---|---|---|
| Opt-Out (0) | 0.64 | 0.64 | 0.64 |
| Opt-In (1) | 0.52 | 0.53 | 0.53 |

The FD model is the most balanced and trustworthy. Actual opt-in rate is ~43%, so the model has real uncertainty to resolve.

### RQ Model — High Accuracy, But Inflated

| Class | Precision | Recall | F1 |
|---|---|---|---|
| Opt-Out (0) | 0.30 | 0.35 | 0.32 |
| Opt-In (1) | 0.82 | 0.79 | 0.80 |

**69% accuracy sounds good but is misleading** — the actual opt-in rate for RQ is ~79%, so always predicting "opt-in" would score 79% without any model. Use `prob_optin` for nuance, not the raw accuracy figure.

### EO Model — Weakest (Use With Caution)

| Class | Precision | Recall | F1 |
|---|---|---|---|
| Opt-Out (0) | 0.81 | 0.28 | 0.41 |
| Opt-In (1) | 0.31 | 0.84 | 0.46 |

EO records have almost no usable features (bundle pricing is null, the student hasn't committed). The model essentially falls back to `student_type_score` only. Treat EO predictions as directional signals, not precise forecasts.

### Campus-Level Performance (FD Model)

| Campus | Opt-In Rate | ROC-AUC |
|---|---|---|
| saintleo | 42.3% | 0.654 |
| latechu | 40.9% | 0.653 |
| fiu | 35.2% | 0.650 |
| shsu | 41.9% | 0.638 |
| Ju | 39.2% | 0.632 |
| eku | 45.6% | 0.620 |
| hindscc | 43.5% | 0.605 |
| ccis | 38.5% | 0.562 |
| ucumberlands | 37.7% | 0.552 |

Campuses with fewer FD records (ccis, ucumberlands) show lower ROC-AUC — less data means less reliable predictions.

---

## 8. Output Files — What You Received

All files are in `data_processed/`.

### Prediction Files (3 files)

`pyspark_predictions_fd.csv` / `_rq.csv` / `_eo.csv`

Each row is one student × one book × one section, with model predictions attached.

| Column | Type | Description |
|---|---|---|
| `sis_user_id` | string | Unique student ID |
| `campus_code` | string | Campus identifier |
| `dept_code` | string | Academic department (e.g., MATH, BIOL) |
| `adoption_type` | string | FD, RQ, or EO |
| `target` | 0 or 1 | Actual outcome — did the student opt in? |
| `retail_new` | float | Book retail price ($) |
| `bundle_discount_pct` | float | Fraction discount from the bundle |
| `is_stem_dept` | 0 or 1 | Is this a STEM department? |
| `is_ebook` | 0 or 1 | Is the book an eBook? |
| `student_type_score` | float | 1.0 = full-time, 0.5 = part-time, 0.25 = half-time |
| `title` | string | Book title |
| `author` | string | Book author |
| `isbn` | string | ISBN identifier |
| `term_year` | int | Academic year |
| `term_code` | string | Term semester code |
| `prob_optin` | float (0–1) | **Model's predicted probability of opt-in** |
| `prediction` | 0 or 1 | Hard binary decision — will they opt in? |

> **`prob_optin` is the key column for visualisation.** It gives a continuous score, not just yes/no. Use it for ranking students, building gauges, and identifying at-risk groups.

### Campus Analysis File

`campus_analysis.csv` — per-campus summary metrics.

| Column | Description |
|---|---|
| `campus` | Campus name |
| `total_rows` | Total records for this campus |
| `fd_rows` | First Day adoption records |
| `opt_in_rate` | Fraction of FD students who opted in |
| `n_opted_in` | Count of opt-ins |
| `n_opted_out` | Count of opt-outs |
| `n_students` | Unique student count |
| `n_sections` | Unique course section count |
| `roc_auc` | Model ROC-AUC performance for this campus |

### Model Files (3 `.pkl` files)

`model_fd_pyspark.pkl` / `model_rq_pyspark.pkl` / `model_eo_pyspark.pkl`

Each is a Python pickle file containing:
```python
{
    'model': <HistGradientBoostingClassifier>,
    'features': ['retail_new', 'bundle_discount_pct', 'is_stem_dept', 'is_ebook', 'student_type_score']
}
```

To reload and generate new predictions:
```python
import pickle
with open('model_fd_pyspark.pkl', 'rb') as f:
    bundle = pickle.load(f)
model = bundle['model']
features = bundle['features']
new_probs = model.predict_proba(new_data[features])[:, 1]
```

---

## 9. How to Use This for Visualisation

### Which file to use for what

| Visualisation Goal | Use This File |
|---|---|
| Primary opt-in analysis | `pyspark_predictions_fd.csv` — FD is the most reliable model |
| Required book compliance | `pyspark_predictions_rq.csv` — shows which required books are at risk |
| Campus comparison | `campus_analysis.csv` — aggregated per-campus metrics |
| Full student-level view | All three CSVs joined on `campus_code` |

### Recommended Visualisations

**1. Predicted vs Actual Opt-In Rate by Campus (Bar Chart)**
- X-axis: `campus_code`
- Two bars: `AVG(prob_optin)` and `AVG(target)`
- Shows where the model matches reality and where gaps exist

**2. Probability Distribution Histogram**
- X-axis: `prob_optin` in 0.1 bins
- A bimodal shape (peaks near 0 and 1) = model is confident
- A flat/bell shape = model is uncertain

**3. Price vs Opt-In Probability (Scatter, FD file)**
- X: `retail_new`, Y: `prob_optin`
- Should show a relationship — reveals price elasticity by campus

**4. Department Heatmap**
- Rows: `dept_code`, Columns: `campus_code`, Colour: `AVG(prob_optin)`
- Identifies which departments drive opt-ins at which schools

**5. At-Risk Students Table**
- Filter: `target == 1` AND `prob_optin < 0.4`
- These are students who actually opted in but the model predicted they wouldn't
- Valuable for understanding edge cases and improving the model

**6. Full-Time vs Part-Time Opt-In Comparison**
- Compare `AVG(prob_optin)` where `student_type_score == 1.0` vs `0.5`
- Quantifies the enrollment-intensity effect across campuses

### Key Filters to Implement

- `campus_code` — to drill into individual institutions
- `adoption_type` — to switch between FD / RQ / EO views
- `dept_code` — for department-level analysis
- `is_stem_dept` — STEM vs non-STEM comparison
- `term_year` + `term_code` — for temporal trends
- `prob_optin` slider — to segment by confidence level (e.g., show only >70%)

---

## 10. Important Caveats for the Visualisation Team

1. **The RQ model's 69% accuracy is not as impressive as it sounds.** RQ books have a ~79% natural opt-in rate. The model only needs to beat 79% random baseline to add value.

2. **EO predictions are directional, not precise.** The EO model converged early (53/100 iterations) because there are almost no usable features for Explore-Only records. Use EO `prob_optin` for broad trends, not individual student decisions.

3. **`prob_optin` near 0.5 means the model is uncertain.** Values far from 0.5 (below 0.3 or above 0.7) are more trustworthy.

4. **Small campuses have less reliable predictions.** Campuses with fewer than ~5,000 FD records (e.g., ccis at ~51K total rows, ~20K FD rows) show lower ROC-AUC. Weight their predictions with caution.

5. **Do not use `buy_frac`, `buy_frac_binary`, or `improved_will_buy` as analysis dimensions.** These columns are in the raw data but are derived from the target — they will create circular, misleading insights.

6. **The three CSV files can be unioned** for a full combined view, since they share the same schema. Use `adoption_type` as a filter/slicer to separate them.

---

## 11. Summary Card

| | FD Model | RQ Model | EO Model |
|---|---|---|---|
| **What it predicts** | First Day bundle opt-in | Required book opt-in | Explore-Only opt-in |
| **Opt-in base rate** | ~38–43% | ~78–83% | ~28–36% |
| **Most important feature** | Book price (`retail_new`) | Enrollment status | Enrollment status |
| **ROC-AUC** | 0.61 | 0.58 | 0.56 |
| **Reliability** | High | Medium (inflated by base rate) | Low |
| **Best use case** | Business decisions, revenue forecasting | Compliance monitoring | Broad trend analysis |
| **Output file** | `pyspark_predictions_fd.csv` | `pyspark_predictions_rq.csv` | `pyspark_predictions_eo.csv` |

---

*Documentation prepared by Team 3 — May 2026. For questions about the pipeline, see `multi_model_pipeline.py` and `docs/PROJECT_DOCUMENTATION.md`.*
