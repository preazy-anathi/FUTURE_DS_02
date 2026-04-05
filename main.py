"""
Main Orchestration Script
Coordinates the entire retention analysis pipeline
"""

import warnings
import matplotlib.pyplot as plt
import seaborn as sns

# Suppress warnings
warnings.filterwarnings('ignore')

# Import all modules
from config import REPORT_DATE, OUTPUT_DIR, PLOT_STYLE, PLOT_PALETTE
from data_io import load_data
from cleaning import clean_and_prepare_data
from analysis import (
    calculate_kpis,
    analyze_churn_patterns,
    identify_retention_drivers,
    calculate_risk_score,
    identify_at_risk_customers
)
from visualization import (
    create_executive_overview,
    create_churn_analysis_charts,
    create_retention_drivers_charts
)
from reporting import (
    generate_executive_report,
    export_summary_metrics,
    export_high_risk_customers,
    save_executive_report
)

# Set plotting style
plt.style.use(PLOT_STYLE)
sns.set_palette(PLOT_PALETTE)


def main():
    """
    Main execution pipeline for retention analysis.
    Orchestrates all steps of the analysis workflow.
    """
    
    print(f"\n{'='*80}")
    print(f"CUSTOMER RETENTION ANALYSIS DASHBOARD")
    print(f"Generated: {REPORT_DATE}")
    print(f"{'='*80}\n")
    
    # ==============================
    # STEP 1: LOAD DATA
    # ==============================
    print("\nSTEP 1: Loading Data")
    print("-" * 80)
    subscriptions, churn_events, accounts, feature_usage, support_tickets = load_data()
    
    # ==============================
    # STEP 2: CLEAN & PREPARE DATA
    # ==============================
    print("\nSTEP 2: Data Processing")
    print("-" * 80)
    df = clean_and_prepare_data(subscriptions, churn_events, accounts, feature_usage, support_tickets)
    
    # ==============================
    # STEP 3: CALCULATE KPIs
    # ==============================
    print("\nSTEP 3: Key Metrics")
    print("-" * 80)
    kpis = calculate_kpis(df)
    
    # ==============================
    # STEP 4: ANALYZE CHURN PATTERNS
    # ==============================
    print("\nSTEP 4: Churn Analysis")
    print("-" * 80)
    churn_by_plan, churn_by_country, churn_reasons = analyze_churn_patterns(df)
    
    # ==============================
    # STEP 5: IDENTIFY RETENTION DRIVERS
    # ==============================
    print("\nSTEP 5: Retention Drivers")
    print("-" * 80)
    comparison = identify_retention_drivers(df)
    
    # ==============================
    # STEP 6: CALCULATE RISK SCORES
    # ==============================
    print("\nSTEP 6: Risk Scoring")
    print("-" * 80)
    df = calculate_risk_score(df)
    print("✓ Risk scores calculated for all customers")
    
    # ==============================
    # STEP 7: IDENTIFY AT-RISK CUSTOMERS
    # ==============================
    print("\nSTEP 7: Risk Identification")
    print("-" * 80)
    df, high_risk_customers = identify_at_risk_customers(df)
    
    # ==============================
    # STEP 8: CREATE VISUALIZATIONS
    # ==============================
    print("\nSTEP 8: Creating Visualizations")
    print("-" * 80)
    create_executive_overview(df, kpis)
    create_churn_analysis_charts(df)
    create_retention_drivers_charts(df)
    
    # ==============================
    # STEP 9: EXPORT DATA & METRICS
    # ==============================
    print("\nSTEP 9: Exporting Data")
    print("-" * 80)
    export_high_risk_customers(high_risk_customers)
    export_summary_metrics(df)
    
    # ==============================
    # STEP 10: GENERATE REPORTS
    # ==============================
    print("\nSTEP 10: Generating Reports")
    print("-" * 80)
    report = generate_executive_report(df, kpis, churn_by_plan, churn_reasons, high_risk_customers)
    print(report)
    save_executive_report(report)
    
    # ==============================
    # COMPLETION MESSAGE
    # ==============================
    print(f"\n{'='*80}")
    print(f"✓ ANALYSIS COMPLETE!")
    print(f"All outputs saved to: {OUTPUT_DIR}/")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
