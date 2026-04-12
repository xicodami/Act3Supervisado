# Conclusiones

1. El proyecto logró mantener continuidad con la fase anterior del sistema de transporte masivo local, evitando construir una solución desconectada y demostrando una evolución coherente del mismo dominio hacia técnicas de aprendizaje automático.

2. La construcción de un dataset sintético resultó adecuada para fines académicos, ya que permitió conservar la lógica de estaciones, rutas, segmentos y transbordos previamente modelada, al mismo tiempo que introdujo variables operativas relevantes para el análisis.

3. El componente de aprendizaje supervisado mostró que es posible predecir el tiempo estimado de viaje a partir de variables estructurales y contextuales del trayecto. Entre los modelos evaluados, **Random Forest Regressor** presentó el mejor desempeño, lo que indica que el problema contiene relaciones no lineales que no son capturadas por completo por una regresión lineal simple.

4. El componente no supervisado confirmó que los trayectos del sistema pueden agruparse en perfiles operativos diferenciados. La aplicación de K-Means permitió identificar trayectos cortos, trayectos de hora pico, trayectos medios con transbordo y trayectos largos de alta complejidad, enriqueciendo la comprensión del comportamiento de la red.

5. La combinación de regresión y clustering dentro del mismo proyecto demostró que un sistema de transporte puede analizarse desde múltiples dimensiones: no solo como una estructura de rutas y estaciones, sino también como un entorno susceptible de predicción y descubrimiento de patrones.

6. Desde una perspectiva formativa, el proyecto integra conceptos de ingeniería de software, modelado de datos, aprendizaje supervisado, aprendizaje no supervisado y redacción técnica, constituyéndose en una entrega universitaria completa y metodológicamente consistente.

7. Como trabajo futuro, sería valioso incorporar datos reales de aforo, frecuencia, incidentes operativos o georreferenciación más detallada para fortalecer la validez externa del modelo y aproximarlo aún más a un caso urbano real.