
import speech_recognition as sr
import subprocess as sub
import pyttsx3, pywhatkit, wikipedia, datetime, keyboard, os
from pygame import mixer

name="Oparin"
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)
engine.setProperty('rate', 145)

#diccionario
sites={
    'google':'google.com',
    'youtube':'youtube.com',
    'whatsapp':'web.whatsapp.com',
    'cursos':'freecodecamp.org/lear'
}

#funcion para convertir texto a audio
def talk(text):
    engine.say(text)
    engine.runAndWait()

#funcion de escuchar
def listen():
    try:
        with sr.Microphone() as source:
            talk("escuchando...")
            pc = listener.listen(source) # guarda el audio ingresado desde el microfono en una variable
            rec = listener.recognize_google(pc, language='es')
            rec = rec.lower()#convierte en texto en minuscula
            if name in rec:
                rec = rec.replace(name, '')

    except:
        pass
    return rec

#funcion principal
def run_IA():
    while True:
        rec = listen()
        if 'reproduce' in rec:
            music = rec.replace('reproduce', '')
            print("Reproduciendo" + music)
            talk("Reproduciendo" + music)
            pywhatkit.playonyt(music)
        elif 'busca' in rec:
            search = rec.replace('busca', '')
            wikipedia.set_lang("es")
            wiki = wikipedia.summary(search, 1)#Guarda en una variable lo encontrado
            print(search + ": " + wiki)
            talk(wiki)
        elif 'alarma' in rec:
            num = rec.replace('alarma',  '')
            num = num.strip()
            talk("Alarma activada a las " + num + "horas")
            while True:
                if datetime.datetime.now().strftime('%H:%M') == num:
                    print("despierta")
                    mixer.init()
                    mixer.music.load("alarma.mp3")
                    if keyboard.read_key() == "s":
                        mixer.music.stop()
                        break
        elif 'abre' in rec:
            for site in sites:
                if site in rec:
                    sub.call(f'start chrome.exe {sites[site]}', shell=True)
                    talk(f'Abriendo{site}')
        elif 'escribe' in rec:
            try:
                with open("nota.txt", 'a') as f:
                    write(f)
            except FileNotFoundError as e:
                file = open("nota.txt", 'w')
                write(file)
        elif 'termina' in rec:
            talk('Adios')
            break

#funcion para escribir en un archivo de texto
def write(f):
    talk("¿Que deseas que escriba?")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("Listo, puedes revisar el contenido del archivo")
    sub.Popen("nota.txt", shell=True)

if __name__ == '__main__':
    run_IA()