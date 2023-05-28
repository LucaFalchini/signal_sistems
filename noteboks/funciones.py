import numpy as np
from matplotlib import pyplot as plt
from scipy import signal
import soundfile as sf
import sounddevice as sd
from tkinter import *
from IPython.display import clear_output, display
from tkinter import filedialog

def read_wav(file):
    """
    Cargar un archivo ".wav".
    
    Parametros
    ----------
    file: Archivo ".wav"
        
    return: (Numpy array, frecuencia de muestreo) 

    Ejemplo
    -------
    import numpy as np
    import soundfile as sf
    
    file = 'ruidoRosa.wav'
    read_wav(file)

    """
    data, fs = sf.read(file)
    return(data, fs)

def time_domain_plot(data, fs, graph_name=" "):
    """
    Genera el gráfico del dominio temporal de una señal.
    
    Parametros
    ----------
    data: Numpy array

    fs: Frecuencia de muestreo

    graph_name: str, nombre del gráfico
        
    return: Gráfico del dominio temporal de la señal

    Ejemplo
    -------
    import numpy as np
    from matplotlib import pyplot as plt
    import soundfile as sf
    
    file = 'ruidoRosa.wav'
    time_domain_plot(file)

    """
    
    rate = len(data)       
    time = np.linspace(0, rate/fs, num=rate)  # Objeto Numpy para la duración en el eje x
        
    # Grafico
    plt.figure(figsize=(15, 5))
    plt.plot(time, data, linewidth=0.5)
    plt.title(f'Gráfico {graph_name} Dominio del tiempo')
    plt.ylabel('Amplitud')
    plt.xlabel('Tiempo [s]')
    plt.show()
    return()

def reproducir(filename):
    'Función para reproducir audio'

    # Extract data and sampling rate from file
    data, fs = sf.read(filename, dtype='float32')  
    sd.play(data, fs)
    status = sd.wait()  # Wait until file is done playing
    return data

def esc_log(data_impulse, a = 20):
    """
    Convierte un array a escala logarítmica.
    
    Parametros
    ----------
    data_impulse: Numpy array

    a: int, factor de multiplicación del logaritmo. Por defecto es 20.
      
    return: Numpy array a escala logarítmica

    Ejemplo
    -------
    import numpy as np
    import soundfile as sf
    
    data_impulse, fs = sf.read("impulso_aula2.wav")    #Llamo a la funcion con la señal "impulso.wav"
    B = esc_log(data_impulse)   

    """
    A = data_impulse/(np.max(np.abs(data_impulse)))
    Norm_log = a * np.log10(A)
    return Norm_log

def analisis_frecuencias(audio, fs):
    '''
    Calcular la transformada de Fourier de la señal de audio y graficarla.

    '''        
    audio = audio / np.max(np.abs(audio))  # Normalizar los valores de la señal
    fft_data = np.fft.fft(audio)

    # Calcular los valores de frecuencia correspondientes
    fft_freq = np.fft.fftfreq(len(audio), 1.0 / fs)

    # Tomar solo la mitad de los datos (la otra mitad es simétrica)
    fft_data = esc_log(np.abs(fft_data[:len(audio)//2]))
    fft_freq = fft_freq[:len(audio)//2]

    # Graficar el análisis de frecuencia
    plt.semilogx(fft_freq, fft_data)
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Amplitud (dB)')
    plt.title('Análisis de frecuencia de audio')
    plt.grid(True)
    custom_xticks = [31.5, 63, 125, 250, 1000, 4000, 16000]
    plt.xticks(custom_xticks, custom_xticks)
    plt.fill_between(fft_freq, fft_data, np.min(fft_data))
    plt.show()
    return(fft_data)

if __name__ == '__main__':
    file = 'signal-systems/trabajo_practico/noteboks/TP/Mediciones/Respuestas al impulso/IR2/Mono.wav'
    data, fs = read_wav(file)
    def graph_1():
        time_domain_plot(data, fs, graph_name="impulso")
    def play():
        reproducir(file)

    window = Tk()
    button = Button(window, 
                    text="Plot", 
                    command=graph_1, 
                    font=("Arial", 16),
                    fg="blue")
    button2 = Button(window, 
                    text="Play", 
                    command=play, 
                    font=("Arial", 16),
                    fg="blue")

    button.pack()
    button2.pack()
    window.mainloop()
    

    
    
    