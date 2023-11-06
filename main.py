from flask import Flask, render_template, request, jsonify
from datetime import datetime
from neo4jConnector import Neo4JConnector
from brickadapter import BrickAdapter
from brickResource import BrickClassInstance, BrickPropertyInstance, BrickProperty
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

@app.route('/get_metadata_statistics', methods=["GET"])
def get_metadata_statistics():
    topNClasses = brick.getTopNClasses(3)
    numberOfEntitites = brick.getNumberOfEntities()
    numberOfRelationships = brick.getNumberOfRelationships()
    
    response = jsonify({"topNClasses": topNClasses, "numberOfEntities": numberOfEntitites, "numberOfRelationships": numberOfRelationships})
    print(response)
    return response

@app.route('/get_properties_of', methods=["POST"])
def get_properties_of():
    data = request.get_json()
    _class= data.get('class')
    properties = brick.getPropertiesOf(_class)
    return jsonify([p.serialize() for p in properties])

@app.route('/get_description_of', methods=["POST"])
def get_description_of():
    data = request.get_json()
    _class= data.get('class')
    description = brick.getDescriptionOf(_class)
    return jsonify({"description": description})

@app.route('/createEntity', methods=["POST"])
def createEntity():
    data = request.get_json()
    label= data.get('label')
    name = data.get('name')
    properties = data.get('properties')
    
    response = brick.createNode(name, label, properties)
    print(response)
    return "Success", 200, {"Access-Control-Allow-Origin": "*"}
    

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
    
    #brickClass = brick.getClassResource("Building")
    #brickClassInstance = BrickClassInstance(brickClass, name="BuildingTest", properties=[BrickPropertyInstance(BrickProperty(name="yearBuilt", label="yearBuilt", definition="Test", uri=""), 1996)])
    #brick.createNode(brickClassInstance)
    
    app.run(debug=True)
    
    db.driver.close()
    
    
    