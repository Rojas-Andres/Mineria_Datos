import csv
import io
import re
from pprint import pprint
positivas=dict()
negativas=dict()
encoding='UTF-8'
#archivo_negativo=open()
with open('negativas.txt','r') as f:
    for linea in f:
        linea=linea.rstrip("\n")
        negativas[linea]=0

with open('positive.txt','r') as f:
    for linea in f:
        linea=linea.rstrip("\n")
        positivas[linea]=0
#pprint(positivas)
descripcion_tweet=list()
ver=0
with open('menciones_alejo_url.txt','r',encoding=encoding) as archivo:
    datos=csv.reader(archivo,delimiter='|')
    #pprint(datos)

    for linea in datos:
        if linea[1]!="Alejandro Eder":
            description=linea[3].split()
            #print(len(description))
            for i in range(len(description)-1):
                palabra2=description[i]+" "+description[i+1]
                #print(palabra2)
                if description[i] in positivas:
                    positivas[description[i]]+=1
                if palabra2 in positivas:
                    positivas[palabra2]+=1
                if description[i] in negativas:
                    negativas[description[i]]+=1
                if palabra2 in negativas:
                    negativas[palabra2]+=1
        '''
        for palabra in description:
            palabra=palabra.lower()
            if palabra in positivas:
                positivas[palabra]+=1
            if palabra in negativas:
                    negativas[palabra]+=1
        '''
archivo_palabras_positivas=io.open("mayor_positivas_eder.txt","w",encoding=encoding)
for llave,valor in positivas.items():
    if valor>0:
        archivo_palabras_positivas.write("{}={}\n".format(llave,valor))
archivo_palabras_positivas.close()
archivo_palabras_negativas=io.open('mayor_negativas_eder.txt','w',encoding=encoding)
for llave,valor in negativas.items():
    if valor>0:
        archivo_palabras_negativas.write("{}={}\n".format(llave,valor))
archivo_palabras_negativas.close()
