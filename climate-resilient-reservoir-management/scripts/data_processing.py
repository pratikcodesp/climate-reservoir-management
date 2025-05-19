import pandas as pd
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

RAW_DIR = 'data/raw'
PROCESSED_DIR = 'data/processed'

def load_and_clean_data():
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    # 1. Shasta Reservoir Data
    logging.info("Cleaning Shasta Reservoir Data...")
    reservoir = pd.read_csv(os.path.join(RAW_DIR, 'shasta_reservoir.csv'))
    reservoir.columns = reservoir.columns.str.strip()
    reservoir.to_csv(os.path.join(PROCESSED_DIR, 'shasta_clean.csv'), index=False)
    logging.info("Shasta Reservoir Data cleaned and saved.")

    # 2. NOAA GHCN Precipitation Data
    logging.info("Cleaning NOAA GHCN Precipitation Data...")
    precipitation_path = os.path.join(RAW_DIR, 'precipitation_data.csv')
    precipitation = pd.read_csv(precipitation_path)
    logging.info(f"Precipitation data shape: {precipitation.shape}")

    if precipitation.shape[1] == 8:
        precipitation.columns = ['station_id', 'date', 'element', 'value', 'm_flag', 'q_flag', 's_flag', 'obs_time']
        prcp = precipitation[precipitation['element'] == 'PRCP']
    else:
        logging.warning("Precipitation data does not have 8 columns. Skipping filtering by 'PRCP'.")
        prcp = precipitation

    prcp.to_csv(os.path.join(PROCESSED_DIR, 'precip_clean.csv'), index=False)
    logging.info("NOAA GHCN Precipitation Data cleaned and saved.")

    # 3. Agriculture Land Use Data
    logging.info("Cleaning Agriculture Land Use Data...")
    crops = pd.read_csv(os.path.join(RAW_DIR, 'agriculture_land_use.csv'))
    crops.to_csv(os.path.join(PROCESSED_DIR, 'crops_clean.csv'), index=False)
    logging.info("Agriculture Land Use Data cleaned and saved.")

    # 4. Streamflow Data
    logging.info("Cleaning Streamflow Data...")
    streamflow = pd.read_csv(os.path.join(RAW_DIR, 'streamflow_data.csv'))
    streamflow.to_csv(os.path.join(PROCESSED_DIR, 'streamflow_clean.csv'), index=False)
    logging.info("Streamflow Data cleaned and saved.")

    # 5. Climate Projections Data
    logging.info("Cleaning Climate Temperature Data...")
    temp_df = pd.read_csv(os.path.join(RAW_DIR, 'climate_projections.csv'))
    temp_df.to_csv(os.path.join(PROCESSED_DIR, 'temperature_clean.csv'), index=False)
    logging.info("Climate Temperature Data cleaned and saved.")

if __name__ == '__main__':
    load_and_clean_data()
    logging.info("✅ All datasets cleaned and saved to 'data/processed'")
    logging.info("✅ Data processing complete.")
