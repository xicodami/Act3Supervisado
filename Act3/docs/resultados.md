# Resultados y análisis

## 1. Resultado del aprendizaje supervisado

El problema de regresión tuvo como objetivo estimar el tiempo de viaje de un trayecto dentro del sistema Ciudad Móvil. Al comparar los dos modelos entrenados, se obtuvieron los siguientes resultados:

| Modelo | MAE | MSE | RMSE | R² |
|---|---:|---:|---:|---:|
| Random Forest Regressor | 1.9897 | 7.3415 | 2.7095 | 0.9773 |
| Linear Regression | 2.3367 | 9.0721 | 3.0120 | 0.9719 |

El análisis muestra que ambos modelos aprendieron adecuadamente la relación entre las variables explicativas y el tiempo de viaje. Sin embargo, el bosque aleatorio superó a la regresión lineal en todas las métricas principales. Este resultado confirma que el fenómeno modelado no es estrictamente lineal, sino que involucra interacciones y efectos escalonados asociados a congestión, clima, hora pico y transbordos.

## 2. Resultado del aprendizaje no supervisado

El componente no supervisado permitió segmentar los trayectos en cinco grupos operativos. La selección de `k = 5` se sustentó en una combinación de reducción de inercia e interpretabilidad.

### Resumen de clusters

| Cluster | Cantidad | Distancia promedio | Segmentos promedio | Transbordos promedio | Proporción hora pico |
|---:|---:|---:|---:|---:|---:|
| 2 | 371 | 4.826 | 1.544 | 0.000 | 0.000 |
| 1 | 415 | 5.138 | 1.617 | 0.000 | 1.000 |
| 4 | 447 | 8.586 | 2.792 | 0.935 | 1.000 |
| 0 | 430 | 8.689 | 2.812 | 0.926 | 0.000 |
| 3 | 137 | 17.670 | 4.898 | 1.000 | 0.547 |

## 3. Análisis conjunto

El valor de esta fase del proyecto no radica únicamente en entrenar modelos, sino en demostrar que la misma red de transporte puede analizarse desde dos perspectivas complementarias:

- una perspectiva **predictiva**, que estima la duración del viaje;
- una perspectiva **descriptiva**, que organiza los trayectos en familias operativas.

Esta complementariedad fortalece la utilidad académica del proyecto porque conecta representación del dominio, modelado de datos, aprendizaje automático y análisis de resultados en una sola propuesta coherente.