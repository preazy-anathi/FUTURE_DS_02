"""
Data Loading and I/O Operations
Handles loading all source datasets and initial validation
"""

import pandas as pd
import os
from config import DATA_PATH


def load_data():
    """
    Load and validate all source datasets.
    
    Returns:
        tuple: (subscriptions, churn_events, accounts, feature_usage, support_tickets)
    """
    try:
        subscriptions = pd.read_csv(os.path.join(DATA_PATH, "ravenstack_subscriptions.csv"))
        churn_events = pd.read_csv(os.path.join(DATA_PATH, "ravenstack_churn_events.csv"))
        accounts = pd.read_csv(os.path.join(DATA_PATH, "ravenstack_accounts.csv"))
        feature_usage = pd.read_csv(os.path.join(DATA_PATH, "ravenstack_feature_usage.csv"))
        support_tickets = pd.read_csv(os.path.join(DATA_PATH, "ravenstack_support_tickets.csv"), encoding='utf-8')
        
        print(f"✓ Subscriptions: {len(subscriptions)} records")
        print(f"✓ Churn Events: {len(churn_events)} records")
        print(f"✓ Accounts: {len(accounts)} records")
        print(f"✓ Feature Usage: {len(feature_usage)} records")
        print(f"✓ Support Tickets: {len(support_tickets)} records\n")
        
        return subscriptions, churn_events, accounts, feature_usage, support_tickets
        
    except FileNotFoundError as e:
        print(f"❌ Error: Data file not found - {e}")
        raise
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        raise
