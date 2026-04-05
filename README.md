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

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install pandas numpy matplotlib seaborn
```

### 2. Prepare Data

Ensure your data files are in the `../archive (1)/` directory:
```
../archive (1)/
├── ravenstack_subscriptions.csv
├── ravenstack_churn_events.csv
├── ravenstack_accounts.csv
├── ravenstack_feature_usage.csv
└── ravenstack_support_tickets.csv
```

### 3. Run the Analysis

```bash
python main.py
```

The script will:
- ✓ Load and validate all data sources
- ✓ Clean and integrate datasets
- ✓ Calculate key performance indicators
- ✓ Analyze churn patterns and drivers
- ✓ Generate professional visualizations
- ✓ Identify high-risk customers
- ✓ Export comprehensive reports

All outputs saved to `retention_outputs/` folder

---

## 📊 Output Files

### Visualizations

**01_executive_dashboard.png**
- Churn rate KPI
- Active vs churned customer split
- ARR at risk
- Plan tier churn comparison
- Customer lifetime distribution
- Country-level churn rates
- Feature engagement metrics

**02_churn_analysis.png**
- Churn reasons pie chart
- Trial vs paid account churn
- Downgrade impact analysis
- Auto-renew effectiveness

**03_retention_drivers.png**
- Feature usage impact on churn
- Support ticket frequency analysis
- Referral source impact
- Industry-specific churn rates

### Data Reports

**EXECUTIVE_REPORT.txt**
- Executive summary with key findings
- Strategic recommendations (5 priorities)
- Financial impact projections
- Next steps for implementation

**high_risk_customers.csv**
- List of 2,000+ active customers at risk of churn
- Risk score for each customer
- Account details and metrics
- Use for targeted intervention campaigns

**metrics_by_plan.csv, metrics_by_country.csv, metrics_by_industry.csv**
- Detailed segmentation by customer attributes
- Churn rates, ARR, customer lifetime, feature usage
- Support ticket metrics

---

## 🔍 Data Requirements

### Required Columns

**ravenstack_subscriptions.csv**
- subscription_id, account_id, start_date, end_date
- plan_tier, seats, mrr_amount, arr_amount
- is_trial, churn_flag, auto_renew_flag, upgrade_flag, downgrade_flag

**ravenstack_churn_events.csv**
- churn_event_id, account_id, churn_date
- reason_code, refund_amount_usd, feedback_text

**ravenstack_accounts.csv**
- account_id, account_name, industry, country
- signup_date, referral_source

**ravenstack_feature_usage.csv**
- usage_id, subscription_id, usage_date
- feature_name, usage_count, error_count

**ravenstack_support_tickets.csv**
- ticket_id, account_id, submitted_at, priority
- resolution_time_hours, escalation_flag

---

## 📈 Key Metrics Explained

| Metric | Definition | Industry Benchmark |
|--------|-----------|-------------------|
| **Churn Rate** | % of customers who cancel each period | 5-10% (SaaS) |
| **Revenue Churn** | % of ARR lost to cancellations | 3-5% (SaaS) |
| **Customer Lifetime** | Days from signup to churn/current | 18+ months (healthy) |
| **Feature Adoption** | Avg # of features used per customer | Higher = better retention |
| **High Risk** | Risk score ≥5 (out of 11) | Intervention needed |

---

## 💻 Using Individual Modules

You can import and use individual modules independently:

### Example: Using Just the Analysis Module

```python
from data_io import load_data
from cleaning import clean_and_prepare_data
from analysis import calculate_kpis, analyze_churn_patterns

# Load and clean data
subscriptions, churn_events, accounts, feature_usage, support_tickets = load_data()
df = clean_and_prepare_data(subscriptions, churn_events, accounts, feature_usage, support_tickets)

# Run specific analyses
kpis = calculate_kpis(df)
churn_by_plan, churn_by_country, churn_reasons = analyze_churn_patterns(df)

print(f"Churn Rate: {kpis['churn_rate']:.2f}%")
print(f"ARR at Risk: ${kpis['churned_arr']:,.0f}")
```

### Example: Custom Visualization

```python
from data_io import load_data
from cleaning import clean_and_prepare_data
from visualization import create_executive_overview
from analysis import calculate_kpis

df = clean_and_prepare_data(...)
kpis = calculate_kpis(df)

# Generate just the dashboard
create_executive_overview(df, kpis)
```

### Example: Exporting Data Only

```python
from data_io import load_data
from cleaning import clean_and_prepare_data
from reporting import export_summary_metrics

