from flask import Flask, render_template, request
from datetime import datetime
from neo4jConnector import Neo4JConnector
from services import exampleService
from brickResource import BrickResource, BrickClass, BrickProperty, BrickRelationship

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

classesList = []
#example context infusion   
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow(), 'classes': classesList}

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
    
    print(db.hasBrickInitialized())
    if not db.hasBrickInitialized():
        print("Brick Onntology isnt initilaized.")
        
        db.loadBrickOntology()
    
    classes, summary, keys = db.driver.execute_query(
    "MATCH (a:n4sch__Class) RETURN a.n4sch__name as name, a.n4sch__label as label, a.n4sch__defintion as defintion, a.uri as uri",
    database_="neo4j",
    )   
    classesList = []
    for resource in classes:
        classesList.append(BrickClass(resource["name"], resource["label"], resource["defintion"], resource["uri"]))
    
    properties, summary, keys = db.driver.execute_query(
    "MATCH (a:n4sch__Property) RETURN a.n4sch__name as name, a.n4sch__label as label, a.n4sch__defintion as defintion, a.uri as uri",
    database_="neo4j",
    )   
    propertiesList = []
    for resource in properties:
        propertiesList.append(BrickProperty(resource["name"], resource["label"], resource["defintion"], resource["uri"]))

    relationships, summary, keys = db.driver.execute_query(
    "MATCH (a:n4sch__Relationship) RETURN a.n4sch__name as name, a.n4sch__label as label, a.n4sch__defintion as defintion, a.uri as uri",
    database_="neo4j",
    )   
    relationshipsList = []
    for resource in relationships:
        relationshipsList.append(BrickRelationship(resource["name"], resource["label"], resource["defintion"], resource["uri"]))
    
        
    app.run(debug=True)
    
    db.driver.close()
    
    
    