$.ajaxSetup({
  contentType: "application/json; charset=utf-8"
});


function get_properties_of(className) {
    $.post( "/get_properties_of", JSON.stringify({ class: className }), function( data ) {
        console.log(data);
      });
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
