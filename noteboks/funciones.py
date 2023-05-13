import numpy as np
import soundfile as sf

def get_audio (file):
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
    time_domain_plot(file)

    """
    data, fs = sf.read(file)
    rate = len(data)       
    time = np.linspace(0, rate/fs, num=rate)  # Objeto Numpy para la duración en el eje x