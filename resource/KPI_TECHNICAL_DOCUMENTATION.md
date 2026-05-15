# Student Analytics Dashboard V2.1 — Comprehensive KPI & Metrics Documentation

## 1. Introduction
The Student Analytics Dashboard is a high-performance decision-support tool designed for university procurement officers and academic administrators. It leverages a 15.7-million-record population dataset to provide actionable insights into student purchasing behavior, program ROI, and price sensitivity.

---

## 2. Global KPI Cards (Executive Summary)

### 📊 Opt-In Ratio (Actual Capture Rate)
*   **Definition**: The proportion of the total estimated student population that successfully opted into the bundle program.
*   **Visual Representation**: A "Hero" card featuring the raw ratio (e.g., `312,450 / 566,830`) and the percentage.
*   **Computation Logic**:
    *   `Actual Rate` = `Mean(target)` from the behavioral sample.
    *   `Projected Count` = `Estimated Total Students` × `Actual Rate`.
*   **Significance**: Measures the "Market Share" of the university's program. A low ratio suggests students are finding better value elsewhere; a high ratio validates the program's convenience and pricing.

### 👥 Total Students (Estimated Population)
*   **Definition**: The projected number of unique individual students affected by the selected filters (Campus, Dept, Term).
*   **Significance**: Provides a "Human-Scale" context. While the backend processes millions of enrollment rows, this card answers the fundamental question: *"How many individual students does this affect?"*
*   **Technical Formula**: `Total Bundles in Filter` / `27.767`.
    *   *The factor 27.767 represents the average number of course-level records per unique student identifier in the 15.7M row population.*

### 💰 Avg Savings / Student
*   **Definition**: The average financial benefit (in USD) realized by each student who chooses to opt-in.
*   **Computation Logic**:
    *   Calculates the difference between the **Retail Price** and the **Bundle Price** for every successful opt-in.
    *   `Formula`: `Mean(potential_savings)` where `potential_savings > 0`.
*   **Significance**: Quantifies the "Individual ROI." This is a key metric for student advocacy and program marketing.

### 💎 Total Projected Savings ($M)
*   **Definition**: The cumulative economic value saved by the entire student body through the bundle program.
*   **Computation Logic**:
    *   `Step 1`: Sum all `potential_savings` in the representative sample.
    *   `Step 2`: Multiply by the population scale factor (`15,739,385 / Sample_Size`).
    *   `Step 3`: Divide by 1,000,000 for the final dollar value in millions.
*   **Significance**: The "Grand ROI." This metric justifies the program's existence to university boards and state legislatures by demonstrating massive institutional savings.

---

## 3. Behavioral & Procurement Visualizations

### 🏦 Opt-In Rate by Campus (University Benchmarking)
*   **View**: Sorted Horizontal Bar Chart.
*   **Logic**: Aggregates opt-in probabilities by university name.
*   **Significance**: Identifies top-performing campuses. High-performing campuses can be used as "Internal Case Studies" to help lower-performing campuses improve their adoption strategies.

### 🏢 Top 15 Departments by Opt-In Rate
*   **View**: Horizontal Bar Chart with full department names and estimated student counts.
*   **Logic**: Filters for departments with a statistically significant sample size and ranks them by average opt-in probability.
*   **Significance**: Highlights academic disciplines where the bundle program is most successful (e.g., Nursing or Biology), allowing for department-specific outreach.

### 📈 Potential Savings by Department (Negotiation Priority)
*   **View**: Green-scaled Bar Chart showing savings in thousands of dollars ($K).
*   **Significance**: **The Procurement Roadmap.** It identifies where the most money is being saved (or could be saved). Departments at the top represent the highest priority for contract renewals and publisher negotiations.

### 📉 Bundle Discount Impact (Price Sensitivity)
*   **View**: Categorical Bar Chart with 6 specific bands:
    *   `< -10%` (Overpriced/Premium)
    *   `-10% to 0%` (Near-Retail)
    *   `Exactly 0%` (Retail Match)
    *   `0% to 1%` (Standard Discount)
*   **Significance**: Visualizes "Price Elasticity." It tells administrators: *"How much of a discount do we need to offer to move the needle on student adoption?"*

### 📱 eBook vs Physical Book (Format Preference)
*   **View**: Comparison of Opt-In rates by material format.
*   **Significance**: Guides the Digital Transformation strategy. If eBook opt-in rates are significantly higher, it justifies a shift toward "Digital-First" adoption models.

### 🎓 Student Enrollment Status (Full-Time vs Part-Time)
*   **View**: Side-by-side bar comparison.
*   **Significance**: Explains behavioral differences based on enrollment intensity. Full-time students typically have higher opt-in rates due to the convenience of "one-stop-shop" bundle procurement.

---

## 4. Model Confidence & Distribution

### 🎯 Adoption Model Breakdown
*   **View**: Grouped Bar Chart (Opted-In vs Opted-Out) across different models.
*   **Significance**: Identifies which procurement models (EO, FD, RQ) are driving the most volume and which ones are experiencing higher "friction" (opt-outs).

### ☁️ Dynamic Word Cloud (Material Insights)
*   **Logic**: Real-time frequency analysis of book titles from opted-in records.
*   **Filtering**: Automatically removes common noise words (Edition, Vol, Pearson, etc.) using an academic stopword filter.
*   **Significance**: Provides a "Pulse Check" on what students are actually buying. Larger titles indicate high-volume course materials that are cornerstone to the program's success.

---

## 5. Technical Foundations

*   **Scaling Constant**: `27.767` (Used to extrapolate course enrollments to unique student identities).
*   **Model Confidence**: The dashboard assumes a **91.1% reliability index** based on the underlying PySpark ML model evaluations.
*   **Mapping Logic**: Uses internal dictionaries (`CAMPUS_MAPPING`, `DEPT_MAPPING`) to ensure all technical database codes are translated into human-readable university and department names.

---
*Comprehensive Technical Documentation — Prepared by Antigravity AI.*
