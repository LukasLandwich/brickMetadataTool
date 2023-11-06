$('#entityTypeSelect').on("change", function() {
    className = $(this).val()
    data = get_properties_of(className, updatePropertieForm)
    get_description_of(className, updateEntityDescription)
    
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
            buildPropertyInput(value['name'], value['definition'], el)
        });
    }
    else {
        $('#propertyForm').addClass("d-none");
    }
}


function buildPropertyInput(propertyName, definition, el) {

    var lable = $('<lable>', {
        for: 'propertyInput_' + propertyName,
        text: propertyName
    })
    var input = $('<input>', {
        type:'text',
        class: 'form-control',
        id: 'propertyInput_' + propertyName,
        propertyName: propertyName,
        placeholder: 'Insert Property Value',
        "data-toggle":"tooltip",
        "data-placement":"top",
        title: definition,
    })
    
    var div = $('<div>', {
        class: 'col-auto',
    })

    div.append(lable)
    div.append(input)
    div.appendTo(el)
}

function updateStatistics() {
    getMetadataStatistics(updateStatisticsCallback)
}

function updateStatisticsCallback(data) {
    $("#numberOfEntities").text((data["numberOfEntities"]))
    $("#numberOfRelationships").text(data["numberOfRelationships"])
    var topN = ""
    for (key in data["topNClasses"]){
        console.log(key)
        console.log(data["topNClasses"][key])
        topN += key + data["topNClasses"][key]    
    }
    $("#topEntities").text(topN)

}

function updateEntityDescription(data) {
    $("#entityDescription").attr("title", data["description"])
}

$("#test").on("click", function() {
    updateStatistics()
})

