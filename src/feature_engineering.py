import pandas as pd
import numpy as np
from datetime import datetime

# Load your cleaned files
riders = pd.read_csv('/content/ridewise-customer-driver-insights/data/processed/riders_cleaned.csv')
trips = pd.read_csv('/content/ridewise-customer-driver-insights/data/processed/trip_cleaned.csv')
sessions = pd.read_csv('/content/ridewise-customer-driver-insights/data/processed/session_cleaned.csv')
promotions = pd.read_csv('/content/ridewise-customer-driver-insights/data/processed/promotion_cleaned.csv')
drivers = pd.read_csv('/content/ridewise-customer-driver-insights/data/processed/drivers_cleaned.csv')

# ---------- Feature Engineering ----------

# 1. Riders: recency from signup_date
riders['signup_date'] = pd.to_datetime(riders['signup_date'], utc=True)
today = pd.to_datetime("2025-05-20").tz_localize("UTC")
riders['recency_days'] = (today - riders['signup_date']).dt.days

# 2. Trips: user-level stats
trip_stats = trips.groupby("user_id").agg(
    total_trips=('trip_id', 'count'),
    avg_fare=('fare', 'mean'),
    avg_tip=('tip', 'mean'),
    avg_surge_multiplier=('surge_multiplier', 'mean')
).reset_index()

# 3. Sessions: engagement stats
sessions['session_time'] = pd.to_datetime(sessions['session_time'], utc=True)
session_stats = sessions.groupby("rider_id").agg(
    total_sessions=('session_id', 'count'),
    avg_time_on_app=('time_on_app', 'mean'),
    avg_pages_visited=('pages_visited', 'mean'),
    last_session_time=('session_time', 'max')
).reset_index()
session_stats['session_recency_days'] = (today - session_stats['last_session_time']).dt.days
session_stats.drop(columns='last_session_time', inplace=True)

# ---------- Merge All Features ----------
enriched = riders.merge(trip_stats, on='user_id', how='left')
enriched = enriched.merge(session_stats, left_on='user_id', right_on='rider_id', how='left')
enriched.drop(columns='rider_id', inplace=True)

# ---------- Save to File ----------
output_path = '/content/ridewise-customer-driver-insights/data/processed/riders_enriched.csv'
enriched.to_csv(output_path, index=False)
print(f"✅ Enriched data saved to: {output_path}")
