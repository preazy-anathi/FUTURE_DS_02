"""
Data Cleaning and Integration
Handles data validation, cleaning, and merging of datasets
"""

import pandas as pd
from config import REPORT_DATE


def clean_and_prepare_data(subscriptions, churn_events, accounts, feature_usage, support_tickets):
    """
    Clean, validate, and merge all datasets into a unified dataframe.
    
    Args:
        subscriptions: Subscription data
        churn_events: Churn events data
        accounts: Account data
        feature_usage: Feature usage data
        support_tickets: Support tickets data
    
    Returns:
        pd.DataFrame: Cleaned and merged dataset
    """
    
    print("Data Cleaning & Integration:")
    print("="*80)
    
    # ==============================
    # 1. PARSE DATES
    # ==============================
    subscriptions['start_date'] = pd.to_datetime(subscriptions['start_date'])
    subscriptions['end_date'] = pd.to_datetime(subscriptions['end_date'], errors='coerce')
    churn_events['churn_date'] = pd.to_datetime(churn_events['churn_date'])
    accounts['signup_date'] = pd.to_datetime(accounts['signup_date'], errors='coerce')
    support_tickets['submitted_at'] = pd.to_datetime(support_tickets['submitted_at'], errors='coerce')
    feature_usage['usage_date'] = pd.to_datetime(feature_usage['usage_date'], errors='coerce')
    
    # ==============================
    # 2. REMOVE DUPLICATES
    # ==============================
    subscriptions = subscriptions.drop_duplicates(subset=['subscription_id'], keep='first')
    churn_events = churn_events.drop_duplicates(subset=['churn_event_id'], keep='first')
    
    # ==============================
    # 3. HANDLE MISSING VALUES
    # ==============================
    subscriptions['end_date'].fillna(pd.Timestamp.now(), inplace=True)
    
    # ==============================
    # 4. CALCULATE SUBSCRIPTION METRICS
    # ==============================
    subscriptions['subscription_age_days'] = (subscriptions['end_date'] - subscriptions['start_date']).dt.days
    subscriptions['is_churned'] = subscriptions['churn_flag'].astype(int)
    
    # ==============================
    # 5. MERGE WITH CHURN EVENT DETAILS
    # ==============================
    df = subscriptions.merge(
        churn_events[['account_id', 'churn_date', 'reason_code', 'refund_amount_usd', 'feedback_text']],
        on='account_id',
        how='left'
    )
    
    # ==============================
    # 6. MERGE WITH ACCOUNT DETAILS
    # ==============================
    df = df.merge(accounts[['account_id', 'account_name', 'industry', 'country', 'referral_source']], 
                  on='account_id', how='left')
    
    # ==============================
    # 7. ADD FEATURE USAGE METRICS
    # ==============================
    feature_agg = feature_usage.groupby('subscription_id').agg({
        'usage_count': 'sum',
        'usage_date': 'max',
        'error_count': 'sum'
    }).reset_index()
    feature_agg.columns = ['subscription_id', 'total_features_used', 'last_feature_usage', 'total_errors']
    feature_agg['last_feature_usage'] = pd.to_datetime(feature_agg['last_feature_usage'], errors='coerce')
    
    df = df.merge(feature_agg, on='subscription_id', how='left')
    df['total_features_used'].fillna(0, inplace=True)
    df['total_errors'].fillna(0, inplace=True)
    
    # ==============================
    # 8. ADD SUPPORT METRICS
    # ==============================
    support_agg = support_tickets.groupby('account_id').agg({
        'ticket_id': 'count',
        'priority': lambda x: (x == 'high').sum() / len(x) if len(x) > 0 else 0
    }).reset_index()
    support_agg.columns = ['account_id', 'total_support_tickets', 'high_priority_ratio']
    
    df = df.merge(support_agg, on='account_id', how='left')
    df['total_support_tickets'].fillna(0, inplace=True)
    df['high_priority_ratio'].fillna(0, inplace=True)
    
    # ==============================
    # 9. CALCULATE ACTIVITY METRICS
    # ==============================
    df['last_activity_date'] = df[['end_date', 'last_feature_usage']].max(axis=1)
    df['days_since_activity'] = (pd.Timestamp.now() - df['last_activity_date']).dt.days
    
    # ==============================
    # 10. FILL REMAINING MISSING VALUES
    # ==============================
    df['industry'].fillna('Unknown', inplace=True)
    df['country'].fillna('Unknown', inplace=True)
    df['referral_source'].fillna('Unknown', inplace=True)
    df['reason_code'].fillna('unknown', inplace=True)
    
    # ==============================
    # 11. LOGGING
    # ==============================
    print(f"✓ Data cleaned: {len(df)} records processed")
    print(f"✓ Churn records: {df['is_churned'].sum()}")
    print(f"✓ Active records: {(1 - df['is_churned']).sum()}")
    print()
    
    return df
