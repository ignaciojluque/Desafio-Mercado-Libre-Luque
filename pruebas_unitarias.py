# pruebas Unitarias
import requests
import json

def prueba_buscar_palabra_satisfactoria():
	payload = {'word': 'que'}
	url = "http://localhost:5000/search-in-doc/0Bx7JL8bKYdpgYzhRZnlFTERZcW8/"# probe con un id correspondiente a uno de mis archivos en google drive, para probar poner un id valido de la cuenta de gdrive usada
	r = requests.get(url, params=payload)
	return r
def prueba_buscar_palabra_error():
	payload = {'word': 'que'}
	url = "http://localhost:5000/search-in-doc/1234/"#paso mal el id
	r = requests.get(url, params=payload)
	return r

def prueba_crear_doc_satisfactioria():
	url = "http://localhost:5000/crear-doc/"
	data = {'titulo': 'titulo de prueba', 'descripcion': 'alguna descripcion'}
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	r = requests.post(url, data=json.dumps(data), headers=headers)
	return r
def prueba_crear_doc_con_parametros_mal():
	url = "http://localhost:5000/crear-doc/"
	data = {'landf': 'titulo de prueba', 'lsdn': 'alguna descripcion'}
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	r = requests.post(url, data=json.dumps(data), headers=headers)
	return r


if __name__ == "__main__":

## METODO BUSCAR PALABRA
	print("PRUEBAS UNITARIAS BUSCAR PALABRA \n")
	rta_buscar_palabra_satis = prueba_buscar_palabra_satisfactoria()
	rta_buscar_palabra_error = prueba_buscar_palabra_error()
	if rta_buscar_palabra_satis.text == "HTTP/1.1 200 OK":
		print "Al buscar una palabra que esta en un documento, la encuentra"
	else :
		print "Al buscar una palabra que esta en un documento, NO la encuentra, ERROR"
	if rta_buscar_palabra_error.text == "HTTP/1.1 404 Not Found":
		print "Al buscar una palabra con un id inexistente, no la encuentra"
	else :
		print "Al buscar una palabra con un id inexistente, la encuentra: ERROR"
## METODO CREAR DOCUMENTO
	print("\n")
	print("PRUEBAS UNITARIAS CREAR DOC \n")
	rta_crear_doc = prueba_crear_doc_satisfactioria()
	rta_param_mal = prueba_crear_doc_con_parametros_mal()
	if (str(rta_crear_doc)) == "<Response [200]>":# como no se que id es la del archivo que creo, corroboro que funcione de esta manera 
		print "Al pasar bien los parametros en un archivo .json valido el archivo se crea"
	else :
		print "Al pasar bien los parametros en un archivo .json valido el archivo se crea: ERROR"
	if rta_param_mal.text == "HTTP/1.1 400":
		print "Al pasar mal los parametros devuelve 400"
	else :
		print "Al pasar mal los parametros NO devuelve 400: ERROR"


