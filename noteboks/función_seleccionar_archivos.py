from tkinter import *
from IPython.display import clear_output, display
from tkinter import filedialog
from funciones import read_wav

files_list = []
wav_list = []
def select_files():
    '''
    Carga archivos de audio en formato '.wav', '.wma', '.mp3'
    y los almacena en una lista de tuplas (Numpy array, frecuencia de muestreo).
    
    Parametros
    ----------
    
    fs: Frecuencia de muestreo

    graph_name: str, nombre del gráfico
        
    return: Gráfico del dominio temporal de la señal

    Ejemplo
    -------
    from tkinter import *
    from IPython.display import clear_output, display
    from tkinter import filedialog
    from funciones import read_wav
    
    select_files()
    

    '''    
    clear_output()
    files_list.clear() 
    wav_list.clear() 
    root = Tk()
    root.withdraw() # Hide the main window.
    root.call('wm', 'attributes', '.', '-topmost', True) # Raise the root to the top of all windows.
    files_list.append(filedialog.askopenfilenames(filetypes = [('Wav', '.wav'),('Mp3', '.mp3'),('Wma', '.wma')])) # List of selected files will be set button's file attribute.  
    print(files_list) # Print the list of files selected.
    
    for i in range(len(files_list[0])):  # Bucle para almacenar los datos de los archivos en una lista.
        wav = read_wav(files_list[0][i])
        wav_list.append(wav)
  

if __name__ == "__main__":
    window = Tk()
    button = Button(window, 
                    text=" Seleccione el/los archivo/os de audio", 
                    command=select_files, 
                    font=("Arial", 16),
                    fg="blue")
    button.pack()
    window.mainloop()
   


    


