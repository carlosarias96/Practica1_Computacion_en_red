from flask import Flask, render_template, request,redirect
import sqlite3
from beebotte import *

API_KEY ='dDsQYLZMNIbcjAEV6bERyyUE'
SECRET_KEY ='o7HV8uWiUE36G82XSbI4JwpN8wo8VlDJ'

media_local=0
media_exterior=0

app= Flask(__name__)

@app.route('/')
def layout2():
    return render_template('layout2.html')

@app.route('/inicio', methods=['GET','POST'])
def inicio():
  if request.method == 'POST' and request.form['Beebotte'] == 'Graficas externas':
      return redirect("https://beebotte.com/dash/e7491450-e446-11e8-a9e5-9db85b2d1393", code=302)
  else:
    con= sqlite3.connect('base_de_datos.db')
    cursor=con.cursor()
    cursor.execute("SELECT * FROM Datos ORDER BY Clics DESC, Meneos DESC, Titulo DESC, Hora DESC, Fecha DESC")
    print(cursor.fetchone()[0])
    print(cursor.fetchone()[1])
    print(cursor.fetchone()[2])
    print(cursor.fetchone()[3])
    print(cursor.fetchone()[4])
    return render_template('inicio2.html', Datos=cursor.fetchone())


@app.route('/umbral', methods=['GET','POST'])
def umbral():
	umb= 0
	cuenta=0
	
	if request.method == 'POST':
	  superan = []
	  umb=request.form['Umbral']
	  con=sqlite3.connect('base_de_datos.db')
	  cursor=con.cursor()
	  cursor.execute("SELECT * FROM Datos ORDER BY Meneos DESC, Titulo DESC, Hora DESC, Fecha DESC")
	  Datos=cursor.fetchall()
	  for dato in Datos:
	  	if float(umb)< dato[0] and cuenta < 10:
	  		superan[0+cuenta*4:4+cuenta*4]= [dato[1],dato[2],dato[3],dato[4]]
	  		cuenta=cuenta+1
	  		print (dato)
	        long=range(len(superan)/4)
	        
	  return render_template('umbral2.html', umbral=umb, pasan=superan,longitud=long,veces=cuenta)
	else:
          return render_template('umbral2.html',umbral=umb,veces=cuenta)

@app.route('/media', methods=['GET', 'POST'])
def media():
  
  global media_local
  global media_exterior
  if request.method == 'POST':
      if request.form['Media'] == 'Local':
        media_local=0
        vueltas=0
   	con= sqlite3.connect('base_de_datos.db')
   	cursor=con.cursor()
   	cursor.execute("SELECT * FROM Datos")
   	Datos=cursor.fetchall()
   	num=len(Datos)
   	print(Datos)
   	print(num)
   	for dato in Datos:
   	  media_local = media_local+dato[vueltas*5]
	  print(vueltas*5)
   	  print(dato[vueltas*5])
   	media_local = media_local/num
        return render_template('media2.html', media=media_local, datos=media_exterior)
      elif request.form['Media'] == 'Externa':
          media_exterior=0
          bclient= BBT( API_KEY, SECRET_KEY)
          leer=bclient.read('channel1', 'Clics', limit=200)
          tot=len(leer)
          for lectura in range(len(leer)):
    	    media_exterior=media_exterior+int(leer[lectura] ['data'])
          media_exterior=media_exterior/tot
          return render_template('media2.html', datos=media_exterior, media=media_local)
  else:
  	return render_template('media2.html', media=0, datos=0)

if __name__=='__main__':
  app.run(debug=True, host="0.0.0.0", port=8080)
