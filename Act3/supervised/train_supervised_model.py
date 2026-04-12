from pathlib import Path
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "transport_supervised_dataset.csv"
RESULTS_DIR = ROOT / "results"
MODELS_DIR = ROOT / "models"

RESULTS_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

FEATURES = [
    'origin_station', 'destination_station', 'route_id', 'day_type', 'hour_block',
    'distance_km', 'segment_count', 'transfer_count', 'is_peak_hour',
    'weather_condition', 'traffic_level', 'station_type_origin', 'station_type_destination'
]
TARGET = 'travel_time_min'

def main():
    df = pd.read_csv(DATA_PATH)

    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    categorical_cols = [
        'origin_station', 'destination_station', 'route_id', 'day_type',
        'hour_block', 'weather_condition', 'traffic_level',
        'station_type_origin', 'station_type_destination'
    ]
    numerical_cols = ['distance_km', 'segment_count', 'transfer_count', 'is_peak_hour']

    preprocessor = ColumnTransformer(
        transformers=[
            (
                'num',
                Pipeline([
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler())
                ]),
                numerical_cols
            ),
            (
                'cat',
                Pipeline([
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('onehot', OneHotEncoder(handle_unknown='ignore'))
                ]),
                categorical_cols
            )
        ]
    )

    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest Regressor': RandomForestRegressor(
            n_estimators=250,
            random_state=42,
            n_jobs=-1
        )
    }

    metrics = []
    best_rmse = float('inf')
    best_model_name = None
    best_bundle = None

    for model_name, estimator in models.items():
        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('model', estimator)
        ])

        pipeline.fit(X_train, y_train)
        predictions = pipeline.predict(X_test)

        mae = mean_absolute_error(y_test, predictions)
        mse = mean_squared_error(y_test, predictions)
        rmse = mse ** 0.5
        r2 = r2_score(y_test, predictions)

        metrics.append({
            'model': model_name,
            'MAE': mae,
            'MSE': mse,
            'RMSE': rmse,
            'R2': r2
        })

        joblib.dump(pipeline, MODELS_DIR / f"{model_name.lower().replace(' ', '_')}.joblib")

        if rmse < best_rmse:
            best_rmse = rmse
            best_model_name = model_name
            best_bundle = {
                'pipeline': pipeline,
                'X_test': X_test,
                'y_test': y_test
            }

    metrics_df = pd.DataFrame(metrics).sort_values('RMSE')
    metrics_df.to_csv(RESULTS_DIR / 'supervised_metrics.csv', index=False)

    joblib.dump(best_bundle, MODELS_DIR / 'best_supervised_bundle.joblib')

    print(metrics_df.to_string(index=False))
    print(f"\nMejor modelo: {best_model_name}")

if __name__ == '__main__':
    main()