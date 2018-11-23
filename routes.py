from flask import Flask, render_template

app= Flask(__name__)

@app.route('/')
def inicio():
  return render_template('inicio.html')

@app.route('/umbral')
def umbral():
  return render_template('umbral.html')

@app.route('/media')
def media():
  return render_template('media.html')

if __name__=='__main__':
  app.run(debug=True, host="0.0.0.0", port=8080)
