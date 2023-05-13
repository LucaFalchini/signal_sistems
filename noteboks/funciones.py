import numpy as np
from matplotlib import pyplot as plt
from scipy import signal
import soundfile as sf
import sounddevice as sd
from ipywidgets import Button
from tkinter import Tk, filedialog
from IPython.display import clear_output, display

def read_wav(file):
    """
    Cargar un archivo ".wav".
    
    Parametros
    ----------
    file: Archivo ".wav"
        
    return: Numpy array

    Ejemplo
    -------
    import numpy as np
    import soundfile as sf
    
    file = 'ruidoRosa.wav'
    read_wav(file)

    """
    data, fs = sf.read(file, dtype='float32')
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

files = []
wav_list = []
def select_files(b, files=files):    
    clear_output()
    files.clear() 
    wav_list.clear() 
    root = Tk()
    root.withdraw() # Hide the main window.
    root.call('wm', 'attributes', '.', '-topmost', True) # Raise the root to the top of all windows.
    files.append(filedialog.askopenfilenames(filetypes = [('Wav', '.wav'),('Mp3', '.mp3'),('Wma', '.wma')])) # List of selected files will be set button's file attribute.
    print(files) # Print the list of files selected.
     
    for i in range(len(files[0])):  # Bucle para almacenar los datos de los archivos en una lista.
        wav = read_wav(files[0][i])
        wav_list.append(wav)

if __name__ == '__main__':
    time_domain_plot()
    read_wav()
    