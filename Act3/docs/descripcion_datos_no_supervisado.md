# Descripción de datos del componente no supervisado

## Fuente de datos

El conjunto de datos no supervisado se derivó del mismo sistema y del mismo proceso de simulación utilizado en el componente supervisado. De esta manera, se garantiza continuidad entre ambos enfoques y se evita tratar el clustering como una actividad aislada.

El archivo utilizado es:

- `data/transport_unsupervised_dataset.csv`

Este archivo contiene **1800 trayectos** y conserva únicamente las variables necesarias para estudiar similitudes operativas entre recorridos.

## Variables utilizadas para clustering

- `distance_km`
- `segment_count`
- `transfer_count`
- `is_peak_hour`
- `traffic_level`
- `day_type`
- `weather_condition`
- `hour_block`

## Criterio de preparación

Para aplicar K-Means, las variables numéricas fueron escaladas y las variables categóricas se transformaron en variables dummy. Con el fin de evitar que la codificación categórica dominara por completo el agrupamiento, se aplicó un peso moderado a los bloques categóricos dentro de la matriz final. Esta decisión permitió conservar el contexto operativo del trayecto sin perder el protagonismo de variables estructurales como la distancia, el número de segmentos y los transbordos.

## Propósito analítico

Mientras que el componente supervisado busca predecir una variable concreta, el dataset no supervisado busca revelar estructuras latentes. En este sentido, su propósito es identificar grupos de trayectos que compartan complejidad, congestión, momento de operación y características de recorrido, generando perfiles útiles para comprender la dinámica del sistema.