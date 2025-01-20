import os, sys
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk
from win10toast import ToastNotifier
from yt_dlp import YoutubeDL
import threading

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

root = Tk()

iconWindow = resource_path("./assets/icon.ico")
logoApp = resource_path("./assets/logo.png")
appName = "YouTube Downloader"

root.title(appName)

# Estilo para botones.
styles = Style()
styles.configure('W.TButton', font = ('Arial', 14), width = 20)

window_width = 550
window_height = 320

# Obtiene las dimensiones de la ventana
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Encuentra el punto central
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)

root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}') # Centra la ventana
root.resizable(False, False) # Evita que se pueda alterar el tamaño de la ventana
root.iconbitmap(iconWindow) # Cambia el icono predefinido por el asignado

# Se define la varitable que almacenará la URL y se le da un valor vacío por defecto
youtubeURL = StringVar()
youtubeURL.set('')

# Lee la imagen como binario
img = ImageTk.PhotoImage(data=open(logoApp, "rb").read())

# Introduce la imagen dentro de la ventana principal con 'Label'
imgLabel = Label(root, image = img)
imgLabel.place(x = 25, y = 25)

# Título  creado con texto en un 'Label'
titleLabel = Label(root, text = appName, font = ('Impact', 32))
titleLabel.place(x = 155, y = 40)

# Simplemente un texto en un 'Label'
textLabel = Label(root, text = "YouTube URL:", font = ('Arial', 12))
textLabel.place(x = 20, y = 128)

# Campo de entrada con 'Entry' para introducir las direcciones a los vídeos de YouTube
youtubeURL = Entry(root, font = ('Arial', 12, ''), textvariable = youtubeURL, justify = 'center')
youtubeURL.place(x = 130, y = 125, width = 380, height = 30)

# Barra de progreso
progressTitle = Label(root, text="PROGRESO DE DESCARGA", font=('Arial', 8, 'bold'), justify='center')
progressTitle.place(x=205, y=220)

progress = Progressbar(root, orient=HORIZONTAL, length=400, mode='determinate')
progress.place(x=70, y=240)

# Unos simples créditos
blueskyLabel = Label(root, text="Bluesky:", font=('Arial', 8, 'bold'), justify='left')
blueskyLabel.place(x=10, y=280)

gitHubLabel = Label(root, text="GitHub:", font=('Arial', 8, 'bold'), justify='left')
gitHubLabel.place(x=10, y=295)

# Texto adicional
creditsLabel = Label(root, text="@srcroqueta.bsky.social", font=('Arial', 8), justify='left')
creditsLabel.place(x=65, y=280)  # Ajusta la posición de acuerdo al texto
creditsLabel = Label(root, text="SrCroqueta", font=('Arial', 8), justify='left')
creditsLabel.place(x=55, y=295)  # Ajusta la posición de acuerdo al texto

# Detecta si el script está compilado y establece la ruta base
if getattr(sys, 'frozen', False):  # Detecta si está compilado
    base_path = sys._MEIPASS  # Ruta temporal que usa PyInstaller
else:
    base_path = os.path.abspath(".")  # Ruta base en modo normal

# Rutas a los ejecutables yt-dlp y ffmpeg
yt_dlp_path = os.path.join(base_path, "yt-dlp.exe")  # Ruta para yt-dlp
ffmpeg_path = os.path.join(base_path, "ffmpeg.exe")  # Ruta para ffmpeg

# Verifica si los archivos existen
if not os.path.exists(yt_dlp_path):
    raise FileNotFoundError(f"No se encontró 'yt-dlp.exe' en {yt_dlp_path}.")
if not os.path.exists(ffmpeg_path):
    raise FileNotFoundError(f"No se encontró 'ffmpeg.exe' en {ffmpeg_path}.")

# Función 'destinationPath()' para obtener el perfil del usuario mediante una variable de entorno y así obtener el directorio 'Downloads' (Descargas)
def destinationPath():
    return os.path.join(os.getenv('USERPROFILE'), 'Downloads')

# Función 'lengthPath()' calcula el tamaño del string de la ruta en la que se va a guardar y le suma '1'
def lengthPath():
    return len(destinationPath()) + 1

# Hook para mostrar el progreso
def progress_hook(d):
    if d['status'] == 'downloading':
        progress['value'] = d['downloaded_bytes'] * 100 / d['total_bytes']
        root.update_idletasks()

# Función para manejar la descarga de video de forma separada (usando threading)
def download_video():
    try:
        url = str(youtubeURL.get())
        output_path = destinationPath()
        
        # Usar yt-dlp con la opción de fusión de audio y video
        ydl_opts = {
            'format': 'bv+ba',  # Video y audio mejor
            'merge_output_format': 'mp4',  # Fusionar a formato mp4
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'ffmpeg_location': ffmpeg_path,  # Indica la ubicación de ffmpeg
            'progress_hooks': [progress_hook],  # Agregar hook de progreso
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        ToastNotifier().show_toast(appName, f'El archivo de vídeo aparecerá en:\n{output_path}', duration=5, icon_path=iconWindow, threaded=True)
    except Exception as e:
        print(f"Error al descargar el video: {e}")
        ToastNotifier().show_toast(appName, "Fallo en la descarga.", duration=5, icon_path=iconWindow, threaded=True)

# Función de descarga de audio
def download_audio(url, output_path):
    ydl_opts = {
        'format': 'bestaudio',  # Mejor calidad de audio
        'extractaudio': True,  # Extrae solo el audio
        'audioformat': 'mp3',  # Convierte a MP3
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),  # Ruta y formato de salida
        'progress_hooks': [progress_hook],  # Actualiza la barra de progreso
        'ffmpeg_location': ffmpeg_path,  # Ubicación de ffmpeg
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Función 'submitVideo()' para iniciar la descarga en un hilo separado
def submitVideo():
    progress['value'] = 0  # Resetear la barra de progreso antes de iniciar la descarga
    # Crear un hilo para descargar el video sin bloquear la interfaz
    download_thread = threading.Thread(target=download_video)
    download_thread.start()

# Función 'submitSound()' para el botón que descargará solo el audio
def submitSound():
    try:
        url = str(youtubeURL.get())
        output_path = destinationPath()
        # Llamamos a la función de descarga de audio
        download_audio(url, output_path)

        ToastNotifier().show_toast(appName, f'El archivo de audio aparecerá en:\n{output_path}', duration=5, icon_path=iconWindow, threaded=True)
    except Exception as e:
        print(f"Error al descargar el audio: {e}")
        ToastNotifier().show_toast(appName, "Fallo en la descarga.", duration=5, icon_path=iconWindow, threaded=True)

# Se crea un botón de descarga el vídeo que usará la función submitVideo
btnV = Button(root, text = 'Descargar', style = 'W.TButton', command = submitVideo)
btnV.place(x = 34, y = 170)

#btnS = Button(root, text = 'Convertir a .MP3', font = ('Arial', 14), bd = '2', command = submitSound, width = 20)
btnS = Button(root, text = 'Convertir a .MP3', style = 'W.TButton', command = submitSound)
btnS.place(x = 286, y = 170)

# Loop infinito requerido para que el programa funcione de manera indefinida hasta que se indique lo contrario
root.mainloop()


# Loop infinito requerido para que el programa funcione de manera indefinida hasta que se indique lo contrario
root.mainloop()
