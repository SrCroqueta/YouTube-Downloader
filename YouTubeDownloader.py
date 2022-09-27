import os
from tkinter import *
from PIL import ImageTk, Image
from win10toast import ToastNotifier
from pytube import YouTube

root = Tk()

iconWindow = "./assets/YouTubeDownloader.ico"
logoApp = "./assets/YouTubeDownloader.png"
appName = "Youtube Downloader"

root.title(appName)

window_width = 550
window_height = 250

# Obtiene las dimensiones de la ventana
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Encuentra el punto central
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)

root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}') # Centra la ventana
root.resizable(False, False) # Evita que se pueda alterar el tamaño de la ventana
root.iconbitmap(iconWindow) # Cambia el icono predefinido por el asignado

youtubeURL = StringVar()
youtubeURL.set('')

# imagen
img = ImageTk.PhotoImage(data=open(logoApp, "rb").read())

imgLabel = Label(root, image = img)
imgLabel.place(x = 25, y = 25)

titleLabel = Label(root, text = "YouTube Downloader", font = ('Impact', 32), fg = 'black')
titleLabel.place(x = 155, y = 45)

textLabel = Label(root, text = "YouTube URL:", font = ('Arial', 12), fg = 'black')
textLabel.place(x = 20, y = 128)

youtubeURL = Entry(root, font = ('Arial', 12, ''), textvariable = youtubeURL, justify = 'center')
youtubeURL.place(x = 130, y = 125, width = 380, height = 30)

creditsLabel = Label(root, text = "Twitter: @SrCroqueta_\nGitHub: SrCroqueta", font = ('Arial', 8, ''), fg = 'black', justify = 'left')
creditsLabel.place(x = 10, y = 210)

def submit():
    try:
        yt = YouTube(str(youtubeURL.get()))
        video = yt.streams.get_highest_resolution()

        destination = os.getenv('USERPROFILE')+r'\Downloads'

        out_file = video.download(output_path = destination)

        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp4'
        os.rename(out_file, new_file)

        length = len(destination)+1

        nameForNotifier = new_file[length:]

        ToastNotifier().show_toast(appName, f"{nameForNotifier} ha sido descargado con éxito.", duration = 5, icon_path = iconWindow, threaded=True)
    except:
        ToastNotifier().show_toast(appName, "Fallo en la descarga.", duration = 5, icon_path = iconWindow, threaded=True)

btn = Button(root, text = 'Descargar', font = ('Arial', 14), bd = '2', command = submit, width = 20)
btn.place(x = 160, y = 170)

# Loop infinito requerido para que el programa funcione de manera indefinida hasta que se indique lo contrario
root.mainloop()
