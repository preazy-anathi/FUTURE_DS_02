"""
Churn Analysis and KPI Calculations
Core analytics logic for retention insights
"""

import pandas as pd
import numpy as np
from config import (
    RISK_WEIGHT_LOW_FEATURE_USAGE,
    RISK_WEIGHT_HIGH_SUPPORT_ISSUES,
    RISK_WEIGHT_DOWNGRADE,
    RISK_WEIGHT_INACTIVITY,
    RISK_WEIGHT_NO_AUTORENEW,
    RISK_SCORE_THRESHOLD
)


def calculate_kpis(df):
    """
    Calculate key performance indicators.
    
    Args:
        df: Cleaned and merged dataframe
    
    Returns:
        dict: Dictionary of KPI values
    """
    
    print("Key Performance Indicators:")
    print("="*80)
    
    # Overall metrics
    total_customers = len(df)
    churned_customers = df['is_churned'].sum()
    active_customers = total_customers - churned_customers
    churn_rate = (churned_customers / total_customers) * 100
    
    # Revenue metrics
    total_arr = df['arr_amount'].sum()
    churned_arr = df[df['is_churned'] == 1]['arr_amount'].sum()
    revenue_churn_rate = (churned_arr / total_arr) * 100 if total_arr > 0 else 0
    
    # Lifetime metrics
    avg_lifetime = df['subscription_age_days'].mean()
    median_lifetime = df['subscription_age_days'].median()
    
    # Engagement metrics
    avg_features_used = df['total_features_used'].mean()
    avg_support_tickets = df['total_support_tickets'].mean()
    
    kpis = {
        'total_customers': total_customers,
        'active_customers': active_customers,
        'churned_customers': churned_customers,
        'churn_rate': churn_rate,
        'revenue_churn_rate': revenue_churn_rate,
        'total_arr': total_arr,
        'churned_arr': churned_arr,
        'avg_lifetime_days': avg_lifetime,
        'median_lifetime_days': median_lifetime,
        'avg_features_used': avg_features_used,
        'avg_support_tickets': avg_support_tickets,
    }
    
    print(f"Total Customers: {total_customers:,.0f}")
    print(f"Active Customers: {active_customers:,.0f}")
    print(f"Churned Customers: {churned_customers:,.0f}")
    print(f"Overall Churn Rate: {churn_rate:.2f}%")
    print(f"Revenue Churn Rate: {revenue_churn_rate:.2f}%")
    print(f"Total ARR: ${total_arr:,.0f}")
    print(f"ARR at Risk (Churned): ${churned_arr:,.0f}")
    print(f"Avg Customer Lifetime: {avg_lifetime:.0f} days")
    print(f"Median Customer Lifetime: {median_lifetime:.0f} days")
    print()
    
    return kpis


def analyze_churn_patterns(df):
    """
    Analyze churn by different dimensions.
    
    Args:
        df: Cleaned and merged dataframe
    
    Returns:
        tuple: (churn_by_plan, churn_by_country, churn_reasons)
    """
    
    print("Churn Pattern Analysis:")
    print("="*80)
    
    # Churn by Plan Tier
    churn_by_plan = df.groupby('plan_tier').agg({
        'is_churned': ['count', 'sum', 'mean']
    }).round(4)
    churn_by_plan.columns = ['total', 'churned', 'churn_rate']
    churn_by_plan['churn_rate'] *= 100
    print("\nChurn by Plan Tier:")
    print(churn_by_plan)
    
    # Churn by Country
    churn_by_country = df.groupby('country').agg({
        'is_churned': ['count', 'sum', 'mean']
    }).round(4)
    churn_by_country.columns = ['total', 'churned', 'churn_rate']
    churn_by_country['churn_rate'] *= 100
    print("\nChurn by Country (Top 10):")
    print(churn_by_country.head(10))
    
    # Churn by Reason
    churn_reasons = df[df['is_churned'] == 1]['reason_code'].value_counts()
    print("\nChurn Reasons Distribution:")
    print(churn_reasons)
    print()
    
    return churn_by_plan, churn_by_country, churn_reasons


