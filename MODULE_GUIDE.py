"""
Module Documentation & Architecture Guide
Complete reference for modular retention analysis framework
"""

# ============================================================================
# MODULAR ARCHITECTURE OVERVIEW
# ============================================================================

FUTURE_DS_02/
├── MAIN EXECUTION
│   └── main.py                  # Entry point - orchestrates 10-step pipeline
│
├── CONFIGURATION
│   └── config.py                # All settings, paths, and constants
│
├── DATA LAYER
│   ├── data_io.py               # Loading raw data
│   └── cleaning.py              # Data cleaning and integration
│
├── ANALYSIS LAYER
│   └── analysis.py              # All calculations and analytics
│
├── PRESENTATION LAYER
│   ├── visualization.py         # Chart creation
│   └── reporting.py             # Report and CSV export
│
├── PACKAGE
│   └── __init__.py              # Package initialization
│
├── CONFIGURATION
│   ├── requirements.txt         # Python dependencies
│   └── README.md                # Full documentation
│
└── OUTPUTS (auto-created)
    └── retention_outputs/       # All generated files


# ============================================================================
# DETAILED MODULE BREAKDOWN
# ============================================================================

## main.py (140 lines)
Entry point that orchestrates the entire analysis workflow.

Functions:
  - main() - Coordinates 10-step pipeline

Execution:
  $ python main.py

Pipeline Steps:
  1. Load Data              (data_io.py)
  2. Clean & Prepare       (cleaning.py)
  3. Calculate KPIs        (analysis.py)
  4. Churn Analysis        (analysis.py)
  5. Retention Drivers     (analysis.py)
  6. Risk Scoring          (analysis.py)
  7. At-Risk Identification (analysis.py)
  8. Visualizations        (visualization.py)
  9. Export Data           (reporting.py)
  10. Generate Reports     (reporting.py)


## config.py (65 lines)
Central configuration hub for all settings.

Key Settings:
  - OUTPUT_DIR = "retention_outputs"
  - DATA_PATH = "../archive (1)"
  - PLOT_STYLE, PLOT_PALETTE, DPI
  - RISK_WEIGHT_* (5 scoring factors)
  - RISK_SCORE_THRESHOLD = 5
  - COLOR_* (chart colors)

To Customize:
  1. Edit config.py
  2. Run main.py
  Changes apply to entire pipeline


## data_io.py (45 lines)
Handles all data loading operations.

Exported Functions:
  - load_data() -> tuple of 5 DataFrames
    Returns: (subscriptions, churn_events, accounts, 
              feature_usage, support_tickets)

Usage:
  from data_io import load_data
  subs, churn, acct, feat, supp = load_data()

Key Features:
  - Reads from ../archive (1)/ directory
  - Validates all files exist
  - Returns 5 DataFrames with record counts printed


## cleaning.py (120 lines)
Data preparation and integration.

Exported Functions:
  - clean_and_prepare_data(subs, churn, acct, feat, supp) -> DataFrame
    Input: Five separate DataFrames
    Output: Single merged, cleaned DataFrame

Integration Steps:
  1. Parse all date columns
  2. Remove duplicates by ID
  3. Calculate subscription metrics
  4. Merge churn event details
  5. Add account information
  6. Add feature usage metrics
  7. Add support ticket metrics
  8. Calculate activity metrics
  9. Fill missing values

Usage:
  from cleaning import clean_and_prepare_data
  df = clean_and_prepare_data(subs, churn, acct, feat, supp)
  # Returns 7,429 rows with 50+ columns


## analysis.py (280 lines)
Core analytics and calculations.

Exported Functions:
  1. calculate_kpis(df) -> dict
     - Churn rate, ARR, lifetime value
     - Returns 11 key metrics

  2. analyze_churn_patterns(df) -> tuple
     - Churn by plan, country, reason
     - Returns 3 DataFrames

  3. identify_retention_drivers(df) -> DataFrame
     - Active vs churned comparison
     - Returns comparison table

  4. calculate_risk_score(df) -> DataFrame
     - Scores all customers 0-11
     - 5 weighted risk factors
     - Modifies df in place

  5. identify_at_risk_customers(df) -> tuple
     - Flags customers with risk_score >= 5
     - Returns (df, high_risk_df)

Custom Usage:
  from analysis import calculate_kpis, analyze_churn_patterns
  kpis = calculate_kpis(df)
  print(f"Churn: {kpis['churn_rate']:.1f}%")


## visualization.py (380 lines)
Professional chart creation.

Exported Functions:
  1. create_executive_overview(df, kpis)
     - Generates: 01_executive_dashboard.png
     - 7 subplots with KPIs and metrics

  2. create_churn_analysis_charts(df)
     - Generates: 02_churn_analysis.png
     - Reasons, trial/paid, downgrade, auto-renew

  3. create_retention_drivers_charts(df)
     - Generates: 03_retention_drivers.png
     - Features, support, referral, industry

Features:
  - Professional styling with config settings
  - Color schemes from config.py
  - High-resolution PNG output (300 DPI)
  - All charts 16x10 inches
  - Automatic legend and labels

Custom Visualization:
  from visualization import create_executive_overview
  from analysis import calculate_kpis
  
  # Generate just dashboard
  kpis = calculate_kpis(df)
  create_executive_overview(df, kpis)


## reporting.py (190 lines)
Report generation and data export.

