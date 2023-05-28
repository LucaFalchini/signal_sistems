import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from scipy import signal as s
import soundfile as sf
from funciones import read_wav
from funciones import time_domain_plot
from funciones import esc_log

# Función suavizado de señal
def suavizado_señal(signal, w_size):
    '''
    Calcula la señal analítica de una señal y su transformada de Hilbert y
    Calcula el promedio en un rango de valores de la señal original dado por w_size y los almacena en un array.

    Parametros
    ----------
    signal: Numpy array

    w_size: Tamaño de la ventana de muestreo.
           
    return: Numpy array con la señal suavizada.

    Ejemplo
    -------
    import numpy as np
    import soundfile as sf
    from scipy import signal as s
    
    signal, fs = sf.read('SineSweepLog.wav')
    suavizado_señal(signal, w_size)
    
    '''
    analytic_signal = s.hilbert(signal) 
    amplitude_envelope = np.abs(analytic_signal)
    
    signal_win = [] # Inicio una lista donde se van a almacenar los promedios móviles

    for i in range(len(amplitude_envelope)-(w_size-1)): # Ciclo for con rango hasta el ancho de la ventana
        w_i = amplitude_envelope[i : i + w_size]    # Ventana que itera en cada ciclo
        w_mean = np.mean(w_i)   # Calculo el promedio
        signal_win.append(w_mean)   # Agrego el promedio a la lista signal_win
    
    for i in range(w_size-1):   # Ciclo para que shape(signal)=shape(signal_win) agregando el último valor promediado
        signal_win.append(signal_win[-1])
       
    return(np.array(signal_win))

# Función integral de Schroeder
def schroeder(signal, lim=3):
    """
    Calcula la integral de Schroeder de una RI.
     Parametros
    ----------
    signal:

    lim:

    Ejemplo
    -------
    import numpy as np
    import soundfile as sf
    from scipy import signal as s
    
    signal, fs = sf.read('impulso_aula2.wav')
    lim = int(len(signal)/fs)
    schroeder(signal, lim)
    """
    cut_lim = lim*44100
    E = (10*np.log10(np.cumsum(np.power(signal[cut_lim::-1],2))/np.sum(np.power(signal[:cut_lim],2))))[::-1]
    #E = np.cumsum(np.power(signal[150000::-1],2))[::-1]
    return(E)

# Función regresión lineal por mínimos cuadrados
def regresion_lineal(X, y):
    '''
    Calculo de la recta a partir de la regresión lineal por mínimos cuadrados de una señal RI.
    
    Parametros
    ----------
    X: array
        Array con los datos del tiempo.

    y: array
        Array con los valores en dB.
           
    return: Función con la recta aproximada.

    Ejemplo
    -------
    import numpy as np
    
    X = t
    y = data_1_suav_sch    
    regresion_lineal(X, y)
    '''
    
    # Cálculo de las medias
    X_mean = np.mean(X)
    y_mean = np.mean(y)
    
    # Cálculo de las desviaciones
    X_dev = X - X_mean
    y_dev = y - y_mean
    
    # Cálculo del producto de las desviaciones
    XY_dev = X_dev * y_dev
    
    # Cálculo del cuadrado de las desviaciones de X
    X_dev_sq = X_dev ** 2
    
    # Cálculo de los coeficientes de la regresión
    m = np.sum(XY_dev) / np.sum(X_dev_sq)
    b = y_mean - m * X_mean
    print(m/60,"Pendiente = ", m, "Intersección = ", b)
    # Crea la función de regresión lineal
    #def regression_function(x):
     #   return m * x + b
    
    return(m, b)

# Función cálculo de parámetros acústicos
def valor_cercano(lista, valor_buscado):
    """
    Calcula el valor más cercano a un cierto valor en dB dado.
    
    Parametros
    ----------
    lista: array
        Array con los datos de la señal.

    valor_buscado: float
        valo en dB que estoy buscando.
           
    return: (lista[indice], indice)
        lista[indice]: Valor hallado
        indice: índice del valor hallado

    Ejemplo
    -------
    import numpy as np
    lista=[1.2,2.3,3.2,4.6,5.2,6.4,7.5,8.6,9.1,10.4]
    valor_buscado = 4
    valor_cercano(lista, valor_buscado) 
    
    """
    dif = np.abs(lista-valor_buscado)
    indice = np.argmin(dif)
    return(lista[indice], indice)

