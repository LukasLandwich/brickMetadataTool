$.ajaxSetup({
  contentType: "application/json; charset=utf-8",
});


function get_possible_properties_of(className, callback) {
    $.post( "/get_possible_properties_of", JSON.stringify({ class: className }), callback);
}

function get_possible_relationships_byClass(className, callback) {
  $.post( "/get_possible_relationships_of", JSON.stringify({ class: className, byId: false }), callback);
}

function get_possible_relationships_byId(id, callback) {
  $.post( "/get_possible_relationships_of", JSON.stringify({ id: id, byId: true }), callback);
}

function get_definition_of(className, callback) {
  $.post( "/get_definition_of", JSON.stringify({ class: className }), callback);
}

function get_all_existing_entities(callback) {
  $.get( "/get_all_existing_entities", callback);
}

function get_all_shapes(callback) {
  $.get( "/get_all_shapes", callback);
}

function createEntity(entityValues, callback) {
  $.post( "/create_entity", JSON.stringify(entityValues), callback);
}

function createRelationship(fromId, toId, relType, callback) {
  $.post( "/create_relationship", JSON.stringify({
    fromId: fromId,
    toId: toId,
    relType: relType
   }), callback);
}


function createPropertyBlueprint(entityValues, callback) {
  $.post( "/get_possible_blueprints", JSON.stringify(entityValues), callback);
}

function getPossibleBlueprints(className, callback) {
  $.post( "/get_possible_Blueprints", JSON.stringify({ class: className }), callback);
}

function getBlueprintById(_id, callback) {
  $.post( "/get_blueprint_by_id", JSON.stringify({ id: _id }), callback);
}

function getMetadataStatistics(callback) {
  $.get( "/get_metadata_statistics", callback);
}