Exported Functions:
  1. generate_executive_report(df, kpis, churn_plan, 
                             churn_reasons, high_risk) -> str
     - Returns formatted report text
     - 6 sections, 300+ lines
     - Ready for copy/paste

  2. export_summary_metrics(df)
     - Generates 3 CSV files
     - Metrics by plan/country/industry
     - ~20 metrics per CSV

  3. export_high_risk_customers(high_risk_customers)
     - Generates: high_risk_customers.csv
     - 2,000+ at-risk active accounts
     - 9 columns with risk details

  4. save_executive_report(report_text)
     - Generates: EXECUTIVE_REPORT.txt
     - Full strategic report
     - 250+ lines formatted

Usage:
  from reporting import generate_executive_report
  report = generate_executive_report(df, kpis, plan, reasons, risk)
  print(report)


## __init__.py (20 lines)
Package initialization.

Exports:
  - VERSION info
  - Key constants imported from config

Usage:
  import FUTURE_DS_02


# ============================================================================
# WORKFLOW EXAMPLES
# ============================================================================

### EXAMPLE 1: Standard Full Analysis
python main.py
# Generates all outputs in retention_outputs/


### EXAMPLE 2: Custom Risk Threshold
"""Edit config.py"""
RISK_SCORE_THRESHOLD = 6
"""Run analysis"""
python main.py


### EXAMPLE 3: Generate Visualizations Only
from data_io import load_data
from cleaning import clean_and_prepare_data
from analysis import calculate_kpis
from visualization import *

subs, churn, acct, feat, supp = load_data()
df = clean_and_prepare_data(subs, churn, acct, feat, supp)
kpis = calculate_kpis(df)

create_executive_overview(df, kpis)
create_churn_analysis_charts(df)
create_retention_drivers_charts(df)


### EXAMPLE 4: Export Data Only
from data_io import load_data
from cleaning import clean_and_prepare_data
from analysis import calculate_risk_score, identify_at_risk_customers
from reporting import export_high_risk_customers, export_summary_metrics

subs, churn, acct, feat, supp = load_data()
df = clean_and_prepare_data(subs, churn, acct, feat, supp)
df = calculate_risk_score(df)
df, high_risk = identify_at_risk_customers(df)

export_high_risk_customers(high_risk)
export_summary_metrics(df)


### EXAMPLE 5: Custom Analysis + Standard Report
from data_io import load_data
from cleaning import clean_and_prepare_data
from analysis import *
from reporting import generate_executive_report, save_executive_report

# Load and prepare
subs, churn, acct, feat, supp = load_data()
df = clean_and_prepare_data(subs, churn, acct, feat, supp)

# Run analyses
kpis = calculate_kpis(df)
churn_plan, churn_country, churn_reasons = analyze_churn_patterns(df)
df = calculate_risk_score(df)
df, high_risk = identify_at_risk_customers(df)

# Generate report
report = generate_executive_report(df, kpis, churn_plan, churn_reasons, high_risk)
save_executive_report(report)
print(report)


# ============================================================================
# DEPENDENCIES
# ============================================================================

Config imports:
  - os (standard library)
  - datetime (standard library)

Data I/O imports:
  - pandas
  - os

Cleaning imports:
  - pandas
  - config

Analysis imports:
  - pandas
  - numpy
  - config

Visualization imports:
  - pandas
  - numpy
  - matplotlib.pyplot
  - seaborn
  - config

Reporting imports:
  - pandas
  - config

Main imports:
  - warnings (standard library)
  - matplotlib.pyplot
  - seaborn
  - All custom modules


# ============================================================================
# EXTENDING THE FRAMEWORK
# ============================================================================

### ADD NEW ANALYSIS FUNCTION

1. Edit analysis.py:

def analyze_new_metric(df):
    \"\"\"Description of analysis\"\"\"
    result = df.groupby('column').agg({'metric': ['mean', 'count']})
    print(f"Result: {result}")
    return result


2. Call from main.py:

# After other analyses
new_result = analyze_new_metric(df)


### ADD NEW VISUALIZATION

1. Edit visualization.py:

def create_custom_chart(df):
    \"\"\"Your visualization\"\"\"
    fig, ax = plt.subplots(figsize=(12, 8))
    # Your plotting code
    plt.savefig(f'{OUTPUT_DIR}/custom.png', dpi=DPI)
    plt.close()


2. Call from main.py:

# In visualization step
create_custom_chart(df)


### ADD NEW DATA SOURCE

1. Edit data_io.py:

def load_new_data():
    \"\"\"Load new CSV\"\"\"
    df = pd.read_csv(os.path.join(DATA_PATH, 'new_file.csv'))
    return df


2. Use in main:

new_data = load_new_data()


### MODIFY RISK SCORING

1. Edit config.py:

RISK_WEIGHT_NEW_FACTOR = 2


2. Edit analysis.py calculate_risk_score():

df.loc[condition, 'risk_score'] += RISK_WEIGHT_NEW_FACTOR


# ============================================================================
# STATUS: PRODUCTION READY
# ============================================================================

✓ Modular architecture with separation of concerns
✓ Configuration-driven (all settings in config.py)
✓ Reusable components (import individual modules)
✓ Professional visualizations (3 high-quality charts)
✓ Comprehensive reporting (CSV + TXT exports)
✓ Well-documented (docstrings + examples)
✓ Error handling (try/except where needed)
✓ Performance (2-3 minute runtime typical)

Last Updated: 2026-04-06
Version: 1.0 Modular
