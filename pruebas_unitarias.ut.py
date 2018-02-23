import unittest
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

class TestAPI(unittest.TestCase):
	def setUp(self):
		self.rta1 = prueba_buscar_palabra_satisfactoria()
		self.rta2 = prueba_buscar_palabra_error()
		self.rta3 = prueba_crear_doc_satisfactioria()
		self.rta4 = prueba_crear_doc_con_parametros_mal()

	def test_1(self):
		self.assertEqual(self.rta1.status_code, 200)
	def test_2(self):
		self.assertEqual(self.rta2.status_code, 404)
	def test_3(self):
		self.assertEqual(self.rta3.status_code, 200)
	def test_4(self):
		self.assertEqual(self.rta4.status_code, 400)
 
if __name__ == '__main__':
    unittest.main()
