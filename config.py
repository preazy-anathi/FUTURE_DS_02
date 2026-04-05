# Configuration and constants for retention analysis

import os
from datetime import datetime

# ==============================
# PATHS & DIRECTORIES
# ==============================
OUTPUT_DIR = "retention_outputs"
DATA_PATH = "../archive (1)"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==============================
# REPORT SETTINGS
# ==============================
REPORT_DATE = datetime.now().strftime("%Y-%m-%d")
REPORT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ==============================
# VISUALIZATION SETTINGS
# ==============================
PLOT_STYLE = 'seaborn-v0_8-darkgrid'
PLOT_PALETTE = "husl"
DPI = 300
FIGURE_SIZE_LARGE = (16, 10)
FIGURE_SIZE_MEDIUM = (12, 8)

# ==============================
# ANALYSIS PARAMETERS
# ==============================
# Risk scoring weights
RISK_WEIGHT_LOW_FEATURE_USAGE = 3
RISK_WEIGHT_HIGH_SUPPORT_ISSUES = 2
RISK_WEIGHT_DOWNGRADE = 3
RISK_WEIGHT_INACTIVITY = 2
RISK_WEIGHT_NO_AUTORENEW = 1

# Risk score threshold (minimum score to be flagged as high-risk)
RISK_SCORE_THRESHOLD = 5

# Churn definition threshold
CHURN_INACTIVITY_DAYS = 30

# Data quality thresholds
MIN_RECORDS_FOR_ANALYSIS = 3
MIN_RECORDS_FOR_CHART = 5

# ==============================
# COLORS
# ==============================
COLOR_ACTIVE = '#2ecc71'
COLOR_CHURNED = '#e74c3c'
COLOR_TRIAL = '#f39c12'
COLOR_PAID = '#3498db'
COLOR_PRIMARY = '#9b59b6'
COLOR_SECONDARY = '#1abc9c'
