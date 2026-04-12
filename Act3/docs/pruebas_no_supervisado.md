# Pruebas realizadas: componente no supervisado

## 1. Validación del dataset

Se verificó que el archivo `transport_unsupervised_dataset.csv` conservara consistencia con el conjunto supervisado y contuviera variables relevantes para agrupar trayectos según sus características operativas.

## 2. Evaluación de distintos valores de k

Se aplicó K-Means para `k` entre 2 y 6. Los resultados fueron:

| k | Inercia | Silhouette |
|---:|---:|---:|
| 2 | 7826.9072 | 0.2368 |
| 3 | 6601.8314 | 0.2267 |
| 4 | 5689.3085 | 0.2371 |
| 5 | 4910.7933 | 0.2596 |
| 6 | 4594.2654 | 0.2675 |

## 3. Justificación del número de clusters

La inercia disminuye de forma progresiva al aumentar `k`, como es habitual en K-Means. No obstante, el cambio empieza a ser menos pronunciado después de `k = 5`. En paralelo, el silhouette score mejora respecto a configuraciones más pequeñas, mostrando que cinco grupos ofrecen una segmentación útil sin caer en una partición excesivamente fragmentada para el propósito académico del proyecto.

Por esta razón se seleccionó **k = 5**.

## 4. Perfil general de los clusters

A partir del resumen estadístico de cada grupo, se identificaron los siguientes perfiles:

- **Cluster 2:** trayectos cortos, sin transbordos, en franja de valle y con tráfico medio.
- **Cluster 1:** trayectos cortos, en hora pico de la tarde y con mayor presión de congestión.
- **Cluster 4:** trayectos medios-largos, típicos de la hora pico de la mañana, con alta probabilidad de transbordo.
- **Cluster 0:** trayectos medios-largos en jornada diurna, con congestión media y complejidad intermedia.
- **Cluster 3:** trayectos largos, con transbordo garantizado y mayor número de segmentos, es decir, el grupo de mayor complejidad operativa.

## 5. Validación visual

Se generaron las siguientes salidas:

- `unsupervised/clusters_results.png`: gráfico del codo y proyección bidimensional de los trayectos agrupados.
- `unsupervised/silhouette_scores.png`: comparación del silhouette score por número de clusters.
- `results/cluster_summary.csv`: resumen numérico de cada grupo.

## 6. Conclusión de la prueba no supervisada

El clustering permitió confirmar que la red de transporte no solo puede describirse o predecirse, sino también segmentarse en perfiles operativos comprensibles. Esto amplía el valor académico del proyecto, ya que demuestra la utilidad del aprendizaje no supervisado sobre el mismo dominio trabajado en etapas anteriores.