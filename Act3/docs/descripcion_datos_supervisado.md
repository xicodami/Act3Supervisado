# Descripción de datos del componente supervisado

## Fuente de datos

El conjunto de datos supervisado fue construido de forma **sintética** con fines académicos, debido a que no se contaba con una fuente real que reprodujera exactamente la red del sistema local ya modelado. Sin embargo, el dataset no se diseñó de manera arbitraria: se generó a partir de la estructura previa del proyecto, compuesta por 12 estaciones, 5 rutas, segmentos conectados, rutas con o sin transbordo y reglas de operación plausibles.

El archivo principal es:

- `data/transport_supervised_dataset.csv`

Este archivo contiene **1800 registros**, cada uno correspondiente a un trayecto posible dentro de la red.

## Variables incluidas

### Variables de entrada

- `origin_station`: estación de origen del trayecto.
- `destination_station`: estación de destino del trayecto.
- `route_id`: identificador de la ruta directa o combinación de rutas usada en el trayecto.
- `day_type`: tipo de día (`weekday`, `saturday`, `sunday`).
- `hour_block`: bloque horario del recorrido.
- `distance_km`: distancia total estimada del trayecto en kilómetros.
- `segment_count`: cantidad de segmentos recorridos.
- `transfer_count`: número de transbordos requeridos.
- `is_peak_hour`: indicador binario que señala si el trayecto ocurre en hora pico.
- `weather_condition`: condición climática del trayecto.
- `traffic_level`: nivel de tráfico asociado al recorrido.
- `station_type_origin`: tipo de estación de origen.
- `station_type_destination`: tipo de estación de destino.

### Variable objetivo

- `travel_time_min`: tiempo estimado de viaje en minutos.

## Lógica de generación

La variable objetivo fue calculada mediante una combinación de reglas operativas coherentes con el dominio:

- mayor distancia implica mayor tiempo,
- más segmentos aumentan la duración,
- los transbordos agregan penalización temporal,
- la congestión incrementa el tiempo,
- la lluvia y la lluvia fuerte añaden demoras,
- las horas pico afectan la velocidad operativa,
- algunos corredores, como los asociados a zonas industriales o al aeropuerto, presentan comportamiento más lento en determinadas franjas.

Adicionalmente, se incorporó una perturbación aleatoria controlada para evitar un comportamiento completamente determinista, haciendo más realista el ejercicio de regresión.

## Justificación académica

Este dataset es válido para fines formativos porque conserva la coherencia del sistema modelado, incorpora variables significativas del dominio y permite desarrollar análisis cuantitativos reproducibles. Aunque no reemplaza una base real de operación masiva, sí constituye una aproximación suficientemente rica para evaluar modelos de aprendizaje automático en un contexto universitario.