df = clean_and_prepare_data(...)
export_summary_metrics(df)
```

---

## 📊 Analysis Pipeline (10 Steps)

When you run `main.py`, it executes:

1. **Load Data** - Read all CSV files with validation
2. **Data Processing** - Clean, validate, merge datasets
3. **Key Metrics** - Calculate churn rate, ARR, lifetime value
4. **Churn Analysis** - Analyze churn by plan, country, reason
5. **Retention Drivers** - Compare active vs churned characteristics
6. **Risk Scoring** - Calculate risk scores on 5 factors
7. **Risk Identification** - Flag 2,000+ at-risk customers
8. **Create Visualizations** - Generate 3 professional dashboards
9. **Export Data** - Save CSV files and metrics
10. **Generate Reports** - Create executive summary report

Total runtime: **2-3 minutes** (typical)

---

## 🔧 Customization Guide

### Modify Risk Scoring Weights

Edit `config.py`:

```python
# Risk scoring weights (higher = more important)
RISK_WEIGHT_LOW_FEATURE_USAGE = 3
RISK_WEIGHT_HIGH_SUPPORT_ISSUES = 2
RISK_WEIGHT_DOWNGRADE = 3
RISK_WEIGHT_INACTIVITY = 2
RISK_WEIGHT_NO_AUTORENEW = 1

# Threshold for flagging as high-risk
RISK_SCORE_THRESHOLD = 5  # Customers with score ≥ 5 are flagged
```

### Change Output Directory

Edit `config.py`:
```python
OUTPUT_DIR = "my_custom_folder"
```

### Adjust Data Paths

Edit `config.py`:
```python
DATA_PATH = "/path/to/data"
```

### Add Custom Analysis

Create a new function in `analysis.py`:

```python
def analyze_custom_metric(df):
    """Your custom analysis logic here"""
    result = df.groupby('some_column').agg({...})
    return result
```

Call it from `main.py`:

```python
# In main.py, after Step 5
custom_result = analyze_custom_metric(df)
```

### Create Custom Visualizations

Create a new function in `visualization.py`:

```python
def create_custom_chart(df):
    """Your custom visualization here"""
    fig, ax = plt.subplots(figsize=(12, 8))
    # Your plotting code
    plt.savefig(f'{OUTPUT_DIR}/custom_chart.png', dpi=300)
    plt.close()
```

Call it from `main.py`:

```python
# In Step 8 (Creating Visualizations)
create_custom_chart(df)
```

---

## 📚 Best Practices

### For Regular Use
- Run monthly to track trends
- Compare monthly results to spot changes
- Monitor high-risk customer list for effectiveness

### For Customization
- Always modify in `config.py` first (centralized settings)
- Add new analyses to `analysis.py`
- Add visualizations to `visualization.py`
- Call new functions from `main.py`

### For Deployment
- Test on sample data first
- Validate output files are generated
- Check visualizations render correctly
- Verify CSV exports have correct data

### For Maintenance
- Keep module dependencies minimal
- Use config for all parameters
- Add docstrings to new functions
- Test changes with sample data

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **FileNotFoundError: CSV not found** | Verify data files exist in `../archive (1)/` directory |
| **KeyError: Column not found** | Check CSV headers match expected names (see Data Requirements) |
| **matplotlib error** | Ensure display environment supports PNG output |
| **ModuleNotFoundError** | Run `pip install -r requirements.txt` |
| **Missing data in charts** | Check data quality - some segments may have <5 records (filtered out) |
| **Memory error on large datasets** | Process data in chunks or use filtering |

---

## 📝 Common Tasks

### Generate only high-risk customer list
```python
from main import *

df = clean_and_prepare_data(...)
df = calculate_risk_score(df)
df, high_risk = identify_at_risk_customers(df)
export_high_risk_customers(high_risk)
```

### Update risk thresholds
Edit `config.py` and rerun `main.py`:
```python
RISK_SCORE_THRESHOLD = 6  # Higher threshold = fewer customers flagged
```

### Add a new churn reason filter
Edit `main.py` after Step 4:
```python
specific_reason = df[df['reason_code'] == 'pricing']
specific_churn_rate = specific_reason['is_churned'].mean() * 100
print(f"Pricing churn: {specific_churn_rate:.1f}%")
```

---

---

## 🎯 Strategic Recommendations

The analysis identifies 5 priority areas:

1. **Trial-to-Paid Conversion** (Highest Impact)
   - Guide trial users through onboarding
   - Reduce trial churn from 10%+ to 5-8%

2. **Downgrade Monitoring** (Red Flag Event)
   - Downgrade → 11%+ churn rate
   - Implement immediate outreach protocol

3. **Feature Engagement** (Low Feature Usage = High Churn)
   - 2,200 at-risk customers have engagement issues
   - Drive adoption through in-app education

4. **Auto-Renewal Enablement** (Friction Reduction)
   - Manual renewal adds 0.3% churn
   - Default to auto-renew for new signups

5. **Support Quality** (Operational Excellence)
   - High-priority support tickets correlate with churn
   - Improve first response time and resolution

---

## 💡 How to Use the Results

### For Product Teams
- Identify which features drive retention
- Focus product roadmap on high-impact features
- Measure success by cohort retention improvements

### For Success Teams
- Use high_risk_customers.csv for proactive outreach
- Create intervention playbooks by churn reason
- Implement customer health scoring

### For Executives
- Review EXECUTIVE_REPORT.txt for strategic priorities
- Track churn rate vs company OKRs
- Monitor ARR impact of retention improvements

### For Finance
- Estimate ARR saved by each intervention
- Calculate payback period for retention investments
- Track LTV improvements

---

---

## 🔧 Customization Guide

### Modify Risk Scoring Weights

Edit `config.py`:

```python
# Risk scoring weights (higher = more important)
RISK_WEIGHT_LOW_FEATURE_USAGE = 3
RISK_WEIGHT_HIGH_SUPPORT_ISSUES = 2
RISK_WEIGHT_DOWNGRADE = 3
RISK_WEIGHT_INACTIVITY = 2
RISK_WEIGHT_NO_AUTORENEW = 1

