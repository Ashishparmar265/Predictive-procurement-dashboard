# Student Analytics Dashboard V2 — Handover Report

**Date:** May 14, 2026  
**Status:** Completed & Optimized  
**Version:** 2.1 (Student-Centric Model)

---

## 1. Executive Summary
The procurement dashboard has been successfully transformed from a basic predictive tool into a high-fidelity, student-centric analytics interface. This version focuses on **population-scale projections**, accurately estimating behavior for over **600,000 students** and **15.7M enrollment records** by extrapolating insights from a representative 0.5% behavioral sample.

---

## 2. Key UI Features & Analytics
The dashboard now includes the following high-value visualizations and metrics:

### A. High-Impact KPI Cards
*   **Opt-In Ratio (Actual)**: The primary success metric showing the real-world adoption rate.
*   **Total Students (Est.)**: Projected global student population across all campuses.
*   **Avg Savings / Student**: The direct financial value delivered to each opted-in student compared to retail costs.
*   **Total Projected Savings ($M)**: The cumulative economic impact of the bundle program across the university system.

### B. Procurement & Behavioral Charts
*   **Potential Savings by Department**: A prioritized view for procurement teams to identify departments with the highest untapped ROI.
*   **Bundle Discount Impact**: Granular analysis of how price changes (from -30% to +30%) affect student adoption.
*   **eBook vs Physical Book**: Comparison of adoption rates across different material formats.
*   **Enrollment Status**: Side-by-side comparison of **Full-Time** vs **Part-Time** student behavior.
*   **Opt-In Trend by Term**: Multi-year analysis of program growth and seasonal fluctuations.

### C. Advanced UI Elements
*   **Dynamic Word Cloud**: A vivid, high-density visualization of the most popular course materials among students who opted in.
*   **Campus Mapping**: Obscure database IDs (e.g., "784-23") have been mapped to human-readable university names (e.g., "University of Central Florida") for intuitive filtering.
*   **Top 15 Departments**: Expanded view of academic unit performance with full titles.

---

## 3. Data Integration Details
*   **Global Scaling**: The dashboard uses a scaling factor of **~27.77 enrollments per student** to convert course-level data into unique student counts.
*   **Campus Metadata**: A comprehensive mapping dictionary is integrated to bridge the gap between legacy database codes and university names.
*   **Stopword Filtering**: The Word Cloud uses an optimized "Academic Stopword" filter to remove noise words (e.g., "Edition", "Access", "Pearson") to highlight actual subjects.

---

## 4. Operational Requirements
*   **Technology Stack**: Python, Streamlit, Plotly, Pandas.
*   **Main Logic**: `dashboard_app.py`
*   **Core Data**: `resource/global_kpis.csv` (Population metrics) and `resource/dashboard_sample.csv` (Behavioral sample).

---
*Report generated and finalized by Antigravity AI Coding Assistant.*
