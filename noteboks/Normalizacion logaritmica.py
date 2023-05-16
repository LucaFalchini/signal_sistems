

def esc_log (data_impulse, a = 20):
    A = data_impulse/(np.max(np.abs(data_impulse)))  #normalizacion
    Norm_log = a * np.log10(A)
    return Norm_log


data_impulse, fs= sf.read("impulso.wav")    #Llamo a la funcion con la señal "impulso.wav"
B = esc_log(data_impulse)

sp.write('Norm_Log.wav', fs, B)             #Escribo como wav a la normalizacion , para graficar
from funciones import time_domain_plot
fs = 44100
time_domain_plot(B, fs)

