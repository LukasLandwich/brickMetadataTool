function hello() {
    console.log("Hello Luki")
}

$( "#target" ).on( "click", function() {
    alert( "Handler for `click` called." );
  } );

$('#entityTypeSelect').on("change", function() {
    console.log($(this).val())
    get_properties_of($(this).val())
});