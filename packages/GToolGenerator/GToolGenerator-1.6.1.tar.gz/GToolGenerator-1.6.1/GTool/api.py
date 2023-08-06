# Flask Libraries
from flask import Flask, request, send_file
from markupsafe import escape # para pintar en html.

from generate_target import github # Nuestro módulo.
import os



# App.
app = Flask(__name__) # Nombre de la app = nombre del archivo.
app.config.from_pyfile('config_api.py') # Configuramos la app por medio de un archivo python.




@app.route('/generate/github/<string:github_user>/<string:color>') # Comando #1
def github_generator(github_user, color): # Recibe 2 valores.
    gen = github(github_user) # Generamos la imagen!

    if os.path.exists(gen):
        return send_file(gen) # Devolvemos la imagen.

    else:
        return gen # Devolvemos el error.


    
app.run(port = '5000')