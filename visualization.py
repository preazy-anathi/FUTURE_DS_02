"""
Visualization Functions
Creates professional charts and dashboards for retention analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from config import (
    OUTPUT_DIR, PLOT_STYLE, PLOT_PALETTE, DPI, FIGURE_SIZE_LARGE,
    COLOR_ACTIVE, COLOR_CHURNED, COLOR_TRIAL, COLOR_PAID, COLOR_PRIMARY, COLOR_SECONDARY
)

# Set styling
plt.style.use(PLOT_STYLE)
sns.set_palette(PLOT_PALETTE)


def create_executive_overview(df, kpis):
    """
    Create professional executive overview dashboard.
    
    Args:
        df: Cleaned dataframe
        kpis: Dictionary of KPI values
    """
    
    fig = plt.figure(figsize=FIGURE_SIZE_LARGE)
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    fig.suptitle('Customer Retention Executive Dashboard', fontsize=20, fontweight='bold', y=0.98)
    
    # 1. Churn vs Active (Pie)
    ax1 = fig.add_subplot(gs[0, 0])
    sizes = [kpis['active_customers'], kpis['churned_customers']]
    colors = [COLOR_ACTIVE, COLOR_CHURNED]
    wedges, texts, autotexts = ax1.pie(sizes, labels=['Active', 'Churned'], autopct='%1.1f%%',
                                         colors=colors, startangle=90, textprops={'fontsize': 10})
    ax1.set_title('Customer Status Distribution', fontweight='bold')
    
    # 2. Churn Rate KPI
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
    bars = ax4.bar(churn_plan.index, churn_plan['mean'], color=COLOR_CHURNED, alpha=0.7, edgecolor='black')
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
    ax5.axvline(df['subscription_age_days'].mean(), color='red', linestyle='--', linewidth=2, 
                label=f'Mean: {df["subscription_age_days"].mean():.0f}d')
    ax5.legend()
    
    # 6. Churn by Country
    ax6 = fig.add_subplot(gs[2, :2])
    churn_country = df.groupby('country')['is_churned'].agg(['count', 'mean']).round(3)
    churn_country['mean'] *= 100
    churn_country = churn_country[churn_country['count'] > 3].sort_values('mean', ascending=False).head(8)
    bars = ax6.barh(churn_country.index, churn_country['mean'], color=COLOR_PRIMARY, alpha=0.7, edgecolor='black')
    ax6.set_xlabel('Churn Rate (%)', fontweight='bold')
    ax6.set_title('Churn Rate by Country (Top 8)', fontweight='bold')
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax6.text(width, bar.get_y() + bar.get_height()/2.,
                f' {width:.1f}%',
                ha='left', va='center', fontsize=9, fontweight='bold')
    
    # 7. Feature Engagement
    ax7 = fig.add_subplot(gs[2, 2])
    engagement_data = {
        'Active': df[df['is_churned'] == 0]['total_features_used'].mean(),
        'Churned': df[df['is_churned'] == 1]['total_features_used'].mean()
    }
    bars = ax7.bar(engagement_data.keys(), engagement_data.values(), 
                   color=[COLOR_ACTIVE, COLOR_CHURNED], alpha=0.7, edgecolor='black')
    ax7.set_ylabel('Avg Features Used', fontweight='bold')
    ax7.set_title('Feature Engagement', fontweight='bold')
    for bar in bars:
        height = bar.get_height()
        ax7.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.savefig(f'{OUTPUT_DIR}/01_executive_dashboard.png', dpi=DPI, bbox_inches='tight')
    print("✓ Saved: 01_executive_dashboard.png")
    plt.close()


def create_churn_analysis_charts(df):
    """
    Create detailed churn analysis visualizations.
    
    Args:
        df: Cleaned dataframe
    """
    
    fig = plt.figure(figsize=FIGURE_SIZE_LARGE)
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
                   color=[COLOR_TRIAL, COLOR_PAID], alpha=0.7, edgecolor='black')
    ax2.set_ylabel('Churn Rate (%)', fontweight='bold')
    ax2.set_title('Trial vs Paid Account Churn', fontweight='bold')
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%\n(n={trial_churn_data["Count"].iloc[i]})',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # 3. Downgrade Impact
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
    bars = ax3.bar(downgrade_impact.index, downgrade_impact['Churn Rate'], 
                   color=[COLOR_CHURNED, '#3498db'], alpha=0.7, edgecolor='black')
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
    bars = ax4.bar(autorenew_impact.index, autorenew_impact['Churn Rate'], 
                   color=[COLOR_ACTIVE, COLOR_CHURNED], alpha=0.7, edgecolor='black')
    ax4.set_ylabel('Churn Rate (%)', fontweight='bold')
    ax4.set_title('Auto-Renew Impact on Churn', fontweight='bold')
    for bar in bars:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.savefig(f'{OUTPUT_DIR}/02_churn_analysis.png', dpi=DPI, bbox_inches='tight')
    print("✓ Saved: 02_churn_analysis.png")
    plt.close()


def create_retention_drivers_charts(df):
    """
    Create retention drivers analysis visualizations.
    
    Args:
        df: Cleaned dataframe
    """
    
    fig = plt.figure(figsize=FIGURE_SIZE_LARGE)
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
    bars = ax2.bar(range(len(support_labels)), support_churn['churn_pct'], color=COLOR_CHURNED, alpha=0.7, edgecolor='black')
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
    referral_churn = df.groupby('referral_source')['is_churned'].agg(['count', 'mean'])
    referral_churn['churn_pct'] = referral_churn['mean'] * 100
    referral_churn = referral_churn[referral_churn['count'] > 3].sort_values('churn_pct', ascending=False)
    bars = ax3.barh(range(len(referral_churn)), referral_churn['churn_pct'], color=COLOR_PRIMARY, alpha=0.7, edgecolor='black')
    ax3.set_yticks(range(len(referral_churn)))
    ax3.set_yticklabels(referral_churn.index)
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
    bars = ax4.barh(range(len(industry_churn)), industry_churn['churn_pct'], color=COLOR_SECONDARY, alpha=0.7, edgecolor='black')
    ax4.set_yticks(range(len(industry_churn)))
    ax4.set_yticklabels(industry_churn.index)
    ax4.set_xlabel('Churn Rate (%)', fontweight='bold')
    ax4.set_title('Churn by Industry (Top 8)', fontweight='bold')
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax4.text(width, bar.get_y() + bar.get_height()/2.,
                f' {width:.1f}%',
                ha='left', va='center', fontsize=9, fontweight='bold')
    
    plt.savefig(f'{OUTPUT_DIR}/03_retention_drivers.png', dpi=DPI, bbox_inches='tight')
    print("✓ Saved: 03_retention_drivers.png")
    plt.close()
