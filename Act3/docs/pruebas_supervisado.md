# Pruebas realizadas: componente supervisado

## 1. Validación del dataset

Se verificó que el archivo `transport_supervised_dataset.csv` contuviera registros consistentes con la red modelada, sin estaciones repetidas como origen y destino en un mismo trayecto, y con valores numéricos válidos para distancia, segmentos, transbordos y tiempo estimado de viaje.

También se revisó que la variable objetivo presentara variabilidad suficiente para el entrenamiento. La distribución observada mostró trayectos cortos, medios y largos, lo cual favorece el aprendizaje del modelo y evita un conjunto excesivamente homogéneo.

## 2. Prueba de entrenamiento de modelos

Se ejecutó el entrenamiento de dos modelos de regresión sobre la misma partición de entrenamiento y prueba.

### Modelos evaluados

- Linear Regression
- Random Forest Regressor

## 3. Métricas obtenidas

| Modelo | MAE | MSE | RMSE | R² |
|---|---:|---:|---:|---:|
| Random Forest Regressor | 1.9897 | 7.3415 | 2.7095 | 0.9773 |
| Linear Regression | 2.3367 | 9.0721 | 3.0120 | 0.9719 |

## 4. Interpretación de resultados

Los dos modelos mostraron un desempeño alto, lo cual indica que el dataset contiene una relación clara entre las variables operativas y el tiempo estimado de viaje. Sin embargo, el mejor comportamiento fue obtenido por **Random Forest Regressor**, que alcanzó:

- menor error absoluto medio,
- menor error cuadrático medio,
- menor RMSE,
- mayor coeficiente R².

Esta diferencia era esperable, ya que el tiempo de viaje fue generado con reglas no lineales y con interacciones entre variables como tráfico, clima, transbordos y franja horaria. En este contexto, un modelo de bosque aleatorio tiene mayor capacidad para capturar dichos patrones que una regresión lineal pura.

## 5. Validación visual

Se generaron las siguientes visualizaciones:

- `supervised/supervised_results.png`: comparación de métricas y gráfico de valores reales vs. predichos.
- `supervised/travel_time_distribution.png`: distribución de tiempos de viaje del dataset.

## 6. Conclusión de la prueba supervisada

La prueba permite concluir que el sistema de transporte modelado puede evolucionar a una herramienta predictiva con buen desempeño. El resultado no solo valida el uso del dataset sintético, sino que demuestra que la red previa del proyecto es suficientemente rica para soportar analítica supervisada coherente.