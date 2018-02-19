## Desafio Mercado Libre , Ignacio Luque

import json
import os
import flask
from flask import request, jsonify
import httplib2
from apiclient import discovery
from apiclient.http import MediaIoBaseDownload, MediaFileUpload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

app = flask.Flask(__name__)

@app.route('/search-in-doc/<ident>/',methods=['GET']) 
def index(ident):# funcion que busca una palabra en en el documento indicado(ambos pasados por parametro)
    credentials = get_credentials() #se obtienen credenciales para usar apis de google
    if credentials == False:
		return flask.redirect(flask.url_for('oauth2callback'))# se debe ingresar en la cuenta de google drive
    elif credentials.access_token_expired:
		return flask.redirect(flask.url_for('oauth2callback'))# expiro la sesion y se debe ingresar nuevamente
    else:
		palabra=request.args.get('word')
		if palabra is None:
			return "Falta pasar palabra como parametro, por favor agregue: ?word=palabra_deseada" # no se paso palabra por parametro 			
		all_files = fetch( "fullText contains '%s'"% palabra, sort='modifiedTime desc')# se buscan todos los archivos que contengan la palabra pasada por parametro
		for file in all_files:
			ide = file['id']
			print(file['name']) 
			print(file['id'])# se imprimen por consola las id de los documentos para conocerlas (solo para el caso en que no se conozca la id previamente)
			if ident == ide: # nos quedamos con el documento que tenga la ID pasada por parametro
				return "HTTP/1.1 200 OK"
		return "HTTP/1.1 404 Not Found" # si llego hasta aca es porque no se encontro el documento

@app.route('/crear-doc/', methods=['GET', 'POST'])
def crear_doc():
	file_metadata = request.get_json()	
	titulo = file_metadata.get("titulo")
	descripcion = file_metadata.get("descripcion")
	
	if file_metadata is None or titulo is None or descripcion is None:# si no se recibio el archivo json o los parametros titulo y descripcion son nulos , entonces devuelve error 400
		return "HTTP/1.1 400"
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('drive', 'v3', http=http)
	file = service.files().create(body=file_metadata, # se crea el documento con los datos pasados por parametro
                                    fields='id').execute()
	
	if file is None:
		return "HTTP/1.1 500" 
	
	return "HTTP/1.1 200 OK" + " id: %s propiedades: " % file.get('id') +  str(file_metadata)

@app.route('/oauth2callback')
def oauth2callback():
	flow = client.flow_from_clientsecrets('client_id.json',
			scope='https://www.googleapis.com/auth/drive',
			redirect_uri=flask.url_for('oauth2callback', _external=True)) # se accede a drive usando las credenciales de desarrollador
	flow.params['include_granted_scopes'] = 'true'
	if 'code' not in flask.request.args:
		auth_uri = flow.step1_get_authorize_url()
		return flask.redirect(auth_uri)
	else:
		auth_code = flask.request.args.get('code')
		credentials = flow.step2_exchange(auth_code)
		open('credentials.json','w').write(credentials.to_json())  
		return flask.redirect(flask.url_for('index'))

def get_credentials():
	credential_path = 'credentials.json'

	store = Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		print("Credentials no encontradas.")
		return False
	else:
		print("credenciales encontradas con exito.")
		return credentials

def fetch(query, sort='modifiedTime desc'):
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('drive', 'v3', http=http)
	results = service.files().list(
		q=query,orderBy=sort,fields="nextPageToken, files(id, name)").execute()
	items = results.get('files', [])
	return items
	
if __name__ == '__main__':
	if os.path.exists('client_id.json') == False:
		print('archivo secreto del cliente (client_id.json) no encontrado.')
		exit()
	import uuid
	app.secret_key = str(uuid.uuid4())
	app.run(debug=True)
