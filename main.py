from flask import Flask, render_template, request
from datetime import datetime
from neo4jConnector import Neo4JConnector
from services import exampleService

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates'
            )

_now = datetime.utcnow()
db = None

#The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
def main_page():
    return render_template('content.html', now = _now)


#example context infusion   
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

#example GET    
@app.route('/get_handle', methods=["GET"])
def button():
    print("Im here")
    return ('', 204)

#exampe POST
@app.route('/get_handle_post', methods=["POST"])
def button_post():
    username = request.form['username']
    print(username)
    db.print_greeting("hello, world")
    return ('', 204)

@app.before_request
def before():
    print("This is executed BEFORE each request.")


# main driver function
if __name__ == '__main__':
    #Open Neo4J DB connection.
    #Credentials are fixed for development reasosn
    db = Neo4JConnector("neo4j://localhost:7687", "neo4j", "admin1234")
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)