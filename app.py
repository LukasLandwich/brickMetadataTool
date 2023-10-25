from datetime import datetime
# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template
 
# Flask constructor takes the name of
# current module (__name__) as argument.

_now = datetime.utcnow()

app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates'
            )
 
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return render_template('content.html', now = _now)
 
# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)
    
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}