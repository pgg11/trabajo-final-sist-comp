import numpy as np
import matplotlib.pyplot as plt
import os

# Asegurarse de que la carpeta de imágenes exista
os.makedirs('img', exist_ok=True)

def leer_datos_netlogo(filepath):
    """
    Lee los CSV de NetLogo (formato spreadsheet).
    El código es robusto y limpia comillas por las dudas.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    reporters = lines[8].strip().replace('"', '').split(',')
    
    hum_i_indices = [i for i, rep in enumerate(reporters) if 'hum-I' in rep]
    hum_r_indices = [i for i, rep in enumerate(reporters) if 'hum-R' in rep]
    num_runs = len(hum_i_indices)
    
    hum_i_data_dict = {}
    hum_r_data_dict = {}
    
    for line in lines[9:]:
        vals = line.strip().replace('"', '').split(',')
        if len(vals) < max(hum_r_indices) + 1: continue
        
        step_str = vals[1] 
        
        try:
            step = int(step_str)
        except ValueError:
            continue
            
        if step not in hum_i_data_dict:
            hum_i_data_dict[step] = np.zeros(num_runs)
            hum_r_data_dict[step] = np.zeros(num_runs)
            
        for r in range(num_runs):
            try:
                i_val = vals[hum_i_indices[r]]
                r_val = vals[hum_r_indices[r]]
                hum_i_data_dict[step][r] = float(i_val) if i_val else 0.0
                hum_r_data_dict[step][r] = float(r_val) if r_val else 0.0
            except ValueError:
                pass

    max_step = max(hum_i_data_dict.keys())
    hum_i_arr = np.zeros((max_step + 1, num_runs))
    hum_r_arr = np.zeros((max_step + 1, num_runs))
    
    for step in range(max_step + 1):
        if step in hum_i_data_dict:
            hum_i_arr[step] = hum_i_data_dict[step]
            hum_r_arr[step] = hum_r_data_dict[step]
            
    return hum_i_arr, hum_r_arr

def generar_grafico_individual(i_mean, i_std, r_mean, s_mean, titulo, archivo_salida, color_i, color_r, color_s):
    ticks = np.arange(len(i_mean))
    plt.figure(figsize=(10, 5))
    
    # Graficamos Susceptibles
    plt.plot(ticks, s_mean, label='Susceptibles (Media)', color=color_s, linestyle=':')
    
    # Graficamos Infectados con su sombra (mínimo en 1 para logarítmica)
    plt.plot(ticks, i_mean, label='Infectados (Media)', color=color_i)
    plt.fill_between(ticks, np.maximum(i_mean - i_std, 1), i_mean + i_std, color=color_i, alpha=0.2, label='Desv. Estándar (Infectados)')
    
    # Graficamos Recuperados
    plt.plot(ticks, r_mean, label='Recuperados (Media)', color=color_r, linestyle='--')
    
    plt.yscale('log')
    plt.ylim(1, 2500000)
    plt.xlim(left=0)
    
    plt.title(titulo)
    plt.xlabel('Días (ticks)')
    plt.ylabel('Población Humana (Escala Logarítmica)')
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3, which="both", ls="--")
    plt.tight_layout()
    
    # Guardamos en la carpeta img/
    ruta_guardado = os.path.join('img', archivo_salida)
    plt.savefig(ruta_guardado, dpi=300)
    plt.close()
    print(f"Generado: {ruta_guardado}")

# 1. Cargar los datos desde la carpeta datasets/
base_i, base_r = leer_datos_netlogo(os.path.join("datasets", "base-50-runs.csv"))
anillo_i, anillo_r = leer_datos_netlogo(os.path.join("datasets", "Anillo-50-runs.csv"))
barrera_i, barrera_r = leer_datos_netlogo(os.path.join("datasets", "Barrera-50-runs.csv"))

# 2. Calcular medias y desviaciones estándar
base_i_mean = np.mean(base_i, axis=1)
base_i_std = np.std(base_i, axis=1)
base_r_mean = np.mean(base_r, axis=1)

anillo_i_mean = np.mean(anillo_i, axis=1)
anillo_i_std = np.std(anillo_i, axis=1)
anillo_r_mean = np.mean(anillo_r, axis=1)

barrera_i_mean = np.mean(barrera_i, axis=1)
barrera_i_std = np.std(barrera_i, axis=1)
barrera_r_mean = np.mean(barrera_r, axis=1)

# Calcular Susceptibles por conservación de masa
POBLACION_TOTAL = 1521700
base_s_mean = POBLACION_TOTAL - base_i_mean - base_r_mean
anillo_s_mean = POBLACION_TOTAL - anillo_i_mean - anillo_r_mean
barrera_s_mean = POBLACION_TOTAL - barrera_i_mean - barrera_r_mean

ticks = np.arange(len(base_i_mean))

# 3. Generar el gráfico comparativo general
plt.figure(figsize=(8, 8))

# === SOLO INFECTADOS ===
plt.plot(ticks, base_i_mean, label='Base (Infectados)', color='#d62728')
plt.fill_between(ticks, np.maximum(base_i_mean - base_i_std, 1), base_i_mean + base_i_std, color='#d62728', alpha=0.15)

plt.plot(ticks, anillo_i_mean, label='Anillo (Infectados)', color='#1f77b4')
plt.fill_between(ticks, np.maximum(anillo_i_mean - anillo_i_std, 1), anillo_i_mean + anillo_i_std, color='#1f77b4', alpha=0.15)

plt.plot(ticks, barrera_i_mean, label='Barrera (Infectados)', color='#ff7f0e')
plt.fill_between(ticks, np.maximum(barrera_i_mean - barrera_i_std, 1), barrera_i_mean + barrera_i_std, color='#ff7f0e', alpha=0.15)

# === SOLO RECUPERADOS ===
plt.plot(ticks, base_r_mean, label='Base (Recuperados)', color='#8c564b', linestyle='--')
plt.plot(ticks, anillo_r_mean, label='Anillo (Recuperados)', color='#000080', linestyle='--')
plt.plot(ticks, barrera_r_mean, label='Barrera (Recuperados)', color='#8b4500', linestyle='--')

# Configuración de escala y límites
plt.yscale('log')
plt.ylim(1, 10000) # Techo bajado a 1e4
plt.xlim(left=0)

# Títulos y fuentes más grandes para legibilidad
plt.title('Comparación de Estrategias (50 Corridas)', fontsize=16)
plt.xlabel('Días (ticks)', fontsize=14)
plt.ylabel('Población Humana (Escala Logarítmica)', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Leyenda sin los Susceptibles
plt.legend(loc='upper left', fontsize=11, ncol=2) 
plt.grid(True, alpha=0.3, which="both", ls="--")
plt.tight_layout()

ruta_comparativo = os.path.join('img', 'grafico_comparativo.png')
plt.savefig(ruta_comparativo, dpi=300)
plt.close()


# 4. Generar los gráficos individuales
generar_grafico_individual(base_i_mean, base_i_std, base_r_mean, base_s_mean,
                           'Escenario Base (50 Corridas)', 'grafico_base.png', '#d62728', '#8c564b', '#2ca02c')
generar_grafico_individual(anillo_i_mean, anillo_i_std, anillo_r_mean, anillo_s_mean,
                           'Escenario Anillo (50 Corridas)', 'grafico_anillo.png', '#1f77b4', '#000080', '#006400')
generar_grafico_individual(barrera_i_mean, barrera_i_std, barrera_r_mean, barrera_s_mean,
                           'Escenario Barrera (50 Corridas)', 'grafico_barrera.png', '#ff7f0e', '#8b4500', '#98df8a')


aleatorio_i, aleatorio_r = leer_datos_netlogo(os.path.join("datasets", "Aleatorio-50-runs.csv"))
aleatorio_i_mean = np.mean(aleatorio_i, axis=1)
aleatorio_i_std = np.std(aleatorio_i, axis=1)

plt.figure(figsize=(8, 8)) # Ratio 1:1

plt.plot(ticks, aleatorio_i_mean, label='Aleatorio (Media)', color='#9467bd')
plt.fill_between(ticks, np.maximum(aleatorio_i_mean - aleatorio_i_std, 1), 
                 aleatorio_i_mean + aleatorio_i_std, color='#9467bd', alpha=0.15)

plt.plot(ticks, anillo_i_mean, label='Anillo (Media)', color='#1f77b4')
plt.fill_between(ticks, np.maximum(anillo_i_mean - anillo_i_std, 1), 
                 anillo_i_mean + anillo_i_std, color='#1f77b4', alpha=0.15)

plt.yscale('log')
plt.ylim(1, 10000) # Techo bajado a 1e4
plt.xlim(left=0)

plt.title('Contraste de Hipótesis: Anillo vs. Aleatorio (Área Constante)', fontsize=16)
plt.xlabel('Días (ticks)', fontsize=14)
plt.ylabel('Población Infectada (Escala Logarítmica)', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(loc='upper left', fontsize=12)
plt.grid(True, alpha=0.3, which="both", ls="--")
plt.tight_layout()

ruta_anillo_aleatorio = os.path.join('img', 'comparativa_anillo_aleatorio.png')
plt.savefig(ruta_anillo_aleatorio, dpi=300)
plt.close()

print("Gráficos generados exitosamente")