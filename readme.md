# Modelo de Autómata Celular para la Propagación Espacial del Dengue en el Gran Mendoza

Este repositorio contiene el código fuente, los scripts de análisis y los datasets de simulación de un modelo estocástico basado en Autómatas Celulares (AC) diseñado para estudiar la percolación espacial del virus del dengue en el ejido urbano del Gran Mendoza, Argentina, bajo condiciones climáticas anómalas (fenómeno de El Niño).

Este proyecto fue desarrollado como trabajo final para la asignatura **Sistemas Complejos** de la Licenciatura en Ciencias de la Computación (Universidad Nacional de Cuyo).

## Características Principales

*   **Entorno Espacial Realista:** Utiliza una grilla base de 251x251 parches (escalable) sobre la cual se aplica una máscara espacial binaria para restringir la simulación estrictamente a la mancha urbana activa del Gran Mendoza.
*   **Movilidad por Gravedad:** Implementa un algoritmo de ruteo pendular estocástico para la población asintomática, ponderando la distancia euclidiana y el atractivo zonal (nodos comerciales/educativos).
*   **Dinámica Eco-Epidemiológica Local:** La capacidad de carga del vector (*Aedes aegypti*) está condicionada por variables meteorológicas locales (precipitaciones y temperatura), simulando el letargo invernal y el rebrote estival.
*   **Evaluación de Estrategias Topológicas:** Incluye funciones de mitigación espacial para evaluar intervenciones de fumigación:
    *   `Base`: Evolución natural del brote (sin intervención).
    *   `Anillo`: Cerco perimetral concéntrico focalizado en casos índice.
    *   `Barrera`: Bloqueo transversal de corredores de movilidad.

## Estructura del Repositorio

```text
├── dengue_mendoza.nlogox        # Código fuente principal del modelo en NetLogo
├── graficos.py                 # Script de Python para procesamiento y visualización de datos
├── mascara-gran-mendoza.png    # Máscara binaria topológica del ejido urbano
├── /datasets                   # Directorio con salidas CSV de BehaviorSpace (n=50 corridas)
│   ├── base-50-runs.csv
│   ├── Anillo-50-runs.csv
│   └── Barrera-50-runs.csv
└── /img                        # Gráficos generados y capturas de percolación espacial
```

## Requisitos y Configuración

Para ejecutar y modificar este proyecto necesitas:

1.  **NetLogo:** Versión 7.0 o superior.
2.  **Python:** Versión 3.10 o superior para el análisis de resultados.
3.  **Dependencias de Python:**
    ```bash
    pip install numpy matplotlib
    ```

## Uso y Ejecución

### 1. Simulación en NetLogo
*   Abre el archivo `dengue_mendoza.nlogo` en NetLogo.
*   Asegúrate de que la imagen `mascara-gran-mendoza.png` se encuentre en el mismo directorio.
*   Desde la interfaz, presiona `Setup` para inicializar las poblaciones y cargar la topología.
*   Usa el botón `Go` para ejecutar la simulación de forma continua, o utiliza la herramienta **BehaviorSpace** (`Tools > BehaviorSpace`) para realizar múltiples corridas de Montecarlo (recomendado $n \ge 50$ para estabilizar la varianza estocástica).

### 2. Generación de Gráficos
Una vez exportados los resultados desde BehaviorSpace en formato CSV (formato *spreadsheet*), ejecuta el analizador en Python para calcular las medias, desviaciones estándar poblacionales y renderizar los gráficos en escala logarítmica (aplicando conservación estricta de masa poblacional):

```bash
python3 graficos.py
```