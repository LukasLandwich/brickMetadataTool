from flask import Flask, render_template, request, jsonify
from apiflask import APIFlask
from datetime import datetime
from neo4jConnector import Neo4JConnector
from brickAdapter import BrickAdapter
from metadataAdapter import MetadataAdapter
from resourceDictionary import ResourceDictionaty
from brickResource import *

# Flask constructor takes the name of
# current module (__name__) as argument.
app = APIFlask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates',
            spec_path='/spec'
            )
app.json.sort_keys = False
brick = None
brickDict = None

#The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
def main_page():
    return render_template('entityMaintainance.html')

@app.route('/relationship')
def relationship():
    return render_template('relationshipMaintainance.html')

@app.route('/dataStatistics')
def view_data():
    return render_template('dataStatistics.html')

classesList = []
#example context infusion   
@app.context_processor
def inject_now():
    return {'classes': classesList}

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

@app.route('/get_all_existing_entities', methods=["GET"])
def get_all_existing_entities():
    entities = metadata.getAllExistingEntities()
    return jsonify([e.serialize() for e in entities])

@app.route('/get_metadata_statistics', methods=["GET"])
def get_metadata_statistics():
    topNClasses = metadata.getTopNClasses(10)
    numberOfEntitites = metadata.getNumberOfEntities()
    numberOfRelationships = metadata.getNumberOfRelationships()
    
    response = jsonify({"topNClasses": topNClasses, "numberOfEntities": numberOfEntitites, "numberOfRelationships": numberOfRelationships})
    return response

@app.route('/get_possible_properties_of', methods=["POST"])
def get_possible_properties_of():
    data = request.get_json()
    _class= data.get('class')
    properties = brick.getPossiblePropertiesOf(_class)
    return jsonify([p.serialize() for p in properties])

@app.route('/get_possible_relationships_of', methods=["POST"])
def get_possible_relationships_of():
    
    data = request.get_json()
    byId = data.get('byId')
    
    if byId:
        id= data.get('id')
        _class = metadata.getClassOf(id).name
    else:
        _class= data.get('class')
        
    relationships = brick.getPossibleRelationshipsOf(_class)
    return jsonify([r.serialize() for r in relationships])


    

@app.route('/get_definition_of', methods=["POST"])
def get_definition_of():
    data = request.get_json()
    _class= data.get('class')
    
    resource = brickDict.getClass(_class)
    definition = resource.definition
    return jsonify({"definition": definition})

@app.route('/createEntity', methods=["POST"])
def createEntity():
    data = request.get_json()
    
    label= data.get('label')
    name = data.get('name')
    properties = data.get('properties')

    classInstance = BrickClassInstance(brickDict.getClass(label), name, [BrickPropertyInstance(brickDict.getProperty(p['label']), p['value']) for p in properties])
    
    response = metadata.createNode(classInstance)
    if response: 
        return "Success", 200, {"Access-Control-Allow-Origin": "*"}
    else:
        return "Internal Server Error", 500

@app.route('/createRelationship', methods=["POST"])
def createRelationship():
    data = request.get_json()
    fromId = data.get('fromId')
    toId = data.get('toId')
    relType = data.get('relType')
    fromInstance = metadata.getEntityById(fromId)
    toInstance = metadata.getEntityById(toId)
    relationship = BrickRelationshipInstance(brickDict.getReslationship(relType),fromInstance, toInstance)
    response = metadata.createRelationshipOnExisingNodes(relationship, fromInstance, toInstance)
    
    if response: 
        return "Success", 200, {"Access-Control-Allow-Origin": "*"}
    else:
        return "Internal Server Error", 500


@app.route('/createPropertyBlueprint', methods=["POST"])
def createPropertyBlueprint():
    data = request.get_json()
    label= data.get('label')
    name = data.get('name')
    properties = data.get('properties')
    classInstance = BrickClassInstance(brickDict.getClass(label), name, [BrickPropertyInstance(brickDict.getProperty(p['label']), p['value']) for p in properties])
    
    response = metadata.createNode(classInstance, True)
    if response: 
        return "Success", 200, {"Access-Control-Allow-Origin": "*"}
    else:
        return "Internal Server Error", 500


@app.route('/get_possible_Blueprints', methods=["POST"])
def get_possible_Blueprints():
    data = request.get_json()
    className = data.get('class')
   
    blueprints = metadata.getBlueprintsOf(className)
    return jsonify([r.serialize() for r in blueprints])

@app.route('/get_blueprint_by_id', methods=["POST"])
def get_blueprint_by_id():
    data = request.get_json()
    _id = data.get('id')
   
    blueprint = metadata.getBlueprintById(_id)
    return jsonify(blueprint.serialize())
# main driver function
if __name__ == '__main__':
    #Open Neo4J DB connection.
    #Credentials are fixed for development reasosn
    db = Neo4JConnector("neo4j://localhost:7687", "neo4j", "admin1234")
    # run() method of Flask class runs the application
    # on the local development server.
    
    brick = BrickAdapter(db)
    brickDict = ResourceDictionaty(brick)
    metadata = MetadataAdapter(db, brickDict)
    classesList = [x for x in brickDict.classes.values()]

    metadata.getAllExistingEntities()

    app.run(debug=True)
    
    brick.db.driver.close()   