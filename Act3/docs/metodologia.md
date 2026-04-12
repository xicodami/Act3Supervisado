# Metodología

## 1. Continuidad del proyecto

La metodología se diseñó para extender el sistema de transporte masivo local previamente construido, manteniendo coherencia con la red, las estaciones y la lógica de trayectos ya existentes. No se trató de un ejercicio independiente, sino de una evolución del mismo proyecto hacia un enfoque de ciencia de datos aplicada.

## 2. Construcción del dataset

Se definió una red sintética con 12 estaciones y 5 rutas principales. A partir de esta red se generaron trayectos válidos, tanto directos como con transbordo. Para cada recorrido se calcularon variables estructurales como distancia, número de segmentos y número de transbordos, y luego se añadieron variables contextuales como tipo de día, bloque horario, condición climática y nivel de tráfico.

La variable `travel_time_min` se simuló mediante reglas no lineales de comportamiento operativo, incorporando también un componente de ruido controlado. Esto permitió disponer de una señal suficientemente compleja para evaluar modelos de regresión con mayor realismo.

## 3. Metodología del aprendizaje supervisado

Para el componente supervisado se planteó una tarea de regresión. El conjunto de datos fue dividido en entrenamiento y prueba usando una partición 80/20. Las variables numéricas fueron estandarizadas y las variables categóricas fueron transformadas mediante one-hot encoding.

Se entrenaron dos modelos:

- **Linear Regression**, como línea base interpretable.
- **Random Forest Regressor**, como modelo capaz de capturar relaciones no lineales y efectos de interacción.

La evaluación se realizó con las métricas:

- MAE
- MSE
- RMSE
- R²

## 4. Metodología del aprendizaje no supervisado

Para el clustering se trabajó sobre el dataset derivado de trayectos. Dado que K-Means opera mejor sobre variables numéricas, se aplicó escalado a las variables cuantitativas y codificación dummy a las variables categóricas. Luego se evaluaron distintos valores de `k` entre 2 y 6.

La decisión sobre el número de clusters se apoyó en:

- **método del codo**, para observar la reducción de inercia,
- **silhouette score**, para evaluar separación y cohesión relativa.

Finalmente, se seleccionó `k = 5`, al ofrecer una relación razonable entre calidad del agrupamiento e interpretabilidad operativa.

## 5. Análisis de resultados

Los resultados se analizaron desde dos planos:

1. **Plano predictivo**, observando qué modelo estimó mejor el tiempo de viaje.
2. **Plano descriptivo**, identificando qué tipo de trayectos representa cada cluster y cómo estos patrones amplían la comprensión del sistema de transporte.