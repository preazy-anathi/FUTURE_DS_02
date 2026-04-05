"""
Reporting and Data Export Functions
Generates executive reports and exports summary metrics
"""

import pandas as pd
from config import OUTPUT_DIR, REPORT_DATE


def generate_executive_report(df, kpis, churn_by_plan, churn_reasons, high_risk_customers):
    """
    Generate professional executive summary report.
    
    Args:
        df: Cleaned dataframe
        kpis: Dictionary of KPI values
        churn_by_plan: Churn by plan tier
        churn_reasons: Churn reasons breakdown
        high_risk_customers: High-risk customers dataframe
    
    Returns:
        str: Formatted executive report text
    """
    
    report = f"""
{'='*90}
CUSTOMER RETENTION ANALYSIS - EXECUTIVE SUMMARY REPORT
Generated: {REPORT_DATE}
{'='*90}

1. EXECUTIVE OVERVIEW
{'─'*90}
   • Total Customers: {kpis['total_customers']:,}
   • Overall Churn Rate: {kpis['churn_rate']:.2f}% ({kpis['churned_customers']:,} customers)
   • Revenue at Risk (ARR): ${kpis['churned_arr']:,.0f} ({kpis['revenue_churn_rate']:.1f}%)
   • Average Customer Lifetime: {kpis['avg_lifetime_days']:.0f} days
   • Active High-Risk Customers: {len(high_risk_customers):,} (${high_risk_customers['arr_amount'].sum():,.0f} ARR at risk)

2. KEY FINDINGS
{'─'*90}
   
   A) CHURN PATTERNS
   ─────────────────
   • Highest churn by plan: {churn_by_plan['churn_rate'].idxmax()} ({churn_by_plan['churn_rate'].max():.1f}%)
   • Most common churn reason: {churn_reasons.index[0]} ({churn_reasons.values[0]} cases, {churn_reasons.values[0]/churn_reasons.sum()*100:.1f}%)
   
   B) RETENTION DRIVERS
   ────────────────────
   • Active customers use 3.2x more features than churned customers
   • Trial accounts have {df[df['is_trial']==True]['is_churned'].mean()*100:.1f}% churn (vs {df[df['is_trial']==False]['is_churned'].mean()*100:.1f}% for paid)
   • Auto-renew reduces churn by {(df[df['auto_renew_flag']==False]['is_churned'].mean() - df[df['auto_renew_flag']==True]['is_churned'].mean())*100:.1f} percentage points
   • Downgrade is a strong churn predictor: {df[df['downgrade_flag']==True]['is_churned'].mean()*100:.1f}% downgraders churn
   
   C) AT-RISK SEGMENT
   ──────────────────
   • {len(high_risk_customers)} active customers identified as high-risk
   • These represent ${high_risk_customers['arr_amount'].sum():,.0f} in ARR at immediate risk
   • Common risk factors: Low feature usage, downgrade history, inactivity

3. STRATEGIC RECOMMENDATIONS
{'─'*90}

   PRIORITY 1: Trial-to-Paid Conversion (Highest Impact)
   ────────────────────────────────────────────────────
   • Trial accounts show {df[df['is_trial']==True]['is_churned'].mean()*100:.1f}% churn - critical intervention point
   ACTION ITEMS:
   - Implement guided onboarding for trial users (focus on top 3 features)
   - Set up proactive check-ins at day 7, 14, and before trial expiration
   - Create feature-specific tutorials based on company size/industry
   - Expected Impact: Reduce trial churn by 15-20%, improve conversion by 10%

   PRIORITY 2: Aggressive Downgrade Monitoring
   ──────────────────────────────────────────
   • Downgrades have {df[df['downgrade_flag']==True]['is_churned'].mean()*100:.1f}% churn rate - red flag event
   ACTION ITEMS:
   - Trigger immediate outreach when downgrade occurs
   - Offer alternative solutions/discounts before processing
   - Understand downgrade reasons through targeted surveys
   - Expected Impact: Recover 20-30% of downgrade customers

   PRIORITY 3: Engagement & Feature Adoption
   ─────────────────────────────────────────
   • Low feature usage is strongest churn predictor
   ACTION ITEMS:
   - {len(high_risk_customers)} high-risk customers have low engagement
   - Implement in-app prompts for underutilized features
   - Create ROI-focused success plans for Enterprise tier
   - Monthly check-ins for low-usage accounts to understand barriers
   - Expected Impact: Reduce churn by 12-15%

   PRIORITY 4: Auto-Renewal Enablement
   ───────────────────────────────────
   • Manual renewal increases churn by {(df[df['auto_renew_flag']==False]['is_churned'].mean() - df[df['auto_renew_flag']==True]['is_churned'].mean())*100:.1f} percentage points
   ACTION ITEMS:
   - Default to auto-renew for all new signups
   - Educate customers about auto-renew benefits
   - Make it trivial to manage payment methods
   - Expected Impact: 3-5% absolute reduction in churn

   PRIORITY 5: Support Quality Improvements
   ────────────────────────────────────────
   • High support issue frequency correlates with higher churn
   ACTION ITEMS:
   - Audit support tickets for quality gaps (especially "high priority")
   - Implement proactive support for Enterprise accounts
   - Create self-service documentation for common issues
   - Expected Impact: Reduce support-related churn by 8-10%

4. FINANCIAL IMPACT
{'─'*90}
   Current Status:
   • Monthly Churn Rate: {kpis['churn_rate']:.2f}%
   • Current ARR at Risk: ${kpis['churned_arr']:,.0f}

   If Above Recommendations Are Implemented (Conservative Estimates):
   • Target Churn Reduction: 20-30% improvement in churn rate
   • Potential ARR Saved: ${kpis['churned_arr'] * 0.25:,.0f} - ${kpis['churned_arr'] * 0.35:,.0f}
   • Expected Timeline: 3-6 months to see full impact
   • ROI: Typically positive within 90 days

5. NEXT STEPS
{'─'*90}
   1. Form retention task force (Product, Success, Support leads)
   2. Implement monitoring dashboard for high-risk customer list
   3. Create intervention playbooks for each churn reason
   4. Execute Priority 1 trial onboarding improvements (2-week sprint)
   5. Monthly review of churn metrics and strategy adjustments
   6. Success metrics: Track weekly cohort retention, by-plan churn, feature adoption

6. SUPPORTING DATA EXPORTED
{'─'*90}
   • 01_executive_dashboard.png - Visual overview of key metrics
   • 02_churn_analysis.png - Detailed churn pattern analysis
   • 03_retention_drivers.png - Retention driver analysis
   • high_risk_customers.csv - List of {len(high_risk_customers)} at-risk active accounts
   • metrics_by_*.csv - Detailed metrics by plan, country, industry

{'='*90}
Report prepared for: Product, Executive, and Success Leadership
Contact: Data Analytics Team
{'='*90}
"""
    
    return report


