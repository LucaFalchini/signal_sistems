# Este software permite obtener los parámetros acústicos EDT, T60 (a partir del T10, T20, T30),
# D50 y C80 de un recinto, según la Norma ISO 3382 (UNE-EN ISO 3382, 2010)
import funciones as f
import generacion_adquisicion as ga
import preprocesamiento_filtrado as pf
import suavizado_calculo as sc
import pandas as pd

# Etapa de generación y adquisición

# Etapa de preprocesamiento y filtrado

# Etapa de suavizado y cálculo

if __name__ == "__main__":
    file = 'signal-systems/trabajo_practico/noteboks/TP/Mediciones/Respuestas al impulso/IR2/Mono.wav'
    data, fs = f.read_wav(file)
    f.time_domain_plot(data, fs)
    
    frec = pf.filtro_IEC(file)

    nominal_frec = [31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
    list_param = []
    
    for i in range(len(nominal_frec)):
        log_signal = f.esc_log(frec[i][1])
        f.time_domain_plot(log_signal, fs)
        limit=int(input("ingrese el tiempo limite en segundos de la integración de Schroeder: "))
        param_i = sc.parametros_acústicos(frec[i][1], limit)
        list_param.append(nominal_frec[i])
        list_param.append(param_i)
    print(list_param)

    columns = list_param[::2]
    list_param_df = list_param[1::2]

    df = pd.DataFrame(list_param_df, index =['EDT', 'T10', 'T20', 'T30'], columns =columns)
    df.to_csv('resultados.csv')
    print(df)