def parametros_acústicos(data, limit, w_size=1000, fs=44100):
    """
    Calcula los parámetros acústicos.
    """
    list_param = []
    # Suavizo la señal con Hilbert, filtro promedio movil y Schroeder
    data_suav = suavizado_señal(data, w_size)
    data_suav_sch = schroeder(data, limit)
    
    # Transformo los datos a escala logarítmica
    log_data = esc_log(data)    
    data_suav_log = esc_log(data_suav)

    # Genero los linspace de tiempo
    t_data = np.linspace(0, len(data)/fs, num=len(data))
    t_sch = np.linspace(0, len(data_suav_sch)/fs, num=len(data_suav_sch))

    # Datos 
    X = t_sch
    y = data_suav_sch
    
    # T60 a partir de T10, T20, T30
    # EDT
    X_EDT = X[:valor_cercano(y, -10)[1]]
    y_EDT = data_suav_sch[:valor_cercano(y, -10)[1]]
    
    # T10
    X_T10 = X[valor_cercano(y, -5)[1]:valor_cercano(y, -15)[1]]
    y_T10 = data_suav_sch[valor_cercano(y, -5)[1]:valor_cercano(y, -15)[1]]

    # T20
    X_T20 = X[valor_cercano(y, -5)[1]:valor_cercano(y, -25)[1]]
    y_T20 = data_suav_sch[valor_cercano(y, -5)[1]:valor_cercano(y, -25)[1]]

    # T30
    X_T30 = X[valor_cercano(y, -5)[1]:valor_cercano(y, -35)[1]]
    y_T30 = data_suav_sch[valor_cercano(y, -5)[1]:valor_cercano(y, -35)[1]]

    #------------------------------------------
    # Llamada a la función de regresión lineal
    x_values = np.linspace(min(X), max(X), fs)
    m, b = regresion_lineal(X, y)
    #print("T: ", -m/60)
    #list_param.append(-m/60)

    # EDT
    x_values_edt = np.linspace(min(X), max(X), fs)
    m_EDT, b_EDT = regresion_lineal(X_EDT, y_EDT)
    print("EDT: ", -60/m_EDT)
    list_param.append(-60/m_EDT)
    
    # T10
    x_values_T10 = np.linspace(min(X), max(X), fs)
    m_T10, b_T10 = regresion_lineal(X_T10, y_T10)
    print("T10", -m_T10/60)
    list_param.append(-60/m_T10)

    # T20
    x_values_T20 = np.linspace(min(X), max(X), fs)
    m_T20, b_T20 = regresion_lineal(X_T20, y_T20)
    print("T20", -60/m_T20)
    list_param.append(-60/m_T20)

    # T30
    x_values_T30 = np.linspace(min(X), max(X), fs)
    m_T30, b_T30 = regresion_lineal(X_T30, y_T30)
    print("T30", -60/m_T30)
    list_param.append(-60/m_T30)

    #------------------------------------------
    # Generar valores para la línea de regresión
    y_values = m*x_values+b
    
    # EDT
    y_values_edt = m_EDT*x_values_edt+b_EDT

    # T10
    y_values_T10 = m_T10*x_values_T10+b_T10

    # T20
    y_values_T20 = m_T20*x_values_T20+b_T20

    # T30
    y_values_T30 = m_T30*x_values_T30+b_T30

    #------------------------------------------
    # Visualizar los datos y la línea de regresión    
    fig, ax = plt.subplots(nrows=1)
    ax.plot(t_data, log_data, label='Señal original')
    ax.plot(t_data, data_suav_log, label='Señal suavizada')
    ax.plot(x_values, y_values, label='Recta minimos cuadrados')
    ax.plot(x_values_edt, y_values_edt, label='Recta EDT')
    ax.plot(x_values_T10, y_values_T10, label='Recta T10')
    ax.plot(x_values_T20, y_values_T20, label='Recta T20')
    ax.plot(x_values_T30, y_values_T30, label='Recta T30')
    ax.plot(t_sch, data_suav_sch, label='Scroeder')
    ax.set_xlabel("tiempo en segundos")
    ax.set_ylabel("Amplitud en dB")
    ax.set_ylim(-100, 1)
    ax.legend()
    plt.show()
    print(list_param)
    return list_param

if __name__ == "__main__":
    file = 'signal-systems/trabajo_practico/noteboks/TP/Mediciones/Respuestas al impulso/IR2/Mono.wav'
    signal, fs = read_wav(file)
    log_signal = esc_log(signal)
    time_domain_plot(log_signal, fs)
    limit=int(input("ingrese el tiempo limite en segundos de la integración de Schroeder: "))
    parametros_acústicos(signal, limit)
    
    