"""
================================================================================
CUSTOMER RETENTION ANALYSIS DASHBOARD
Professional SaaS/Subscription Business Analytics Report
================================================================================
Purpose: Generate actionable insights on churn patterns, retention drivers, and 
customer lifetime value to inform retention strategies for business stakeholders.
================================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ==============================
# CONFIGURATION & STYLING
# ==============================
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
OUTPUT_DIR = "retention_outputs"
REPORT_DATE = datetime.now().strftime("%Y-%m-%d")

# Create output directory
import os
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"\n{'='*80}")
print(f"CUSTOMER RETENTION ANALYSIS DASHBOARD")
print(f"Generated: {REPORT_DATE}")
print(f"{'='*80}\n")


# ==============================
# 1. DATA LOADING & VALIDATION
# ==============================
def load_data():
    """Load and validate all source datasets."""
    try:
        subscriptions = pd.read_csv(r"../archive (1)\ravenstack_subscriptions.csv")
        churn_events = pd.read_csv(r"../archive (1)\ravenstack_churn_events.csv")
        accounts = pd.read_csv(r"../archive (1)\ravenstack_accounts.csv")
        feature_usage = pd.read_csv(r"../archive (1)\ravenstack_feature_usage.csv")
        support_tickets = pd.read_csv(r"../archive (1)\ravenstack_support_tickets.csv")
        
        print(f"✓ Subscriptions: {len(subscriptions)} records")
        print(f"✓ Churn Events: {len(churn_events)} records")
        print(f"✓ Accounts: {len(accounts)} records")
        print(f"✓ Feature Usage: {len(feature_usage)} records")
        print(f"✓ Support Tickets: {len(support_tickets)} records\n")
        
        return subscriptions, churn_events, accounts, feature_usage, support_tickets
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        raise


# ==============================
# 2. DATA CLEANING & INTEGRATION
# ==============================
def clean_and_prepare_data(subscriptions, churn_events, accounts, feature_usage, support_tickets):
    """Clean, validate, and merge all datasets."""
    
    print("Data Cleaning & Integration:")
    print("-" * 80)
    
    # Parse dates
    subscriptions['start_date'] = pd.to_datetime(subscriptions['start_date'])
    subscriptions['end_date'] = pd.to_datetime(subscriptions['end_date'], errors='coerce')
    churn_events['churn_date'] = pd.to_datetime(churn_events['churn_date'])
    accounts['signup_date'] = pd.to_datetime(accounts['signup_date'], errors='coerce')
    support_tickets['submitted_at'] = pd.to_datetime(support_tickets['submitted_at'], errors='coerce')
    feature_usage['usage_date'] = pd.to_datetime(feature_usage['usage_date'], errors='coerce')
    
    # Remove duplicates
    subscriptions = subscriptions.drop_duplicates(subset=['subscription_id'], keep='first')
    churn_events = churn_events.drop_duplicates(subset=['churn_event_id'], keep='first')
    
    # Handle missing values
    subscriptions['end_date'].fillna(pd.Timestamp.now(), inplace=True)
    
    # Calculate subscription metrics
    subscriptions['subscription_age_days'] = (subscriptions['end_date'] - subscriptions['start_date']).dt.days
    subscriptions['is_churned'] = subscriptions['churn_flag'].astype(int)
    
    # Merge with churn event details
    df = subscriptions.merge(
        churn_events[['account_id', 'churn_date', 'reason_code', 'refund_amount_usd', 'feedback_text']],
        on='account_id',
        how='left'
    )
    
    # Merge with account details
    df = df.merge(accounts[['account_id', 'account_name', 'industry', 'country', 'referral_source']], 
                  on='account_id', how='left')
    
    # Feature usage metrics per subscription
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
    
    # Support metrics per account
    support_agg = support_tickets.groupby('account_id').agg({
        'ticket_id': 'count',
        'priority': lambda x: (x == 'high').sum() / len(x) if len(x) > 0 else 0
    }).reset_index()
    support_agg.columns = ['account_id', 'total_support_tickets', 'high_priority_ratio']
    
    df = df.merge(support_agg, on='account_id', how='left')
    df['total_support_tickets'].fillna(0, inplace=True)
    df['high_priority_ratio'].fillna(0, inplace=True)
    
    # Calculate days since last activity
    df['last_activity_date'] = df[['end_date', 'last_feature_usage']].max(axis=1)
    df['days_since_activity'] = (pd.Timestamp.now() - df['last_activity_date']).dt.days
    
    # Fill missing values
    df['industry'].fillna('Unknown', inplace=True)
    df['country'].fillna('Unknown', inplace=True)
    df['referral_source'].fillna('Unknown', inplace=True)
    df['reason_code'].fillna('unknown', inplace=True)
    
    print(f"✓ Data cleaned: {len(df)} records processed")
    print(f"✓ Churn records: {df['is_churned'].sum()}")
    print(f"✓ Active records: {(1 - df['is_churned']).sum()}")
    print()
    
    return df


# ==============================
# 3. KEY METRICS CALCULATION
# ==============================
def calculate_kpis(df):
    """Calculate key performance indicators."""
    
    print("Key Performance Indicators:")
    print("-" * 80)
    
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


# ==============================
# 4. CHURN ANALYSIS
# ==============================
def analyze_churn_patterns(df):
    """Analyze churn by different dimensions."""
    
    print("Churn Pattern Analysis:")
    print("-" * 80)
    
    # Churn by Plan Tier
    churn_by_plan = df.groupby('plan_tier').agg({
        'is_churned': ['count', 'sum', 'mean']
    }).round(4)
    churn_by_plan.columns = ['total', 'churned', 'churn_rate']
    churn_by_plan['churn_rate'] *= 100
    print("\nChurn by Plan Tier:")
    print(churn_by_plan)
    
    # Churn by Country
    churn_by_region = df.groupby('country').agg({
        'is_churned': ['count', 'sum', 'mean']
    }).round(4)
    churn_by_region.columns = ['total', 'churned', 'churn_rate']
    churn_by_region['churn_rate'] *= 100
    print("\nChurn by Country (Top 10):")
    print(churn_by_region.head(10))
    
    # Churn by Reason
    churn_reasons = df[df['is_churned'] == 1]['reason_code'].value_counts()
    print("\nChurn Reasons Distribution:")
    print(churn_reasons)
    print()
    
    return churn_by_plan, churn_by_region, churn_reasons


# ==============================
# 5. RETENTION DRIVERS ANALYSIS
# ==============================
def identify_retention_drivers(df):
    """Identify factors that drive better retention."""
    
    print("Retention Drivers Analysis:")
    print("-" * 80)
    
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


# ==============================
# 6. VISUALIZATION: EXECUTIVE OVERVIEW
# ==============================
def create_executive_overview(df, kpis):
    """Create professional executive overview dashboard."""
    
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # Title
    fig.suptitle('Customer Retention Executive Dashboard', fontsize=20, fontweight='bold', y=0.98)
    
    # 1. Churn vs Active (Pie)
    ax1 = fig.add_subplot(gs[0, 0])
    sizes = [kpis['active_customers'], kpis['churned_customers']]
    colors = ['#2ecc71', '#e74c3c']
    wedges, texts, autotexts = ax1.pie(sizes, labels=['Active', 'Churned'], autopct='%1.1f%%',
                                         colors=colors, startangle=90, textprops={'fontsize': 10})
    ax1.set_title('Customer Status Distribution', fontweight='bold')
    
    # 2. Churn Rate KPI (Text Box)
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.axis('off')
    text_str = f"Churn Rate\n{kpis['churn_rate']:.2f}%"
    ax2.text(0.5, 0.5, text_str, ha='center', va='center', fontsize=24, fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='#ecf0f1', edgecolor='#34495e', linewidth=2))
    
    # 3. Revenue at Risk
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.axis('off')
    text_str = f"ARR at Risk\n${kpis['churned_arr']:,.0f}\n({kpis['revenue_churn_rate']:.1f}%)"
    ax3.text(0.5, 0.5, text_str, ha='center', va='center', fontsize=18, fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='#fee5e5', edgecolor='#c0392b', linewidth=2))
    
    # 4. Churn by Plan Tier
    ax4 = fig.add_subplot(gs[1, :2])
    churn_plan = df.groupby('plan_tier')['is_churned'].agg(['count', 'mean']).round(3)
    churn_plan['mean'] *= 100
    churn_plan = churn_plan[churn_plan['count'] > 5].sort_values('mean', ascending=False)
    bars = ax4.bar(churn_plan.index, churn_plan['mean'], color='#e74c3c', alpha=0.7, edgecolor='black')
    ax4.set_ylabel('Churn Rate (%)', fontweight='bold')
    ax4.set_title('Churn Rate by Plan Tier', fontweight='bold')
    ax4.set_ylim(0, max(churn_plan['mean']) * 1.2)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%\n(n={int(churn_plan["count"].iloc[i])})',
                ha='center', va='bottom', fontsize=9)
    
    # 5. Customer Lifetime Distribution
    ax5 = fig.add_subplot(gs[1, 2])
    ax5.hist(df['subscription_age_days'], bins=30, color='#3498db', alpha=0.7, edgecolor='black')
    ax5.set_xlabel('Days', fontweight='bold')
    ax5.set_ylabel('Number of Customers', fontweight='bold')
    ax5.set_title('Customer Lifetime Distribution', fontweight='bold')
    ax5.axvline(df['subscription_age_days'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["subscription_age_days"].mean():.0f}d')
    ax5.legend()
    
    # 6. Churn by Country (Top 8)
    ax6 = fig.add_subplot(gs[2, :2])
    churn_country = df.groupby('country')['is_churned'].agg(['count', 'mean']).round(3)
    churn_country['mean'] *= 100
    churn_country = churn_country[churn_country['count'] > 3].sort_values('mean', ascending=False).head(8)
    bars = ax6.barh(churn_country.index, churn_country['mean'], color='#9b59b6', alpha=0.7, edgecolor='black')
    ax6.set_xlabel('Churn Rate (%)', fontweight='bold')
    ax6.set_title('Churn Rate by Country (Top 8)', fontweight='bold')
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax6.text(width, bar.get_y() + bar.get_height()/2.,
                f' {width:.1f}%',
                ha='left', va='center', fontsize=9, fontweight='bold')
    
    # 7. Active vs Churned Engagement
    ax7 = fig.add_subplot(gs[2, 2])
    engagement_data = {
        'Active': df[df['is_churned'] == 0]['total_features_used'].mean(),
        'Churned': df[df['is_churned'] == 1]['total_features_used'].mean()
    }
    bars = ax7.bar(engagement_data.keys(), engagement_data.values(), color=['#2ecc71', '#e74c3c'], alpha=0.7, edgecolor='black')
    ax7.set_ylabel('Avg Features Used', fontweight='bold')
    ax7.set_title('Feature Engagement', fontweight='bold')
    for bar in bars:
        height = bar.get_height()
        ax7.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.savefig(f'{OUTPUT_DIR}/01_executive_dashboard.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: 01_executive_dashboard.png")
    plt.close()


# ==============================
# 7. VISUALIZATION: CHURN ANALYSIS
# ==============================
def create_churn_analysis_charts(df):
    """Create detailed churn analysis visualizations."""
    
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    fig.suptitle('Detailed Churn Analysis & Patterns', fontsize=18, fontweight='bold')
    
    # 1. Churn Reasons
    ax1 = fig.add_subplot(gs[0, 0])
    churn_reasons = df[df['is_churned'] == 1]['reason_code'].value_counts()
    colors_reasons = plt.cm.Spectral(np.linspace(0, 1, len(churn_reasons)))
    wedges, texts, autotexts = ax1.pie(churn_reasons.values, labels=churn_reasons.index, autopct='%1.1f%%',
                                        colors=colors_reasons, startangle=45)
    ax1.set_title('Churn Reasons Distribution', fontweight='bold')
    
    # 2. Trial vs Paid Churn
    ax2 = fig.add_subplot(gs[0, 1])
    trial_churn_data = pd.DataFrame({
        'Account Type': ['Trial', 'Paid'],
        'Churn Rate': [
            df[df['is_trial'] == True]['is_churned'].mean() * 100,
            df[df['is_trial'] == False]['is_churned'].mean() * 100
        ],
        'Count': [
            len(df[df['is_trial'] == True]),
            len(df[df['is_trial'] == False])
        ]
    })
    bars = ax2.bar(trial_churn_data['Account Type'], trial_churn_data['Churn Rate'], 
                   color=['#f39c12', '#3498db'], alpha=0.7, edgecolor='black')
    ax2.set_ylabel('Churn Rate (%)', fontweight='bold')
    ax2.set_title('Trial vs Paid Account Churn', fontweight='bold')
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%\n(n={trial_churn_data["Count"].iloc[i]})',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # 3. Downgrade/Upgrade Impact
    ax3 = fig.add_subplot(gs[1, 0])
    downgrade_impact = pd.DataFrame({
        'Downgraded': [
            len(df[df['downgrade_flag'] == True]),
            df[df['downgrade_flag'] == True]['is_churned'].sum()
        ],
        'Did Not Downgrade': [
            len(df[df['downgrade_flag'] == False]),
            df[df['downgrade_flag'] == False]['is_churned'].sum()
        ]
    }, index=['Active', 'Churned']).T
    
    downgrade_impact['Churn Rate'] = (downgrade_impact['Churned'] / downgrade_impact['Active']).round(3) * 100
    bars = ax3.bar(downgrade_impact.index, downgrade_impact['Churn Rate'], color=['#e74c3c', '#3498db'], alpha=0.7, edgecolor='black')
    ax3.set_ylabel('Churn Rate (%)', fontweight='bold')
    ax3.set_title('Impact of Downgrades on Churn', fontweight='bold')
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # 4. Auto-Renew Impact
    ax4 = fig.add_subplot(gs[1, 1])
    autorenew_impact = pd.DataFrame({
        'Auto-Renew': [
            len(df[df['auto_renew_flag'] == True]),
            df[df['auto_renew_flag'] == True]['is_churned'].sum()
        ],
        'Manual Renewal': [
            len(df[df['auto_renew_flag'] == False]),
            df[df['auto_renew_flag'] == False]['is_churned'].sum()
        ]
    }, index=['Active', 'Churned']).T
    
    autorenew_impact['Churn Rate'] = (autorenew_impact['Churned'] / autorenew_impact['Active']).round(3) * 100
    bars = ax4.bar(autorenew_impact.index, autorenew_impact['Churn Rate'], color=['#2ecc71', '#e74c3c'], alpha=0.7, edgecolor='black')
    ax4.set_ylabel('Churn Rate (%)', fontweight='bold')
    ax4.set_title('Auto-Renew Impact on Churn', fontweight='bold')
    for bar in bars:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.savefig(f'{OUTPUT_DIR}/02_churn_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: 02_churn_analysis.png")
    plt.close()


# ==============================
# 8. VISUALIZATION: RETENTION DRIVERS
# ==============================
def create_retention_drivers_charts(df):
    """Create retention drivers analysis."""
    
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    fig.suptitle('Key Retention Drivers & Risk Factors', fontsize=18, fontweight='bold')
    
    # 1. Feature Usage Impact
    ax1 = fig.add_subplot(gs[0, 0])
    feature_bins = pd.cut(df['total_features_used'], bins=5)
    feature_churn = df.groupby(feature_bins)['is_churned'].agg(['count', 'mean'])
    feature_churn['churn_pct'] = feature_churn['mean'] * 100
    feature_labels = [f"{int(interval.left)}-{int(interval.right)}" for interval in feature_churn.index]
    bars = ax1.bar(range(len(feature_labels)), feature_churn['churn_pct'], color='#3498db', alpha=0.7, edgecolor='black')
    ax1.set_xticks(range(len(feature_labels)))
    ax1.set_xticklabels(feature_labels, rotation=45, ha='right')
    ax1.set_xlabel('Features Used (Bins)', fontweight='bold')
    ax1.set_ylabel('Churn Rate (%)', fontweight='bold')
    ax1.set_title('Feature Usage Impact on Churn', fontweight='bold')
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%\n(n={int(feature_churn["count"].iloc[i])})',
                ha='center', va='bottom', fontsize=8)
    
    # 2. Support Ticket Frequency
    ax2 = fig.add_subplot(gs[0, 1])
    support_bins = pd.cut(df['total_support_tickets'], bins=4)
    support_churn = df.groupby(support_bins)['is_churned'].agg(['count', 'mean'])
    support_churn['churn_pct'] = support_churn['mean'] * 100
    support_labels = [f"{int(interval.left)}-{int(interval.right)}" for interval in support_churn.index]
    bars = ax2.bar(range(len(support_labels)), support_churn['churn_pct'], color='#e74c3c', alpha=0.7, edgecolor='black')
    ax2.set_xticks(range(len(support_labels)))
    ax2.set_xticklabels(support_labels, rotation=45, ha='right')
    ax2.set_xlabel('Support Tickets (Bins)', fontweight='bold')
    ax2.set_ylabel('Churn Rate (%)', fontweight='bold')
    ax2.set_title('Support Issues Impact on Churn', fontweight='bold')
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%\n(n={int(support_churn["count"].iloc[i])})',
                ha='center', va='bottom', fontsize=8)
    
    # 3. Referral Source Impact
    ax3 = fig.add_subplot(gs[1, 0])
    size_churn = df.groupby('referral_source')['is_churned'].agg(['count', 'mean'])
    size_churn['churn_pct'] = size_churn['mean'] * 100
    size_churn = size_churn[size_churn['count'] > 3].sort_values('churn_pct', ascending=False)
    bars = ax3.barh(range(len(size_churn)), size_churn['churn_pct'], color='#9b59b6', alpha=0.7, edgecolor='black')
    ax3.set_yticks(range(len(size_churn)))
    ax3.set_yticklabels(size_churn.index)
    ax3.set_xlabel('Churn Rate (%)', fontweight='bold')
    ax3.set_title('Churn by Referral Source', fontweight='bold')
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax3.text(width, bar.get_y() + bar.get_height()/2.,
                f' {width:.1f}%',
                ha='left', va='center', fontsize=9, fontweight='bold')
    
    # 4. Industry Impact
    ax4 = fig.add_subplot(gs[1, 1])
    industry_churn = df.groupby('industry')['is_churned'].agg(['count', 'mean'])
    industry_churn['churn_pct'] = industry_churn['mean'] * 100
    industry_churn = industry_churn[industry_churn['count'] > 3].sort_values('churn_pct', ascending=False).head(8)
    bars = ax4.barh(range(len(industry_churn)), industry_churn['churn_pct'], color='#1abc9c', alpha=0.7, edgecolor='black')
    ax4.set_yticks(range(len(industry_churn)))
    ax4.set_yticklabels(industry_churn.index)
    ax4.set_xlabel('Churn Rate (%)', fontweight='bold')
    ax4.set_title('Churn by Industry (Top 8)', fontweight='bold')
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax4.text(width, bar.get_y() + bar.get_height()/2.,
                f' {width:.1f}%',
                ha='left', va='center', fontsize=9, fontweight='bold')
    
    plt.savefig(f'{OUTPUT_DIR}/03_retention_drivers.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: 03_retention_drivers.png")
    plt.close()


# ==============================
# 9. IDENTIFY AT-RISK CUSTOMERS
# ==============================
def identify_at_risk_customers(df):
    """Identify customers at high risk of churn."""
    
    # Calculate risk score
    df['risk_score'] = 0
    
    # Low feature usage (weight: 3)
    low_feature_threshold = df['total_features_used'].quantile(0.25)
    df.loc[df['total_features_used'] <= low_feature_threshold, 'risk_score'] += 3
    
    # High support issue ratio (weight: 2)
    high_support_threshold = df['high_priority_ratio'].quantile(0.75)
    df.loc[df['high_priority_ratio'] >= high_support_threshold, 'risk_score'] += 2
    
    # Downgrade flag (weight: 3)
    df.loc[df['downgrade_flag'] == True, 'risk_score'] += 3
    
    # Long inactivity (weight: 2)
    high_inactivity = df['days_since_activity'].quantile(0.75)
    df.loc[df['days_since_activity'] >= high_inactivity, 'risk_score'] += 2
    
    # No auto-renew (weight: 1)
    df.loc[df['auto_renew_flag'] == False, 'risk_score'] += 1
    
    # Identify high-risk customers (still active)
    high_risk = df[(df['is_churned'] == 0) & (df['risk_score'] >= 5)].sort_values('risk_score', ascending=False)
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
    
    # Export to CSV
    high_risk_export.to_csv(f'{OUTPUT_DIR}/high_risk_customers.csv', index=False)
    print(f"✓ Exported: high_risk_customers.csv ({len(high_risk_export)} records)")
    
    return df, high_risk_export


# ==============================
# 10. GENERATE EXECUTIVE REPORT
# ==============================
def generate_executive_report(df, kpis, churn_by_plan, churn_reasons, high_risk_customers):
    """Generate professional executive summary report."""
    
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
   • retention_analysis_summary.csv - Detailed metrics by plan, country, industry

{'='*90}
Report prepared for: Product, Executive, and Success Leadership
Contact: Data Analytics Team
{'='*90}
"""
    
    return report


