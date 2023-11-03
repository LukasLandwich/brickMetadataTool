from flask import Flask, render_template, request, jsonify
from datetime import datetime
from neo4jConnector import Neo4JConnector
from brickadapter import BrickAdapter
from services import exampleService

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates'
            )

db = None
brick = None
_now = datetime.utcnow()
#The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
def main_page():
    return render_template('content.html', now = _now)

classesList = []
#example context infusion   
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow(), 'classes': classesList}

@app.route('/get_all_classes', methods=["GET"])
def get_all_classes():
    classes = brick.getAllClasses()
    return jsonify([c.serialize() for c in classes])

@app.route('/get_all_properties', methods=["GET"])
def get_all_properties():
    properties = brick.getAllProperties()
    return jsonify([p.serialize() for p in properties])

@app.route('/get_all_relationships', methods=["GET"])
def get_all_relationships():
    relationships = brick.getAllRelationships()
    return jsonify([r.serialize() for r in relationships])

@app.route('/get_properties_of', methods=["POST"])
def get_properties_of():
    data = request.get_json()
    _class= data.get('class')
    properties = brick.getPropertiesOf(_class)
    return jsonify([p.serialize() for p in properties])

#exampe POST
@app.route('/get_handle_post', methods=["POST"])
def button_post():
    username = request.form['username']
    print(username)
    db.print_greeting("hello, world")
    return {'now': datetime.utcnow(), 'classes': classesList}

@app.before_request
def before():
    pass



# main driver function
if __name__ == '__main__':
    #Open Neo4J DB connection.
    #Credentials are fixed for development reasosn
    db = Neo4JConnector("neo4j://localhost:7687", "neo4j", "admin1234")
    # run() method of Flask class runs the application
    # on the local development server.
    
    brick = BrickAdapter(db)
    classesList = brick.getAllClasses()
    app.run(debug=True)
    
    db.driver.close()
    
    
    