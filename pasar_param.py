from flask import Flask
app = Flask(__name__)
 
if __name__ == '__main__':
    app.run()


@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'






@app.route('/search-in-doc/<palabra>/<ident>',methods=['GET'])
def search(palabra,ident):
    return 'Hola ' + palabra + ident +'!!!'
