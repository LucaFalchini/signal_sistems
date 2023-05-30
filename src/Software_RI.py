# Este software permite obtener los parámetros acústicos EDT, T60 (a partir del T10, T20, T30),
# D50 y C80 de un recinto, según la Norma ISO 3382 (UNE-EN ISO 3382, 2010)
import funciones as f
import pandas as pd
from tkinter import *
# Etapa de generación y adquisición
import generacion_adquisicion as ga
# Etapa de preprocesamiento y filtrado
import preprocesamiento_filtrado as pf
# Etapa de suavizado y cálculo
import suavizado_calculo as sc

if __name__ == "__main__":
    file = 'data\IR2\Mono.wav'
    data, fs = f.read_wav(file)

    def graph_ir():
        f.time_domain_plot(data, fs)
    
    
    frec = pf.filtro_IEC(file)  # lista con las frecuencias filtradas por banda de octava     
    nominal_frec = [31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
    
    ## Genero un gráfico para determinar el corte de la integral de Schroeder
    log_signal = f.esc_log(data)
    f.time_domain_plot(log_signal, fs)


    # Interfaz gráfica   
    window = Tk()
    window.title("Suavizado y calculo")

    limit = Entry(window, width=50)
    limit.insert(0, "Ingrese el límite de integración en segundos: ")
    limit.pack()
    
    def param():        
        list_param = [] # Lista que almacena los parámetros acústicos por banda de octava
        for i in range(len(nominal_frec)):
            log_signal_i = f.esc_log(frec[i][1])
            param_i = sc.parametros_acústicos(frec[i][1], int(limit.get()))
            list_param.append(nominal_frec[i])
            list_param.append(param_i)
        print(list_param)

        index = list_param[::2]
        list_param_df = list_param[1::2]
    
        df = pd.DataFrame(list_param_df, index = index, columns =["EDT", "T10", "T20", "T30", "C80", "D50"])
        df = df.transpose()
        label = Label(window, text=str(df))
        label.pack()
        df.to_csv('resultados.csv')
        print(df)
    
    button = Button(window, 
                    text="Graficar impulso en dominio del tiempo", 
                    command=graph_ir, 
                    font=("Arial", 16),
                    fg="blue")
    button2 = Button(window, 
                    text="Calcular y graficar parámetros acústicos", 
                    command=param, 
                    font=("Arial", 16),
                    fg="blue")
    
    button.pack()
    button2.pack()
    window.mainloop()

