from pathlib import Path
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
MODELS_DIR = ROOT / "models"
SUPERVISED_DIR = ROOT / "supervised"
DATA_PATH = ROOT / "data" / "transport_supervised_dataset.csv"

SUPERVISED_DIR.mkdir(exist_ok=True)

def main():
    metrics_df = pd.read_csv(RESULTS_DIR / 'supervised_metrics.csv').sort_values('RMSE')
    bundle = joblib.load(MODELS_DIR / 'best_supervised_bundle.joblib')
    pipeline = bundle['pipeline']
    X_test = bundle['X_test']
    y_test = bundle['y_test']
    predictions = pipeline.predict(X_test)
    best_model_name = metrics_df.iloc[0]['model']

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    x = np.arange(len(metrics_df))
    width = 0.35
    plt.bar(x - width / 2, metrics_df['MAE'], width, label='MAE')
    plt.bar(x + width / 2, metrics_df['RMSE'], width, label='RMSE')
    plt.xticks(x, metrics_df['model'], rotation=10)
    plt.ylabel('Error (minutos)')
    plt.title('Comparación de métricas de error')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.scatter(y_test, predictions, alpha=0.55)
    limits = [min(y_test.min(), predictions.min()), max(y_test.max(), predictions.max())]
    plt.plot(limits, limits)
    plt.xlabel('Tiempo real (min)')
    plt.ylabel('Tiempo predicho (min)')
    plt.title(f'Real vs predicho - {best_model_name}')

    plt.tight_layout()
    plt.savefig(SUPERVISED_DIR / 'supervised_results.png', dpi=180, bbox_inches='tight')
    plt.close()

    df = pd.read_csv(DATA_PATH)
    plt.figure(figsize=(8, 5))
    plt.hist(df['travel_time_min'], bins=25)
    plt.xlabel('Tiempo de viaje (min)')
    plt.ylabel('Frecuencia')
    plt.title('Distribución del tiempo estimado de viaje')
    plt.tight_layout()
    plt.savefig(SUPERVISED_DIR / 'travel_time_distribution.png', dpi=180, bbox_inches='tight')
    plt.close()

    print('Gráficas del componente supervisado generadas correctamente.')

if __name__ == '__main__':
    main()