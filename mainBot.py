import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy
import tflearn
import tensorflow
import json
import random
import pickle
import discord

#nltk.download('punkt')

#token para dicord
llave = "NzA0MjAxMzMwOTIyNjE4OTAw.XqZtTg.4P7FFZfrtKRtb1zXebXuxblArlU"

#abrien archivo .json
with open("contenido.json", encoding='utf-8') as archivo:
    datos = json.load(archivo)
try:
    with open("vriable.pickle","rb") as archivoPickle:
        palabras, tags, entrenamiento, salida = pickle.load(archivoPickle)
except:
    #asignando contenido
    palabras = []
    tags = []
    auxX = []
    auxY = []

    for contenido in datos["contenido"]:
        for patrones in contenido["patrone"]:
            auxPalabra = nltk.word_tokenize(patrones)
            palabras.extend(auxPalabra)
            auxX.append(auxPalabra)
            auxY.append(contenido["tag"])

            if contenido["tag"] not in tags:
                tags.append(contenido["tag"])


    #entrenamiento de I.A
    palabras = [stemmer.stem(w.lower()) for w in palabras if w != "?"] 
    palabras = sorted(list(set(palabras)))
    tags = sorted(tags)

    entrenamiento = []
    salida = []

    salidaVacia = [0 for _ in range(len(tags))]

    for x, documento in enumerate(auxX):
        cubeta = []
        auxPalabra = [stemmer.stem(w.lower()) for w in documento]
        for w in palabras:
            if w in auxPalabra:
                cubeta.append(1)
            else:
                cubeta.append(0)

        filaSalida = salidaVacia[:]
        filaSalida[tags.index(auxY[x])] = 1
        entrenamiento.append(cubeta)
        salida.append(filaSalida)

        #creando archivo de variable
        with open("vriable.pickle","wb") as archivoPickle:
            pickle.dump((palabras, tags, entrenamiento, salida),archivoPickle)    
    #Convirtien listas en array
    entrenamiento = numpy.array(entrenamiento)
    salida = numpy.array(salida)

#Crenado red neuronal
tensorflow.reset_default_graph()

red = tflearn.input_data(shape=[None,len(entrenamiento[0])])
red = tflearn.fully_connected(red,10)
red = tflearn.fully_connected(red,10)
red = tflearn.fully_connected(red,len(salida[0]),activation="softmax")
red = tflearn.regression(red)

#modelo de la red neuronal
modelo = tflearn.DNN(red)

try:
    #creando archivo de red neuronal
    modelo.load("modelo.tflearn")
except:
    modelo.fit(entrenamiento, salida, n_epoch=1000, batch_size=11, show_metric=True)
    modelo.save("modelo.tflearn")

def mainBot():
    global llave
    cliente = discord.Client()
    while True:
        #entrada = input("Tu: ") // se utilizo para pruebas en consola
        @cliente.event
        async def on_message(mensaje):
            #validando que el bot no se responda a el msimo
            if mensaje.author == cliente.user:
                return

            cubeta = [0 for _ in range(len(palabras))]
            #si va usar la prueba en consola cambiar mensaje.content por la variable entrada
            entradaProcesada = nltk.word_tokenize(mensaje.content)
            entradaProcesada = [stemmer.stem(palabra.lower()) for palabra in entradaProcesada]
            for palabraIndividual in entradaProcesada:
                for i,palabra in enumerate(palabras):
                    if palabra == palabraIndividual:
                        cubeta[i] = 1
            resultado = modelo.predict([numpy.array(cubeta)])
            resultadoIndice = numpy.argmax(resultado)
            tag = tags[resultadoIndice]

            for tagAux in datos["contenido"]:
                if tagAux["tag"] == tag:
                    respuesta = tagAux["respuestas"]

            #aqui se manda la respuesta a discord
            await mensaje.channel.send(random.choice(respuesta))
            #print("BOT: ",random.choice(respuesta)) //se utilizaba para pruebas en consola
        cliente.run(llave)
mainBot()