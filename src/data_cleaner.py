
import pandas as pd
import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_loader import load_data

def clean_data():
    # Load datasets
    drivers, trips, sessions, riders, promotions = load_data()

    # Create output path
    output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
    os.makedirs(output_path, exist_ok=True)

    # -------------------- Handle Missing Values --------------------
    print("\n✅ Checking Missing Values:")
    print("Trip Dataset:\n", trips.isnull().sum())
    print("Session Dataset:\n", sessions.isnull().sum())
    print("Drivers Dataset:\n", drivers.isnull().sum())
    print("Promotion Dataset:\n", promotions.isnull().sum())
    print("Riders Dataset:\n", riders.isnull().sum())

    if 'referred_by' in riders.columns:
        mode_val = riders['referred_by'].mode()[0]
        riders['referred_by'] = riders['referred_by'].fillna(mode_val)

    # -------------------- Handle Duplicates --------------------
    print("\n✅ Checking Duplicates:")
    print("Trip Duplicates:", trips.duplicated().sum())
    print("Session Duplicates:", sessions.duplicated().sum())
    print("Drivers Duplicates:", drivers.duplicated().sum())
    print("Promotion Duplicates:", promotions.duplicated().sum())
    print("Riders Duplicates:", riders.duplicated().sum())

    trips = trips.drop_duplicates()
    sessions = sessions.drop_duplicates()
    drivers = drivers.drop_duplicates()
    promotions = promotions.drop_duplicates()
    riders = riders.drop_duplicates()

    # -------------------- Convert Dates --------------------
    date_cols = {
        'trips': ['pickup_time', 'dropoff_time'],
        'sessions': ['session_time'],
        'drivers': ['signup_date', 'last_active'],
        'riders': ['signup_date']
    }

    for col in date_cols['trips']:
        if col in trips.columns:
            trips[col] = pd.to_datetime(trips[col], utc=True)

    for col in date_cols['sessions']:
        if col in sessions.columns:
            sessions[col] = pd.to_datetime(sessions[col], utc=True)

    for col in date_cols['drivers']:
        if col in drivers.columns:
            drivers[col] = pd.to_datetime(drivers[col], utc=True)

    for col in date_cols['riders']:
        if col in riders.columns:
            riders[col] = pd.to_datetime(riders[col], utc=True)

    # ✅ Confirm types
    print("\n✅ Data Types After Conversion:")
    print("Trip:\n", trips.dtypes)
    print("Session:\n", sessions.dtypes)
    print("Drivers:\n", drivers.dtypes)
    print("Promotion:\n", promotions.dtypes)
    print("Riders:\n", riders.dtypes)

    # ✅ Save cleaned datasets
    trips.to_csv(os.path.join(output_path, "trip_cleaned.csv"), index=False)
    sessions.to_csv(os.path.join(output_path, "session_cleaned.csv"), index=False)
    drivers.to_csv(os.path.join(output_path, "drivers_cleaned.csv"), index=False)
    promotions.to_csv(os.path.join(output_path, "promotion_cleaned.csv"), index=False)
    riders.to_csv(os.path.join(output_path, "riders_cleaned.csv"), index=False)

    print(f"\n✅ Cleaned files saved to: {output_path}")

    return drivers, trips, sessions, riders, promotions


if __name__ == "__main__":
    drivers, trips, sessions, riders, promotions = clean_data()
