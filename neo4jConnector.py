from neo4j import GraphDatabase
import brickschema

class Neo4JConnector:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def print_greeting(self, message):
        with self.driver.session() as session:
            greeting = session.execute_write(self._create_and_return_greeting, message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]
'''
class BrickAdapter:
    # creates a new rdflib.Graph with a recent version of the Brick ontology
    # preloaded.
    g = brickschema.Graph(load_brick=True, store='neo4j-n10s')
    # OR use the absolute latest Brick:
    # g = brickschema.Graph(load_brick_nightly=True)
    # OR create from an existing model
    # g = brickschema.Graph(load_brick=True).from_haystack(...)

    # load in data files from your file system
    #g.load_file("mbuilding.ttl")
    # ...or by URL (using rdflib)
    g.parse("https://brickschema.org/ttl/soda_brick.ttl", format="ttl")

    # perform reasoning on the graph (edits in-place)
    #g.expand(profile="owlrl")
    #g.expand(profile="shacl") # infers Brick classes from Brick tags

    # validate your Brick graph against built-in shapes (or add your own)
    #valid, _, resultsText = g.validate()
    #if not valid:
        #print("Graph is not valid!")
        #print(resultsText)

    # perform SPARQL queries on the graph
    res = g.query("""SELECT ?afs ?afsp ?vav WHERE  {
        ?afs    a       brick:Air_Flow_Sensor .
        ?afsp   a       brick:Air_Flow_Setpoint .
        ?afs    brick:isPointOf ?vav .
        ?afsp   brick:isPointOf ?vav .
        ?vav    a   brick:VAV
    }""")
    for row in res:
        print(row)

    # start a blocking web server with an interface for performing
    # reasoning + querying functions
    #g.serve("localhost:8080")
    # now visit in http://localhost:8080
'''