# Threshold for flagging as high-risk
RISK_SCORE_THRESHOLD = 5  # Customers with score ≥ 5 are flagged
```

### Change Output Directory

Edit `config.py`:
```python
OUTPUT_DIR = "my_custom_folder"
```

### Adjust Data Paths

Edit `config.py`:
```python
DATA_PATH = "/path/to/data"
```

### Add Custom Analysis

Create a new function in `analysis.py`:

```python
def analyze_custom_metric(df):
    """Your custom analysis logic here"""
    result = df.groupby('some_column').agg({...})
    return result
```

Call it from `main.py`:

```python
# In main.py, after Step 5
custom_result = analyze_custom_metric(df)
```

### Create Custom Visualizations

Create a new function in `visualization.py`:

```python
def create_custom_chart(df):
    """Your custom visualization here"""
    fig, ax = plt.subplots(figsize=(12, 8))
    # Your plotting code
    plt.savefig(f'{OUTPUT_DIR}/custom_chart.png', dpi=300)
    plt.close()
```

Call it from `main.py`:

```python
# In Step 8 (Creating Visualizations)
create_custom_chart(df)
```

---

## 📊 Output Files

### Visualizations (PNG)

**01_executive_dashboard.png** (Main Overview)
- Churn rate KPI box
- Active vs churned pie chart
- ARR at risk box
- Plan tier churn comparison
- Customer lifetime histogram
- Country-level churn rates
- Feature engagement comparison

**02_churn_analysis.png** (Detailed Churn)
- Churn reasons pie chart
- Trial vs paid churn bars
- Downgrade impact analysis
- Auto-renew effectiveness

**03_retention_drivers.png** (Drivers & Factors)
- Feature usage impact on churn
- Support ticket frequency analysis
- Referral source impact
- Industry-specific churn rates

### Data Files (CSV)

**high_risk_customers.csv** (2,000+ records)
- `account_id` - Customer account ID
- `account_name` - Company name
- `plan_tier` - Current plan (Basic/Pro/Enterprise)
- `arr_amount` - Annual recurring revenue
- `risk_score` - Calculated risk score (0-11)
- `total_features_used` - Feature engagement
- `high_priority_ratio` - % of high-priority support tickets
- `downgrade_flag` - Whether customer downgraded
- `days_since_activity` - Days of inactivity

**metrics_by_plan.csv, metrics_by_country.csv, metrics_by_industry.csv**
- `total_accounts` - Number of customers
- `churned_count` - Number who churned
- `churn_rate` - Churn rate percentage
- `total_arr` - Total annual revenue
- `avg_lifetime` - Average customer lifetime
- `avg_features` - Average features used

**EXECUTIVE_REPORT.txt**
- Full 5-section strategic report
- Findings and recommendations
- Financial impact projections
- Next steps and action items

---

## 🐛 Troubleshooting

**Error: FileNotFoundError - CSV files not found**
- Ensure data files are in `../archive (1)/` directory
- Check file paths match exactly

**Error: KeyError - Column not found**
- Verify CSV headers match expected column names
- Check for case sensitivity

**Graphs not displaying**
- Ensure matplotlib is properly installed
- Check display environment supports PNG output

**Missing data in visualizations**
- Filter conditions may exclude segments (e.g., <5 customers)
- Check data quality in source files

---

## 📝 License & Usage

This analysis framework is provided for business intelligence and retention analytics purposes.

**Recommended Usage:**
- ✅ Present to stakeholders
- ✅ Use for retention strategy planning
- ✅ Segment customers for targeted campaigns
- ✅ Track progress against recommendations

**Best Practices:**
- Run monthly to track trends
- Compare cohorts over time
- Implement recommendations and measure impact
- Update risk scores as new data available

---

## 🤝 Support & Questions

For issues or questions:
1. Review the EXECUTIVE_REPORT.txt for full analysis
2. Check individual CSV exports for data details
3. Verify source data quality and completeness

---

## 📅 Maintenance

**Update Frequency:** Monthly
**Data Refresh:** As new churn events occur
**Report Generation:** 2-3 minutes typical runtime

---

**Last Updated:** April 6, 2026
**Version:** 1.0
**Status:** Production Ready ✅
