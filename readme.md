# Modelo de Propagación y Control Espacial del Dengue en el Gran Mendoza

Este repositorio contiene el código fuente y las rutinas de simulación de un **autómata celular bidimensional** diseñado para modelar la dinámica espacial de propagación del dengue en el Gran Mendoza (Argentina) y evaluar la eficacia topológica de distintas estrategias de fumigación bajo escenarios de anomalías climáticas (El Niño).

Proyecto desarrollado como Trabajo Final para la asignatura **Sistemas Complejos** (Licenciatura en Ciencias de la Computación, FING - UNCUYO).

## Bases Teóricas y Modelado Científico

El simulador integra tres marcos teóricos principales de la literatura reciente:

1. **Motor Biológico (Dinámica Local):** 
   Implementa el modelo eco-epidemiológico compartimental de *Gutierrez et al. (2022)*. Se asume una difusión espacial nula del vector ($D_V = 0$), limitando el radio de vuelo del *Aedes aegypti* a su propia celda. La evolución de la población (Infección cruzada, mortalidad del vector $\mu = 1/15$ y recuperación humana $\gamma = 1/7$) se resuelve en pasos discretos de $\Delta t = 1$ día.
   
2. **Modelo de Movilidad (Percolación Espacial):**
   Dado que el mosquito es estático, el virus se esparce a través de la red humana. Se adaptó el enfoque de *Ospina-Aguirre et al. (2023)* utilizando un **Modelo de Gravedad**, donde las personas viajan diariamente desde zonas residenciales hacia nodos de alto "atractivo" (ej. microcentro), calculado mediante ponderación probabilística espacial ($A = \frac{100}{d^2}$).
   
3. **Estrés Climático (El Niño):**
   Las simulaciones de producción están forzadas por las condiciones de la fase cálida de El Niño (temperatura constante entre 20°C y 30°C), que es el rango crítico que dispara los brotes epidémicos en Argentina, según lo determinado por *Enet et al. (2026)*.

## Herramientas y Requisitos

* **Entorno de Simulación:** NetLogo 7+.

## Uso del Simulador

1. Abrir el archivo `.nlogox` en NetLogo.
2. Hacer clic en `setup` para inicializar el mapa de calor (atractivo urbano) y fijar el paciente cero (1 infectado) en el centro de máxima gravedad.
3. Presionar `go` para iniciar el reloj temporal ($\Delta t = 1$ día).
4. La interfaz pintará de rojo los parches donde la prevalencia de la infección humana supere el 5%, permitiendo visualizar la onda expansiva concéntrica del brote epidémico en la matriz.

*(En desarrollo: Módulos de intervención espacial para evaluación de fumigación en anillos concéntricos vs. barreras lineales estratégicas).*