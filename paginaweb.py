import urllib2
import re
import time
import sqlite3
import schedule
from beebotte import *

API_KEY ='dDsQYLZMNIbcjAEV6bERyyUE'
SECRET_KEY ='o7HV8uWiUE36G82XSbI4JwpN8wo8VlDJ'
def tarea():

    url = 'https://www.meneame.net'
    respuesta= urllib2.urlopen(url)
    contenidoWeb= respuesta.read()

    patron_clics= re.compile(r'[0-9]+\sclics')
    clics=re.findall(patron_clics,contenidoWeb)
    muestra_primera_clics=clics[0].split(" ")
    patron_meneos= re.compile(r'>[0-9]+</a>\s')
    meneos=re.findall(patron_meneos,contenidoWeb)
    muestra_primera_meneos1=meneos[1].split("<")
    muestra_primera_meneos2=muestra_primera_meneos1[0].split(">")
    patron_titulo= re.compile(r'-title=(?:\".*?\")')
    titulo=re.findall(patron_titulo,contenidoWeb)
    muestra_primera_titulo=titulo[0].split("=")
    hora=time.strftime("%H:%M:%S")
    dia=time.strftime("%d/%m/%y")
    print muestra_primera_clics[0]
    print muestra_primera_meneos2[1]
    print muestra_primera_titulo[1]
    print hora
    print dia

    #Almacenamos todo lo que queremos pasar en datos.
    datos=(int(muestra_primera_clics[0]),int(muestra_primera_meneos2[1]),str(muestra_primera_titulo[1]),str(hora),str(dia))
    try:
	    con= sqlite3.connect('base_de_datos.db')
	    con.text_factory = str
	    cursor=con.cursor()
	    #cursor.execute("DROP TABLE IF EXISTS Datos")
	    #cursor.execute("CREATE TABLE Datos(Clics INTEGER, Meneos INTEGER, Titulo TEXT, Hora TEXT, Fecha TEXT)")
            #for datos in Datos:
            cursor.execute("INSERT INTO Datos VALUES(?, ?, ?, ?, ?)", datos)
	    con.commit()
	    print("Estadisticas insertadas correctamente")

	    cursor.execute("SELECT * FROM Datos")
   
	    Datos = cursor.fetchall()
	    print(Datos)
    except sqlite3.OperationalError as error:
	    print("Error al abrir:",error)

    bclient = BBT(API_KEY, SECRET_KEY)

    bclient.write('channel1', 'Clics', datos[0])
    bclient.write('channel2', 'Meneos', datos[1])
    bclient.write('channel3', 'Titulo', datos[2])
    bclient.write('channel4', 'Hora', datos[3])
    bclient.write('channel5', 'Fecha', datos[4])

    print("Datos introducidos en la nube correctamente")

schedule.every(120).seconds.do(tarea)

while True: 
	schedule.run_pending()
	time.sleep(1)
