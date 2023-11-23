$.ajaxSetup({
  contentType: "application/json; charset=utf-8",
});


function get_properties_of(className, callback) {
    $.post( "/get_properties_of", JSON.stringify({ class: className }), callback);
}

function get_description_of(className, callback) {
  $.post( "/get_description_of", JSON.stringify({ class: className }), callback);
}

function createEntity(label, name, properties, callback) {
  $.post( "/createEntity", JSON.stringify({
      label: label,
      name: name,
      properties: properties
     }), callback);
}

function createPropertyBlueprint(label, name, properties, callback) {
  $.post( "/createPropertyBlueprint", JSON.stringify({
      label: label,
      name: name,
      properties: properties
     }), callback);
}


function getAllClasses() {
    $.get( "/get_all_classes", function( data ) {
        console.log(data);
      });
}

function getAllProperties() {
    $.get( "/get_all_properties", function( data ) {
        console.log(data);
      });
}

function getAllRelationships() {
    $.get( "/get_all_relationships", function( data ) {
        console.log(data);
      });
}

function getMetadataStatistics(callback) {
  $.get( "/get_metadata_statistics", callback);
}
