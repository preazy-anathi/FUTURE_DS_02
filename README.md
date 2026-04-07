# Customer Retention Analysis Dashboard 📊

A professional, **modular** analytics framework for analyzing customer churn, retention patterns, and identifying at-risk accounts in SaaS/subscription businesses.

## 📋 Overview

This project provides executive-level insights on:
- **Churn Patterns** - Identify which customer segments have the highest churn
- **Retention Drivers** - Understand what keeps customers engaged
- **Customer Lifetime Value** - Track how long customers stay active
- **At-Risk Identification** - Proactively identify customers likely to churn
- **Actionable Recommendations** - Strategic priorities to reduce churn

**Perfect for presenting to:** Product Managers, Founders, Executive Teams, or Business Stakeholders

---

## 🎯 Key Features

✅ **Modular Architecture**
- Separated concerns: data, cleaning, analysis, visualization, reporting
- Easy to extend and maintain
- Reusable components
- Clean code organization

✅ **Comprehensive Data Integration**
- Merges subscription, churn, account, feature usage, and support data
- Automated data cleaning and validation
- Handles missing values and duplicates

✅ **Executive-Ready Visualizations**
- Churn rate KPI dashboard
- Geographic and plan-tier analysis
- Retention driver identification
- Feature engagement metrics

✅ **Risk Scoring System**
- Proprietary risk algorithm weighing 5 factors
- Identifies 2,000+ at-risk customers
- Exportable list for targeted outreach

✅ **Detailed Analytics Reports**
- Executive summary with strategic recommendations
- Segmented metrics (by plan, country, industry)
- Churn reasons breakdown
- Financial impact analysis

---

## 📁 Project Structure

```
FUTURE_DS_02/
├── main.py                            # Entry point - orchestrates pipeline
├── config.py                          # Configuration & constants
├── data_io.py                         # Data loading functions
├── cleaning.py                        # Data cleaning & integration
├── analysis.py                        # KPI, churn, retention analysis
├── visualization.py                   # Chart creation functions
├── reporting.py                       # Reports & data export
├── __init__.py                        # Package initialization
├── requirements.txt                   # Python dependencies
├── README.md                          # This file
└── retention_outputs/                 # Generated reports & visualizations (auto-created)
    ├── 01_executive_dashboard.png     # KPI overview
    ├── 02_churn_analysis.png          # Churn patterns
    ├── 03_retention_drivers.png       # Retention factors
    ├── EXECUTIVE_REPORT.txt           # Full strategic report
    ├── high_risk_customers.csv        # At-risk accounts list
    ├── metrics_by_plan.csv            # Plan-tier breakdown
    ├── metrics_by_country.csv         # Geographic analysis
    └── metrics_by_industry.csv        # Industry breakdown
```

---

---

## 📦 Module Architecture

### **config.py** - Configuration & Constants
- Center for all configuration settings
- Output directories, paths, analysis parameters
- Color schemes and visualization settings
- Risk scoring weights and thresholds

### **data_io.py** - Data Loading
- `load_data()` - Loads all source datasets with validation
- Handles file paths and error reporting

### **cleaning.py** - Data Cleaning & Preparation
- `clean_and_prepare_data()` - Comprehensive data cleaning
- Date parsing and validation
- Duplicate removal and missing value handling
- Dataset integration and feature engineering
- Activity metrics calculation

### **analysis.py** - Core Analytics
- `calculate_kpis()` - Computes churn rate, ARR, lifetime value
- `analyze_churn_patterns()` - Churn by plan, country, reason
- `identify_retention_drivers()` - Compares active vs churned customers
- `calculate_risk_score()` - Scores customers on 5 risk factors
- `identify_at_risk_customers()` - Flags high-risk active accounts

### **visualization.py** - Chart Creation
- `create_executive_overview()` - Dashboard with KPIs and overview
- `create_churn_analysis_charts()` - Detailed churn patterns
- `create_retention_drivers_charts()` - Feature usage and support analysis
- Professional styling with reusable visualization functions

### **reporting.py** - Reports & Export
- `generate_executive_report()` - Formatted strategic report text
- `export_summary_metrics()` - Metrics by plan, country, industry
- `export_high_risk_customers()` - Exports at-risk customer list
- `save_executive_report()` - Saves report to file

### **main.py** - Orchestration
- Entry point for the entire pipeline
- Coordinates 10-step analysis workflow
- Imports and calls all modules in sequence
- Provides progress feedback

---