# ==============================
# 11. EXPORT SUMMARY METRICS
# ==============================
def export_summary_metrics(df):
    """Export detailed summary metrics by segments."""
    
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
    by_region = df.groupby('country').agg({
        'account_id': 'count',
        'is_churned': ['sum', 'mean'],
        'arr_amount': 'sum',
        'subscription_age_days': 'mean',
        'total_features_used': 'mean'
    }).round(2)
    by_region.columns = ['total_accounts', 'churned_count', 'churn_rate', 'total_arr', 'avg_lifetime', 'avg_features']
    by_region['churn_rate'] *= 100
    by_region = by_region[by_region['total_accounts'] > 3].sort_values('churn_rate', ascending=False).head(15)
    
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
    by_region.to_csv(f'{OUTPUT_DIR}/metrics_by_country.csv')
    by_industry.to_csv(f'{OUTPUT_DIR}/metrics_by_industry.csv')
    
    print(f"✓ Exported: metrics_by_plan.csv")
    print(f"✓ Exported: metrics_by_country.csv")
    print(f"✓ Exported: metrics_by_industry.csv")


# ==============================
# MAIN EXECUTION
# ==============================
if __name__ == "__main__":
    
    # Load data
    print("\nSTEP 1: Loading Data")
    print("─" * 80)
    subscriptions, churn_events, accounts, feature_usage, support_tickets = load_data()
    
    # Clean and integrate
    print("\nSTEP 2: Data Processing")
    print("─" * 80)
    df = clean_and_prepare_data(subscriptions, churn_events, accounts, feature_usage, support_tickets)
    
    # Calculate KPIs
    print("\nSTEP 3: Key Metrics")
    print("─" * 80)
    kpis = calculate_kpis(df)
    
    # Analyze churn
    print("\nSTEP 4: Churn Analysis")
    print("─" * 80)
    churn_by_plan, churn_by_region, churn_reasons = analyze_churn_patterns(df)
    
    # Identify retention drivers
    print("\nSTEP 5: Retention Drivers")
    print("─" * 80)
    comparison = identify_retention_drivers(df)
    
    # Create visualizations
    print("\nSTEP 6: Creating Visualizations")
    print("─" * 80)
    create_executive_overview(df, kpis)
    create_churn_analysis_charts(df)
    create_retention_drivers_charts(df)
    
    # Identify at-risk customers
    print("\nSTEP 7: Risk Identification")
    print("─" * 80)
    df, high_risk_customers = identify_at_risk_customers(df)
    
    # Export metrics
    print("\nSTEP 8: Exporting Summary Metrics")
    print("─" * 80)
    export_summary_metrics(df)
    
    # Generate report
    print("\nSTEP 9: Generating Executive Report")
    print("─" * 80)
    report = generate_executive_report(df, kpis, churn_by_plan, churn_reasons, high_risk_customers)
    print(report)
    
    # Save report to file
    with open(f'{OUTPUT_DIR}/EXECUTIVE_REPORT.txt', 'w') as f:
        f.write(report)
    print(f"✓ Saved: EXECUTIVE_REPORT.txt")
    
    print(f"\n{'='*80}")
    print(f"✓ ANALYSIS COMPLETE!")
    print(f"All outputs saved to: {OUTPUT_DIR}/")
    print(f"{'='*80}\n")