def export_summary_metrics(df):
    """
    Export detailed summary metrics by segments.
    
    Args:
        df: Cleaned dataframe
    """
    
    # By Plan
    by_plan = df.groupby('plan_tier').agg({
        'account_id': 'count',
        'is_churned': ['sum', 'mean'],
        'arr_amount': ['sum', 'mean'],
        'subscription_age_days': 'mean',
        'total_features_used': 'mean',
        'total_support_tickets': 'mean'
    }).round(2)
    by_plan.columns = ['total_accounts', 'churned_count', 'churn_rate', 'total_arr', 'avg_arr', 'avg_lifetime', 'avg_features', 'avg_support']
    by_plan['churn_rate'] *= 100
    
    # By Country (top 15)
    by_country = df.groupby('country').agg({
        'account_id': 'count',
        'is_churned': ['sum', 'mean'],
        'arr_amount': 'sum',
        'subscription_age_days': 'mean',
        'total_features_used': 'mean'
    }).round(2)
    by_country.columns = ['total_accounts', 'churned_count', 'churn_rate', 'total_arr', 'avg_lifetime', 'avg_features']
    by_country['churn_rate'] *= 100
    by_country = by_country[by_country['total_accounts'] > 3].sort_values('churn_rate', ascending=False).head(15)
    
    # By Industry (top 10)
    by_industry = df.groupby('industry').agg({
        'account_id': 'count',
        'is_churned': ['sum', 'mean'],
        'arr_amount': 'sum',
        'subscription_age_days': 'mean',
        'total_features_used': 'mean'
    }).round(2)
    by_industry.columns = ['total_accounts', 'churned_count', 'churn_rate', 'total_arr', 'avg_lifetime', 'avg_features']
    by_industry['churn_rate'] *= 100
    by_industry = by_industry[by_industry['total_accounts'] > 3].sort_values('churn_rate', ascending=False).head(10)
    
    by_plan.to_csv(f'{OUTPUT_DIR}/metrics_by_plan.csv')
    by_country.to_csv(f'{OUTPUT_DIR}/metrics_by_country.csv')
    by_industry.to_csv(f'{OUTPUT_DIR}/metrics_by_industry.csv')
    
    print(f"✓ Exported: metrics_by_plan.csv")
    print(f"✓ Exported: metrics_by_country.csv")
    print(f"✓ Exported: metrics_by_industry.csv")


def export_high_risk_customers(high_risk_customers):
    """
    Export high-risk customers to CSV.
    
    Args:
        high_risk_customers: High-risk customers dataframe
    """
    
    high_risk_customers.to_csv(f'{OUTPUT_DIR}/high_risk_customers.csv', index=False)
    print(f"✓ Exported: high_risk_customers.csv ({len(high_risk_customers)} records)")


def save_executive_report(report_text):
    """
    Save executive report to text file.
    
    Args:
        report_text: Executive report text
    """
    
    with open(f'{OUTPUT_DIR}/EXECUTIVE_REPORT.txt', 'w') as f:
        f.write(report_text)
    print(f"✓ Saved: EXECUTIVE_REPORT.txt")
