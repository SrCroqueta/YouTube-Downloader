import os
from tkinter import *
from PIL import ImageTk, Image
from win10toast import ToastNotifier
from pytube import YouTube

root = Tk()

iconWindow = "./assets/YouTubeDownloader.ico"
logoApp = "./assets/YouTubeDownloader.png"
appName = "YouTube Downloader"

root.title(appName)

window_width = 550
window_height = 260

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
titleLabel = Label(root, text = appName, font = ('Impact', 32), fg = 'black')
titleLabel.place(x = 155, y = 40)

# Simplemente un texto en un 'Label'
textLabel = Label(root, text = "YouTube URL:", font = ('Arial', 12), fg = 'black')
textLabel.place(x = 20, y = 128)

# Campo de entrada con 'Entry' para introducir las direcciones a los vídeos de YouTube
youtubeURL = Entry(root, font = ('Arial', 12, ''), textvariable = youtubeURL, justify = 'center')
youtubeURL.place(x = 130, y = 125, width = 380, height = 30)

# Unos simples créditos
creditsLabel = Label(root, text = "Twitter: @SrCroqueta_\nGitHub: SrCroqueta", font = ('Arial', 8, ''), fg = 'black', justify = 'left')
creditsLabel.place(x = 10, y = 220)

# Función 'destinationPath()' para obtener el perfil del usuario mediante una variable de entorno y así obtener el directorio 'Downloads' (Descargas)
def destinationPath():
    destination = os.getenv('USERPROFILE')+r'\Downloads'
    return(destination)

# Función 'lengthPath()' calcula el tamaño del string de la ruta en la que se va a guardar y le suma '1'
def lengthPath():
    length = len(destinationPath())+1
    return(length)

# Función 'submitVideo()' para el botón que descargará el vídeo
def submitVideo():
    try:
        yt = YouTube(str(youtubeURL.get())) # Obtiene el enlace introducido por el usuario
        video = yt.streams.get_highest_resolution() # Obtiene la resolución más alta del vídeo que se puede descargar

        out_file = video.download(output_path = destinationPath()) # Usa lo anterior guardado en la función 'destinationPath()' para guardar el archivo en la ruta indicada

        base, ext = os.path.splitext(out_file) # Obtiene el nombre del archivo separándolo de la ruta en la que se ha almacenado
        new_file = base + '.mp4' # Con el nombre del archivo obtenido le añade la extensión '.mp4'
        os.rename(out_file, new_file) # Guarda el archivo en la ruta indicada con el nuevo nombre con extensión

        nameForNotifier = new_file[lengthPath():] # Usando la función 'lengthPath()' obtenemos solamente el nombre del archivo con la extensión para usarlo en una notificación de Windows

        # Notificación de Windows una vez el archivo ha sido descargado
        ToastNotifier().show_toast(appName, f"{nameForNotifier} ha sido descargado con éxito.", duration = 5, icon_path = iconWindow, threaded=True)
    except:
        # En caso de que la descarga falle saltará esta notificación
        ToastNotifier().show_toast(appName, "Fallo en la descarga.", duration = 5, icon_path = iconWindow, threaded=True)

# Función 'submitSound()' para el botón que descargará solo el audio
def submitSound():
    try:
        yt = YouTube(str(youtubeURL.get())) # Obtiene el enlace introducido por el usuario
        video = yt.streams.filter(only_audio=True).first() # Solo obtiene el audio del vídeo

        out_file = video.download(output_path = destinationPath()) # Usa lo anterior guardado en la función 'destinationPath()' para guardar el archivo en la ruta indicada

        base, ext = os.path.splitext(out_file) # Obtiene el nombre del archivo separándolo de la ruta en la que se ha almacenado
        new_file = base + '.mp3' # Con el nombre del archivo obtenido le añade la extensión '.mp3'
        os.rename(out_file, new_file) # Guarda el archivo en la ruta indicada con el nuevo nombre con extensión

        nameForNotifier = new_file[lengthPath():] # Usando la función 'lengthPath()' obtenemos solamente el nombre del archivo con la extensión para usarlo en una notificación de Windows

        # Notificación de Windows una vez el archivo ha sido descargado
        ToastNotifier().show_toast(appName, f"{nameForNotifier} ha sido descargado con éxito.", duration = 5, icon_path = iconWindow, threaded=True) 
    except:
        # En caso de que la descarga falle saltará esta notificación
        ToastNotifier().show_toast(appName, "Fallo en la descarga.", duration = 5, icon_path = iconWindow, threaded=True)

# Se crea un botón de descarga el vídeo que usará la función submitVideo
btn = Button(root, text = 'Descargar', font = ('Arial', 14), bd = '2', command = submitVideo, width = 20)
btn.place(x = 30, y = 170)

btn = Button(root, text = 'Convertir a .MP3', font = ('Arial', 14), bd = '2', command = submitSound, width = 20)
btn.place(x = 290, y = 170)

# Loop infinito requerido para que el programa funcione de manera indefinida hasta que se indique lo contrario
root.mainloop()
