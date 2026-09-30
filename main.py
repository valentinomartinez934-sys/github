import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import requests

puntos = 0
contador = 1

print("esto es un programa para mejorar la pronunciacion en ingles, al acabar de repite")


while contador > 0:
    print("puntos actuales: ", puntos)
    dificultad = input("eliga dificultad (facil,medio,dificil):")

    if dificultad == "facil":
        url = "https://random-word-api.herokuapp.com/word?lang=es&number=1&diff=1"
        #url = "https://random-word-api.herokuapp.com/languages"
        response = requests.get(url)
        palabras = response.json()
        print(palabras)
    elif dificultad == "medio":
        url = "https://random-word-api.herokuapp.com/word?lang=es&number=1&diff=3"
        #url = "https://random-word-api.herokuapp.com/languages"
        response = requests.get(url)
        palabras = response.json()
        print(palabras)
    elif dificultad == "dificil":
        url = "https://random-word-api.herokuapp.com/word?lang=es&number=1&diff=5"
        #url = "https://random-word-api.herokuapp.com/languages"
        response = requests.get(url)
        palabras = response.json()
        print(palabras)

    duration = 7  # segundos de grabación
    sample_rate = 44100
    print("Habla ahora...")


    recording = sd.rec(
    int(duration * sample_rate), # el número de muestras a grabar
    samplerate=sample_rate,      # tasa de muestreo
    channels=1,                  # 1 significa grabación mono
    dtype="int16")               # tipo de datos para las muestras grabadas


    sd.wait()  # esperando a que termine la grabación
    wav.write("output.wav", sample_rate, recording)
    print("Grabación completa, ahora reconociendo...")

    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)


    try:
        text = recognizer.recognize_google(audio, language="es")
        print("Dijiste:", text)


    except sr.UnknownValueError:             # - si Google no pudo entender el habla debido a ruido o silencio
        print("No se pudo reconocer el habla.")
    except sr.RequestError as e:             # - si no hay conexión a Internet o la API no está disponible
        print(f"Error del servicio: {e}")

    translator = Translator()
    translated = translator.translate(text, dest="es")  

    if text == palabras:
        print("has pronunciado bien la palabra")
        puntos += 1
    else:
        print("has pronunciado mal la palabra")

    seguir = input("quieres probar devuelta?(S/N)")
    if seguir == "N":
        contador = 0
        print("Fin.")