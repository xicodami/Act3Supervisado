# transport_ai_project

Proyecto académico desarrollado sobre un sistema de transporte masivo local tipo **Ciudad Móvil**, reutilizando la red previamente construida para evolucionar hacia dos componentes de analítica de datos:

1. **Aprendizaje supervisado** para predecir el tiempo estimado de viaje (`travel_time_min`).
2. **Aprendizaje no supervisado** para agrupar trayectos similares según sus características operativas.

## Enfoque general

El proyecto mantiene una sola línea lógica de trabajo:

- representación de la red de transporte,
- generación de trayectos coherentes con estaciones, rutas, segmentos y transbordos,
- predicción de tiempos de viaje,
- descubrimiento de patrones operativos mediante clustering.

Los datos son **sintéticos y académicamente justificados**, construidos a partir de una red pequeña con 12 estaciones y 5 rutas, preservando coherencia con el sistema de transporte diseñado en la fase anterior.

## Estructura del proyecto

```text
transport_ai_project/
├── data/
│   ├── stations_reference.csv
│   ├── routes_reference.csv
│   ├── transport_supervised_dataset.csv
│   └── transport_unsupervised_dataset.csv
├── docs/
│   ├── descripcion_datos_supervisado.md
│   ├── descripcion_datos_no_supervisado.md
│   ├── introduccion.md
│   ├── metodologia.md
│   ├── objetivos.md
│   ├── planteamiento_problema.md
│   ├── pruebas_no_supervisado.md
│   ├── pruebas_supervisado.md
│   ├── resultados.md
│   └── conclusiones.md
├── models/
│   ├── best_supervised_bundle.joblib
│   ├── kmeans_transport.joblib
│   ├── linear_regression.joblib
│   └── random_forest_regressor.joblib
├── results/
│   ├── cluster_summary.csv
│   ├── supervised_metrics.csv
│   ├── transport_unsupervised_labeled.csv
│   └── unsupervised_k_selection.csv
├── supervised/
│   ├── evaluate_supervised_model.py
│   ├── supervised_results.png
│   ├── train_supervised_model.py
│   └── travel_time_distribution.png
├── unsupervised/
│   ├── analyze_clusters.py
│   ├── clusters_results.png
│   ├── silhouette_scores.png
│   └── train_kmeans_model.py
├── generate_datasets.py
├── README.md
└── requirements.txt
```

## Requisitos

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

## Ejecución paso a paso

Desde la raíz del proyecto:

```bash
python generate_datasets.py
python supervised/train_supervised_model.py
python supervised/evaluate_supervised_model.py
python unsupervised/train_kmeans_model.py
python unsupervised/analyze_clusters.py
```

## Resultado del componente supervisado

Se entrenaron dos modelos de regresión:

- Linear Regression
- Random Forest Regressor

Métricas obtenidas:

| Modelo | MAE | MSE | RMSE | R² |
|---|---:|---:|---:|---:|
| Random Forest Regressor | 1.9897 | 7.3415 | 2.7095 | 0.9773 |
| Linear Regression | 2.3367 | 9.0721 | 3.0120 | 0.9719 |

**Conclusión técnica:** el mejor desempeño lo obtuvo **Random Forest Regressor**, con menor error absoluto, menor RMSE y mayor coeficiente de determinación.

## Resultado del componente no supervisado

Para K-Means se evaluaron valores de `k` entre 2 y 6 con apoyo del método del codo y del silhouette score.

| k | Inercia | Silhouette |
|---:|---:|---:|
| 2 | 7826.9072 | 0.2368 |
| 3 | 6601.8314 | 0.2267 |
| 4 | 5689.3085 | 0.2371 |
| 5 | 4910.7933 | 0.2596 |
| 6 | 4594.2654 | 0.2675 |

Se seleccionó **k = 5** porque ofrece un equilibrio adecuado entre reducción de inercia e interpretabilidad operativa, evitando una segmentación excesiva.

## Resumen de clusters

- **Cluster 2:** trayectos cortos de valle operativo, sin transbordos y con tráfico medio.
- **Cluster 1:** trayectos cortos en franja pico de la tarde, con mayor congestión.
- **Cluster 4:** trayectos medios-largos en pico de la mañana, con alta probabilidad de transbordo.
- **Cluster 0:** trayectos medios-largos en franja diurna, con tráfico moderado.
- **Cluster 3:** trayectos largos y complejos, con transbordo garantizado y mayor número de segmentos.
