import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Paths to raw data files
PRECIPITATION_PATH = 'data/raw/precipitation_data.csv'
CLIMATE_PROJECTIONS_PATH = 'data/raw/climate_projections.csv'
AGRICULTURE_LAND_USE_PATH = 'data/raw/agriculture_land_use.csv'
STREAMFLOW_PATH = 'data/raw/streamflow_data.csv'
SHASTA_RESERVOIR_PATH = 'data/raw/shasta_reservoir.csv'

def load_data():
    # Load the datasets
    precipitation = pd.read_csv(PRECIPITATION_PATH)
    climate_projections = pd.read_csv(CLIMATE_PROJECTIONS_PATH)
    agriculture_land_use = pd.read_csv(AGRICULTURE_LAND_USE_PATH)
    streamflow = pd.read_csv(STREAMFLOW_PATH)
    shasta_reservoir = pd.read_csv(SHASTA_RESERVOIR_PATH)

    # Extract year from date columns
    precipitation['year'] = pd.to_datetime(precipitation['DATE'], errors='coerce').dt.year
    streamflow['year'] = pd.to_datetime(streamflow['datetime'], errors='coerce').dt.year
    shasta_reservoir['year'] = pd.to_datetime(shasta_reservoir['DATE'], errors='coerce').dt.year  # Or use 'DATE.1'

    # For agriculture land use, assuming you want to merge on a range of years
    agriculture_land_use['year'] = agriculture_land_use['Min Year']  # Or pick the year based on your requirement

    # Print the columns to ensure 'year' is added
    logging.info(f"Precipitation Columns: {precipitation.columns}")
    logging.info(f"Streamflow Columns: {streamflow.columns}")
    logging.info(f"Shasta Reservoir Columns: {shasta_reservoir.columns}")
    logging.info(f"Agriculture Land Use Columns: {agriculture_land_use.columns}")

    # Filter out rows with invalid dates
    precipitation = precipitation.dropna(subset=['year'])
    streamflow = streamflow.dropna(subset=['year'])
    shasta_reservoir = shasta_reservoir.dropna(subset=['year'])
    
    return precipitation, climate_projections, agriculture_land_use, streamflow, shasta_reservoir


def prepare_model_data(precipitation, climate_projections, agriculture_land_use, streamflow, shasta_reservoir):
    # Ensure that climate_projections has a 'year' column; if not, extract it or create one
    if 'year' not in climate_projections.columns:
        # Assuming the year is embedded within one of the columns (like 'Temperature.1')
        climate_projections['year'] = climate_projections['Temperature.1'].str.extract(r'(\d{4})')
        climate_projections['year'] = pd.to_numeric(climate_projections['year'], errors='coerce')  # Convert to numeric

    # Handle missing values in 'year' column before converting
    climate_projections['year'] = climate_projections['year'].fillna(-1).astype(int)  # Fill NaN with a placeholder (-1 or other)

    # Merge datasets on 'year'
    data = shasta_reservoir.merge(precipitation, on='year', how='left')
    data = data.merge(climate_projections, on='year', how='left')
    data = data.merge(agriculture_land_use, on='year', how='left')
    data = data.merge(streamflow, on='year', how='left')

    # Check the merged data to find the correct column names for the features
    logging.info(f"Merged Data Columns: {data.columns}")
    
    # Adjust the feature selection according to the actual column names in the merged DataFrame
    features = data[['PRCP', 'TAVG', 'Min Year', '10977_00060_00003']]  # Replace with correct columns
    target = data['VALUE']  # Adjust based on your actual target column (e.g., 'reservoir_level')

    # Drop columns that are completely empty (all NaN values)
    features = features.dropna(axis=1, how='all')

    # Check for empty columns and log
    empty_columns = features.columns[features.isnull().all()]
    if not empty_columns.empty:
        logging.warning(f"Features with no observed values (all NaN): {empty_columns.tolist()}")

    # Handle missing values in features (impute if needed)
    imputer = SimpleImputer(strategy='mean')

    # Before imputation, check for missing data in each column
    logging.info(f"Features before imputation: {features.isnull().sum()}")

    # Drop columns that are entirely NaN
    features = features.dropna(axis=1, how='all')  # Drop columns with all NaN values

    # Impute missing values
    features_imputed = pd.DataFrame(imputer.fit_transform(features), columns=features.columns)

    # Ensure that target is also clean (if needed)
    target = target.fillna(target.mean())  # Impute target if there are any NaN values
    
    return features_imputed, target


def train_and_evaluate_model(features, target):
    # Feature Scaling: Standardizing features before training
    scaler = StandardScaler()
    features_scaled = pd.DataFrame(scaler.fit_transform(features), columns=features.columns)
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(features_scaled, target, test_size=0.2, random_state=42)

    # Model selection: Using RandomForest as it handles non-linearity well
    model = RandomForestRegressor(n_estimators=100, random_state=42)

    # Hyperparameter tuning (optional, GridSearchCV)
    param_grid = {'n_estimators': [100, 200], 'max_depth': [None, 10, 20, 30]}
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, n_jobs=-1, scoring='neg_mean_absolute_error')
    grid_search.fit(X_train, y_train)
    
    # Get best model
    best_model = grid_search.best_estimator_

    # Train the model
    best_model.fit(X_train, y_train)

    # Make predictions and evaluate the model
    y_pred = best_model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    logging.info(f'Model Mean Absolute Error: {mae}')

    return best_model


if __name__ == '__main__':
    logging.info("Loading data...")
    precipitation, climate_projections, agriculture_land_use, streamflow, shasta_reservoir = load_data()

    logging.info("Preparing model data...")
    features, target = prepare_model_data(precipitation, climate_projections, agriculture_land_use, streamflow, shasta_reservoir)

    logging.info("Training and evaluating model...")
    model = train_and_evaluate_model(features, target)

    logging.info("Model training completed.")
    logging.info("Model evaluation completed.")
    logging.info("✅ Model training and evaluation complete.")
    logging.info("✅ Model is ready for predictions.")
    logging.info("✅ All datasets loaded and processed successfully.")  