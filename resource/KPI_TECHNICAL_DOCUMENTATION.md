# Technical KPI Documentation — Student Analytics Dashboard

This document provides a detailed breakdown of the Key Performance Indicators (KPIs) and visualizations featured in the Student Analytics Dashboard.

---

## 1. Top-Level KPI Cards

### A. Opt-In Ratio (Actual)
*   **What it shows**: The number of students who purchased a bundle versus the total estimated student population.
*   **What it means**: This is the "Capture Rate" of the program. It tells you how many students are choosing the university-provided bundle over alternative sourcing (Amazon, used books, etc.).
*   **Significance**: This is the primary success metric. A rising ratio indicates the program is providing competitive value and convenience.
*   **How it is computed**:
    *   `Actual Opt-Ins` = `Estimated Total Students` × `Actual Opt-In Rate (from sample)`
    *   `Display` = `{Opted-In Count} / {Total Population Count}`

### B. Total Students (Est.)
*   **What it shows**: The projected number of unique students affected by the current filter.
*   **What it means**: Converts high-volume course enrollment data (15.7M records) into human-scale numbers (600k students).
*   **Significance**: Essential for understanding the "human scale" of the impact. It helps administrators see exactly how many lives are touched by the program.
*   **How it is computed**:
    *   `Formula`: `Total Course Enrollments` / `27.767`
    *   *Note: 27.767 is the historically verified ratio of bundle records to unique students in the full population.*

### C. Avg Savings / Student
*   **What it shows**: The average dollar amount saved by a student who opts into the program.
*   **What it means**: The per-person financial benefit of the bundle program compared to retail prices.
*   **Significance**: This is the core "Value Proposition." It is used in marketing to students and reporting to boards to justify the program's existence.
*   **How it is computed**:
    *   `Formula`: `Mean(potential_savings)` where `potential_savings > 0`.
    *   *Note: This only considers positive savings to ensure accuracy in value reporting.*

### D. Total Projected Savings ($M)
*   **What it shows**: The total economic value saved across the entire university population.
*   **What it means**: The macro-economic impact of the procurement program.
*   **Significance**: Used for high-level institutional reporting to demonstrate the massive scale of the program's financial benefit (often reaching into the hundreds of millions).
*   **How it is computed**:
    *   `Formula`: `Sum(potential_savings in sample)` × `(Total Population Enrollments / Sample Enrollments)` / `1,000,000`.

---

## 2. Behavioral & Procurement Visuals

### E. Potential Savings by Department (Procurement Priority)
*   **What it shows**: A horizontal bar chart of departments with the highest total dollar savings.
*   **Significance**: Identifies "Low Hanging Fruit." Departments at the top of this list are where procurement teams should focus their negotiations to maximize university-wide savings.
*   **Computation**: Groups all students by department and sums their `potential_savings`, scaled to the full population.

### F. Bundle Discount Impact on Student Opt-In
*   **What it shows**: How sensitive students are to the price of the bundle.
*   **Significance**: Helps in pricing strategy. It identifies the "Price Elasticity" of students. If opt-in rates drop sharply at a certain discount level, it helps set the floor for bundle negotiations.
*   **Computation**: Bins `bundle_discount_pct` into 6 bands (from -30% to +30%) and calculates the mean `prob_optin` for each.

### G. eBook vs Physical Book Opt-In Rate
*   **What it shows**: Adoption preference between digital and print materials.
*   **Significance**: Guides long-term digital transformation strategy. If eBooks have higher opt-in rates, it justifies further investment in digital platforms.
*   **Computation**: Maps the `is_ebook` boolean to labels and calculates the average `prob_optin` per group.

### H. Expected Opt-In Rate by Student Enrollment Status
*   **What it shows**: Adoption behavior differences between **Full-Time** and **Part-Time** students.
*   **Significance**: Helps in tailored marketing. Full-time students often have more predictable book needs and may find the bundle more convenient than part-time students.
*   **Computation**: Maps `student_type_score` (1.0 = Full, 0.5 = Part) to labels and averages the prediction probability.

---
*Technical Documentation — Dashboard V2.1*
