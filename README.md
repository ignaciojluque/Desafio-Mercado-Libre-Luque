# Desafío Mercado Libre, Ignacio Luque

En este trabajo se creó una API que puede realizar 2 funciones:
* Buscar una palabra en un documento de Google Drive
* Crear un documento de Google Drive 

Para ello se utiliza la api de Google drive. Para poder hacer uso de la misma se utiliza credenciales de desarrollador,  razón por la cual existen los archivos "client_id.json" "credentials.json".



## Requisitos previos

* Tener python 2.7 o python 3
* Tener una cuenta de Google Drive activa
* Descargar pip: `sudo apt-get install python-pip` 
* Descargar Flask: `sudo pip install Flask`
* Descargar google-api-python-client: `pip install --upgrade google-api-python-client`


## Buscar una palabra en un documento de Gdrive

Para poder ejecutar esta función primero necesitamos descargar todos los archivos y descomprimirlos en una carpeta. Luego ejecutamos en un terminal la siguiente línea (posicionados en la carpeta donde descomprimimos los archivos):

`FLASK_APP=desafioML.py flask run`

Entonces habremos levantado un servidor en localhost:5000 .
Luego abrimos cualquier navegador web y escribimos la siguiente linea, reemplazando según corresponda:

`http://localhost:5000/search-in-doc/<ID>?word=<PALABRA_A_BUSCAR>`

En caso de no encontrar la palabra se recibirá "HTTP/1.1 404 Not Found" en caso satisfactorio se recibirá "HTTP/1.1 200 Ok"

Nota: en caso de no saber cual es el ID del documento deseado, se imprime por terminal el nombre de cada archivo y abajo su ID asociado.
##  Crear un documento de GDrive
Para poder ejecutar esta función primero necesitamos descargar todos los archivos y descomprimirlos en una carpeta. Luego ejecutamos en un terminal la siguiente línea (posicionados en la carpeta donde descomprimimos los archivos):

`FLASK_APP=desafioML.py flask run`

Luego se deberá mandar a la siguiente URL:

`http://localhost:5000/crear/`

un archivo .json que tenga este formato(a través de una petición HTTP POST):

`{“titulo”:”mi_titulo”, “descripcion”:”mi_descripcion”}` 

Las posibles respuestas serán:
* "HTTP/1.1 400" , en caso de haber un error en el archivo .json o en el formato de los parámetros.
* "HTTP/1.1 500" , en caso de no poder crear el archivo en Google Drive.
* "HTTP/1.1 200 OK" , si todo funciono satisfactoriamente.