def identify_retention_drivers(df):
    """
    Identify factors that drive better retention.
    
    Args:
        df: Cleaned and merged dataframe
    
    Returns:
        pd.DataFrame: Comparison of active vs churned customer characteristics
    """
    
    print("Retention Drivers Analysis:")
    print("="*80)
    
    # Compare active vs churned customers
    comparison = pd.DataFrame({
        'Active': [
            df[df['is_churned'] == 0]['total_features_used'].mean(),
            df[df['is_churned'] == 0]['total_support_tickets'].mean(),
            df[df['is_churned'] == 0]['subscription_age_days'].mean(),
            df[df['is_churned'] == 0]['arr_amount'].mean(),
        ],
        'Churned': [
            df[df['is_churned'] == 1]['total_features_used'].mean(),
            df[df['is_churned'] == 1]['total_support_tickets'].mean(),
            df[df['is_churned'] == 1]['subscription_age_days'].mean(),
            df[df['is_churned'] == 1]['arr_amount'].mean(),
        ]
    }, index=['Avg Features Used', 'Avg Support Tickets', 'Avg Lifetime (days)', 'Avg MRR'])
    
    print("\nActive vs Churned Customer Characteristics:")
    print(comparison.round(2))
    print()
    
    # Trial conversion impact
    trial_churn = df[df['is_trial'] == True]['is_churned'].mean() * 100
    paid_churn = df[df['is_trial'] == False]['is_churned'].mean() * 100
    print(f"Trial Accounts Churn Rate: {trial_churn:.2f}%")
    print(f"Paid Accounts Churn Rate: {paid_churn:.2f}%")
    
    # Auto-renew impact
    autorenew_churn = df[df['auto_renew_flag'] == True]['is_churned'].mean() * 100
    manual_churn = df[df['auto_renew_flag'] == False]['is_churned'].mean() * 100
    print(f"Auto-Renew Accounts Churn Rate: {autorenew_churn:.2f}%")
    print(f"Manual Renewal Accounts Churn Rate: {manual_churn:.2f}%")
    print()
    
    return comparison


def calculate_risk_score(df):
    """
    Calculate risk scores for all customers based on multiple factors.
    
    Args:
        df: Cleaned and merged dataframe
    
    Returns:
        pd.DataFrame: DataFrame with risk_score column added
    """
    
    df['risk_score'] = 0
    
    # Low feature usage (weight: 3)
    low_feature_threshold = df['total_features_used'].quantile(0.25)
    df.loc[df['total_features_used'] <= low_feature_threshold, 'risk_score'] += RISK_WEIGHT_LOW_FEATURE_USAGE
    
    # High support issue ratio (weight: 2)
    high_support_threshold = df['high_priority_ratio'].quantile(0.75)
    df.loc[df['high_priority_ratio'] >= high_support_threshold, 'risk_score'] += RISK_WEIGHT_HIGH_SUPPORT_ISSUES
    
    # Downgrade flag (weight: 3)
    df.loc[df['downgrade_flag'] == True, 'risk_score'] += RISK_WEIGHT_DOWNGRADE
    
    # Long inactivity (weight: 2)
    high_inactivity = df['days_since_activity'].quantile(0.75)
    df.loc[df['days_since_activity'] >= high_inactivity, 'risk_score'] += RISK_WEIGHT_INACTIVITY
    
    # No auto-renew (weight: 1)
    df.loc[df['auto_renew_flag'] == False, 'risk_score'] += RISK_WEIGHT_NO_AUTORENEW
    
    return df


def identify_at_risk_customers(df):
    """
    Identify customers at high risk of churn.
    
    Args:
        df: Cleaned dataframe with risk scores
    
    Returns:
        tuple: (df with risk scores, high_risk_customers dataframe)
    """
    
    # High-risk customers (still active but showing warning signs)
    high_risk = df[(df['is_churned'] == 0) & (df['risk_score'] >= RISK_SCORE_THRESHOLD)].sort_values('risk_score', ascending=False)
    high_risk_export = high_risk[[
        'account_id', 'account_name', 'plan_tier', 'arr_amount', 'risk_score',
        'total_features_used', 'high_priority_ratio', 'downgrade_flag', 'days_since_activity'
    ]].copy()
    
    print("HIGH-RISK CUSTOMERS (Active but at risk):")
    print(f"Total High-Risk Customers: {len(high_risk_export)}")
    print(f"ARR at Risk: ${high_risk_export['arr_amount'].sum():,.0f}")
    print("\nTop 15 High-Risk Accounts:")
    print(high_risk_export.head(15).to_string(index=False))
    print()
    
    return df, high_risk_export
