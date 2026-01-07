"""
Create a comprehensive dataset for Station 1068 including occupancy, prices, and weather data
"""

import pandas as pd
import numpy as np

# Load station information
print("Loading station information...")
station_info = pd.read_csv('UrbanEV-main/data/inf.csv')
station_1068 = station_info[station_info['TAZID'] == 1068]

print(f"Station 1068 Details:")
print(f"  Location: ({station_1068['longitude'].values[0]:.4f}, {station_1068['latitude'].values[0]:.4f})")
print(f"  Charging piles: {station_1068['charge_count'].values[0]}")
print(f"  Area: {station_1068['area'].values[0]:.2f} m²")
print()

# Load occupancy data
print("Loading occupancy data...")
occupancy_df = pd.read_csv('UrbanEV-main/data/occupancy.csv')
occupancy_df['time'] = pd.to_datetime(occupancy_df['time'])
occupancy_df.set_index('time', inplace=True)

# Extract station 1068 occupancy
station_data = occupancy_df[['1068']].copy()
station_data.columns = ['occupancy']

# Load electricity price data
print("Loading electricity price data...")
e_price_df = pd.read_csv('UrbanEV-main/data/e_price.csv')
e_price_df['time'] = pd.to_datetime(e_price_df['time'])
e_price_df.set_index('time', inplace=True)

# Extract station 1068 price
station_data['e_price'] = e_price_df['1068']

# Load service price data
print("Loading service price data...")
s_price_df = pd.read_csv('UrbanEV-main/data/s_price.csv')
s_price_df['time'] = pd.to_datetime(s_price_df['time'])
s_price_df.set_index('time', inplace=True)

# Extract station 1068 service price
station_data['s_price'] = s_price_df['1068']

# Calculate total price
station_data['total_price'] = station_data['e_price'] + station_data['s_price']

# Load weather data (central station)
print("Loading weather data...")
weather_df = pd.read_csv('UrbanEV-main/data/weather_central.csv')
weather_df['time'] = pd.to_datetime(weather_df['time'])
weather_df.set_index('time', inplace=True)

# Merge weather data
station_data = station_data.join(weather_df, how='left')

# Add temporal features
print("Adding temporal features...")
station_data['hour'] = station_data.index.hour
station_data['day_of_week'] = station_data.index.dayofweek
station_data['day_of_month'] = station_data.index.day
station_data['month'] = station_data.index.month
station_data['is_weekend'] = station_data['day_of_week'].isin([5, 6]).astype(int)

# Add time-based categories
def get_time_period(hour):
    if 6 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 18:
        return 'afternoon'
    elif 18 <= hour < 24:
        return 'evening'
    else:
        return 'night'

station_data['time_period'] = station_data['hour'].apply(get_time_period)

# Reorder columns for better readability
column_order = [
    'occupancy',
    'e_price', 's_price', 'total_price',
    'T', 'P0', 'P', 'U', 'nRAIN', 'Td',
    'hour', 'day_of_week', 'day_of_month', 'month', 
    'is_weekend', 'time_period'
]
station_data = station_data[column_order]

# Save to CSV
output_file = 'station_1068_dataset.csv'
station_data.to_csv(output_file)
print(f"\n✅ Dataset saved to: {output_file}")

# Display summary statistics
print("\n" + "="*60)
print("STATION 1068 - DATASET SUMMARY")
print("="*60)
print(f"\nDataset shape: {station_data.shape}")
print(f"Date range: {station_data.index.min()} to {station_data.index.max()}")
print(f"Total records: {len(station_data)}")

print("\n📊 Column Overview:")
for col in station_data.columns:
    missing = station_data[col].isna().sum()
    missing_pct = (missing / len(station_data)) * 100
    print(f"  {col:20s} - Missing: {missing:4d} ({missing_pct:5.2f}%)")

print("\n📈 Occupancy Statistics:")
print(station_data['occupancy'].describe())

print("\n💰 Price Statistics:")
print(f"  Electricity price range: {station_data['e_price'].min():.2f} - {station_data['e_price'].max():.2f}")
print(f"  Service price range:     {station_data['s_price'].min():.2f} - {station_data['s_price'].max():.2f}")
print(f"  Total price range:       {station_data['total_price'].min():.2f} - {station_data['total_price'].max():.2f}")

print("\n🌤️  Weather Statistics:")
print(f"  Temperature (T):   {station_data['T'].min():.1f}°C - {station_data['T'].max():.1f}°C")
print(f"  Humidity (U):      {station_data['U'].min():.0f}% - {station_data['U'].max():.0f}%")
print(f"  Rainy hours:       {station_data['nRAIN'].sum():.0f} hours ({(station_data['nRAIN'].sum()/len(station_data)*100):.1f}%)")

print("\n⏰ Temporal Distribution:")
print(f"  Weekend hours: {station_data['is_weekend'].sum()} ({station_data['is_weekend'].mean()*100:.1f}%)")
print("\n  Time period distribution:")
for period in ['morning', 'afternoon', 'evening', 'night']:
    count = (station_data['time_period'] == period).sum()
    pct = count / len(station_data) * 100
    print(f"    {period:10s}: {count:4d} hours ({pct:5.1f}%)")

print("\n" + "="*60)
print(f"✅ Complete dataset created for Station 1068!")
print("="*60)
