##
# Flask Drive Example App
#
# @author Prahlad Yeri <prahladyeri@yahoo.com>
# @date 30-12-2016
# Dependency:
# 1. pip install flask google-api-python-client
# 2. make sure you have client_id.json in this same directory.

import os
import flask
import httplib2
from apiclient import discovery
from apiclient.http import MediaIoBaseDownload, MediaFileUpload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

app = flask.Flask(__name__)

@app.route('/search-in-doc/<palabra>/<ident>',methods=['GET'])
def index(palabra,ident):
    credentials = get_credentials()
    if credentials == False:
		return flask.redirect(flask.url_for('oauth2callback'))
    elif credentials.access_token_expired:
		return flask.redirect(flask.url_for('oauth2callback'))
    else:
		print('now calling fetch')
		all_files = fetch( "fullText contains '%s'"% palabra, sort='modifiedTime desc')
		#s = ""
		for file in all_files:
			ide = file['id']
			if ident == ide:
				return "HTTP/1.1 200 OK"
		return "HTTP/1.1 404 Not Found"

@app.route('/oauth2callback')
def oauth2callback():
	flow = client.flow_from_clientsecrets('client_id.json',
			scope='https://www.googleapis.com/auth/drive',
			redirect_uri=flask.url_for('oauth2callback', _external=True)) # access drive api using developer credentials
	flow.params['include_granted_scopes'] = 'true'
	if 'code' not in flask.request.args:
		auth_uri = flow.step1_get_authorize_url()
		return flask.redirect(auth_uri)
	else:
		auth_code = flask.request.args.get('code')
		credentials = flow.step2_exchange(auth_code)
		open('credentials.json','w').write(credentials.to_json()) # write access token to credentials.json locally 
		return flask.redirect(flask.url_for('index'))

def get_credentials():
	credential_path = 'credentials.json'

	store = Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		print("Credentials not found.")
		return False
	else:
		print("Credentials fetched successfully.")
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
		print('Client secrets file (client_id.json) not found in the app path.')
		exit()
	import uuid
	app.secret_key = str(uuid.uuid4())
	app.run(debug=True)
