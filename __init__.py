"""
Retention Analysis Package
A modular framework for analyzing customer churn and retention
"""

__version__ = "1.0.0"
__author__ = "Data Analytics Team"

from config import (
    OUTPUT_DIR,
    DATA_PATH,
    REPORT_DATE,
    RISK_SCORE_THRESHOLD
)

__all__ = [
    'OUTPUT_DIR',
    'DATA_PATH', 
    'REPORT_DATE',
    'RISK_SCORE_THRESHOLD'
]
