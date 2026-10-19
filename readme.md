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

## Bitácora de Simulación y Comportamientos Emergentes

Durante las pruebas en la topología de grilla abstracta, se implementaron las siguientes mejoras y se registraron los siguientes fenómenos:

1. **Topología Finita:** Se desactivó la topología de toroide ("world wrap") para confinar la simulación a un plano con límites definidos, evitando fugas dimensionales del patógeno.
2. **Estocasticidad Inicial:** El paciente cero se ubica de forma aleatoria en la matriz, permitiendo evaluar el efecto de "succión" gravitacional desde la periferia hacia el nodo céntrico.
3. **Movilidad Bidireccional:** El modelo permite el viaje de humanos susceptibles (S) e infectados (I), simulando el contagio en el destino (ida) y el transporte del virus hacia los barrios residenciales (retorno).
4. **Automatización:** Se integró un disparador que despliega intervenciones de fumigación al superar un umbral crítico de prevalencia (ej. 200 casos), simulando la latencia de respuesta sanitaria.
5. **Efecto Puente (Fuga Espacial):** Las simulaciones con "anillos preventivos amplios" demostraron que la fumigación aislada es ineficaz si se mantiene la movilidad. Los individuos que residen dentro de la barrera química actúan como vectores de relevo: viajan a la zona infectada, contraen el virus y lo exportan cruzando la zona tratada hacia parches susceptibles.