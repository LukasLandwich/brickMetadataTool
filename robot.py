from py4j.java_gateway import launch_gateway, JavaGateway

launch_gateway(jarpath='robot.jar',
               classpath='org.obolibrary.robot.PythonOperation',
               port=25333,
               die_on_exit=True)


gateway = JavaGateway()

io_helper = gateway.jvm.org.obolibrary.robot.IOHelper()

ont = io_helper.loadOntology('docs/examples/annotated.owl')

print(ont.getOntologyID().getVersionIRI())