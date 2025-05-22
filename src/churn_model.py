# Churn Model

# TODO: Add implementation here


import pandas as pd
from datetime import datetime, timedelta

# Setting the current date
current_date = datetime(2025, 5, 20)

# Data loading
riders_df = pd.read_csv('ridewise-customer-driver-insights/data/processed/riders_enriched.csv')

# Computing last trip date
def calculate_last_trip_date(recency_days):
    if pd.notnull(recency_days):
        return current_date - timedelta(days=float(recency_days))
    return None

riders_df['last_trip_date'] = riders_df['recency_days'].apply(calculate_last_trip_date)

# Defining churned users: days_since_last_trip > 90
def is_churned(recency_days):
     
    if pd.notnull(recency_days) and float(recency_days) > 90:
        return 1
    return 0

riders_df['churned'] = riders_df['recency_days'].apply(is_churned)

# Saving the result to a new CSV
riders_df.to_csv('riders_churn_ready.csv', index=False)