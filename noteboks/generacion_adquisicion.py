import numpy as np
import pandas as pd
import soundfile as sf
import sounddevice as sd
from scipy.io.wavfile import write
from scipy import signal
from funciones import time_domain_plot
from funciones import read_wav

## Funcion de sintetización de Ruido Rosa
def ruidoRosa_voss_modified(t, fs=44100, ncols=16):
    """
    Genera ruido rosa utilizando el algoritmo de Voss-McCartney(https://www.dsprelated.com/showabstract/3933.php).
    
    .. Nota:: si 'ruidoRosa.wav' existe, este será sobreescrito
    
    Parametros
    ----------
    t : float
        Valor temporal en segundos, este determina la duración del ruido generado.
    fs: int
        Frecuencia de muestreo en Hz de la señal. Por defecto el valor es 44100 Hz.
    ncols: int
        Determina el número de fuentes a aleatorias a agregar.

    returns: NumPy array
        Datos de la señal generada.
    
    Ejemplo
    -------
    Generar un `.wav` desde un numpy array de 10 segundos con ruido rosa a una 
    frecuencia de muestreo de 44100 Hz.
    
        import numpy as np
        import pandas as pd
        import soundfile as sf
        from scipy.io.wavfile import write
        from scipy import signal
        
        ruidoRosa_voss(10)
    """
    nrows = int(t*fs)

    array = np.full((nrows, ncols), np.nan)
    array[0, :] = np.random.random(ncols)
    array[:, 0] = np.random.random(nrows)
    
    # el numero total de cambios es nrows
    n = nrows
    cols = np.random.geometric(0.5, n)
    cols[cols >= ncols] = 0
    rows = np.random.randint(nrows, size=n)
    array[rows, cols] = np.random.random(n)
    
    df = pd.DataFrame(array)
    filled = df.fillna(method='ffill', axis=0)
    total = filled.sum(axis=1)
    
    ## Centrado de el array en 0
    total = total - total.mean()
    
    ## Normalizado
    valor_max = max(abs(max(total)),abs(min(total)))
    total = total / valor_max
    
    # Agregar generación de archivo de audio .wav
    write('ruidoRosa.wav', fs, total)  # Save as WAV file 
        
    return total

## Funcion de generación de Sine Swep Logarítmico + Filtro Inverso
def log_sweep_invfilter(f1, f2, t_sweep, fs_sweep):
    """
    Genera Sine Sweep Logarítmico y su filtro inverso.
    
    .. Nota:: si 'SineSweepLog.wav' existe, este será sobreescrito
    
    Parametros
    ----------
    t_sweep: int  
        Duración en segundos del sweep
    fs_sweep: int
        Frecuencia de muestreo
    f1: int
        Frecuencia inferior
    f2: int
        Frecuencia superior
    
    returns: (x: NumPy array, k_t: NumPy array)
        x: Datos del sine sweep logarítmico
        k_t: Datos del filtro inverso
   
    Ejemplo
    -------
    Generar dos archivos `.wav` de 10 segundos con una señal Sine Sweep Logarítmica y un Filtro Inverso 
    entre las frecuencias de 20 a 4000 Hz a una frecuencia de muestreo de 44100 Hz.
    
    import numpy as np
    from matplotlib import pyplot as plt
    import soundfile as sf
    from scipy.io.wavfile import write
    from scipy import signal

    log_sweep_invfilter(20, 4000, 10, 44100)

    """
    t_swipe_arange = np.arange(0, t_sweep*fs_sweep)/fs_sweep  # Arreglo de muestreos
    R = np.log(f2/f1)  # Sweep rate
    K = t_sweep*2*np.pi*f1/R
    L = t_sweep/R
    w = (K/L)*np.exp(t_swipe_arange/L)
    m = f1/w
    # Sine Sweep Logarítmico
    x = np.sin(K*(np.exp(t_swipe_arange/L-1)))
    
    # Filtro Inverso
    k_t = x[::-1]*m
    
    # Agregar generación de archivo de audio .wav
    write('SineSweepLog.wav', fs_sweep, x)  # Save as WAV file 
    write('InvFilter.wav', fs_sweep, k_t)  # Save as WAV file 

    return x, k_t

# Adquisición y reproducción
def record_signal(signal, input_device, output_device):
    """
    Reproducción y grabación de una señal en formato ".wav" en simultáneo.
    ..Nota: Para saber los dispositivos de audio disponibles: sd.query_devices()
    
    Parámetros
    ----------
    signal: Archivo ".wav"

    input_device: int
        Dispositivo de grabación de audio.
    
    output_device: int
        Dispositivo de reproducción de audio.

    duration: 
        Tiempo de grabación de la señal.

    Para ver el listado de dispositivos de audio: 
    
    import sounddevice as sd
    sd.query_devices()
        
    Ejemplo
    -------
    import numpy as np
    import soundfile as sf
    import sounddevice as sd
    
    signal = 'SineSweepLog.wav'
    input_device = 1
    output_device = 4
    duration = 10
    record_signal(signal, input_device, output_device,duration)
    
    """
    # Selección de dispositivos de audio
    sd.default.device = input_device, output_device
    # Reproducción de la señal y grabación en simultáneo   
    data, fs = sf.read(signal, dtype='float32')
    duration = int(len(data)/fs)
    samples_rec = duration*fs
    val = data[0:samples_rec]
    signal_recording = sd.playrec(val, fs, channels=1)
    sd.wait()
    write('record_{}'.format(signal), fs, signal_recording)  # Guardo el archivo .wav
    return signal_recording

if __name__ == "__main__":
    # Ruido Rosa
    t = 10
    fs = 44100     
    ruido = ruidoRosa_voss_modified(t, fs)
    time_domain_plot(ruido,fs)
    
    # Sweep y filtro inverso
    log_sine_sweep, invfilt = log_sweep_invfilter(20, 4000, 10, 44100)
    time_domain_plot(log_sine_sweep,fs)
    time_domain_plot(invfilt,fs)

    # Adquisición y reproducción
    print(sd.query_devices())    
    input_device = int(input("Ingrese el dispositivo de entrada: "))
    output_device = int(input("Ingrese el dispositivo de salida: "))
    signal = 'SineSweepLog.wav'
    record_signal(signal, input_device, output_device)
    signal_rec, fs = read_wav('record_{}'.format(signal))
    time_domain_plot(signal_rec, fs)
