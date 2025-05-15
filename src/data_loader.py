
import pandas as pd

def load_data():
  drivers = pd.read_csv("/content/drive/MyDrive/ridewise_data/drivers.csv")
  trips =pd.read_csv("/content/drive/MyDrive/ridewise_data/trips.csv")
  sessions = pd.read_csv("/content/drive/MyDrive/ridewise_data/sessions.csv")
  riders = pd.read_csv('/content/drive/MyDrive/ridewise_data/riders.csv')
  promotions = pd.read_csv('/content/drive/MyDrive/ridewise_data/promotions.csv')

  return drivers, trips, sessions, riders, promotions

if __name__ == "__main__":
    drivers, trips, sessions, riders, promotions = load_data()
    
    print("\nDrivers Preview:")
    print(drivers.head())

    print("\nTrips Preview:")
    print(trips.head())
   
    print("\nSessions Preview:")
    print(sessions.head())

    print("\nRiders Preview:")
    print(riders.head())

    print("\nPromotions Preview:")
    print(promotions.head())

    print("\nData Loading Completed")
