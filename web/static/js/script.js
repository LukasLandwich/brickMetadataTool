$('#entityTypeSelect').on("change", function() {
    data = get_properties_of($(this).val(), updatePropertieForm)
    
});

$('#addEntitySubmit').on("click", function() {
    
    label = $('#entityTypeSelect').val()
    _name = $('#entityName').val()
    properties = []
    $.each($('input[id^="propertyInput_"]'), function(index, element) {
        properties.push({label: $(element).attr('propertyName'), value: $(element).val()})
    })
    createEntity(label, _name, properties, function(){})
});

$('#addEntityCancle').on("click", function() {
    
    console.log("Cancle")   
});

function updatePropertieForm(data) {
    length = Object.keys(data).length;
    var el = $("#propertyForm_textInputs");
    el.empty(); 
    if (length > 0) {
        $('#propertyForm').removeClass("d-none");

        $.each(data, function(key,value) {
            buildPropertyInput(value['name'], el)
        });
    }
    else {
        $('#propertyForm').addClass("d-none");
    }
}


function buildPropertyInput(propertyName, el) {

    var lable = $('<lable>', {
        for: 'propertyInput_' + propertyName,
        text: propertyName
    })
    var input = $('<input>', {
        type:'text',
        class: 'form-control',
        id: 'propertyInput_' + propertyName,
        propertyName: propertyName,
        placeholder: 'Insert Property Value'
    })
    
    var div = $('<div>', {
        class: 'col-auto',
    })

    div.append(lable)
    div.append(input)
    div.appendTo(el)
}

