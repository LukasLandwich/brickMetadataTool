var propertySave_dontAskAgain = false

jQuery(updateStatistics)

$('#propertySaveButton').on("click", togglePropertySaveModal)
$('#propertySave_cancelButton').on("click", cancelPropertySaveModal)
$('#propertySave_saveButton').on("click", savePropertySaveModal)
$('#propertySettignsDropdownButton').on("click", function() {$('#propertySettignsDropdown').toggle()})


$('#entityTypeSelect').on("change", function() {
    className = $(this).val()
    data = get_possible_properties_of(className, updatePropertieForm)
    get_definition_of(className, updateEntityDescription)
    
});

$('#addEntitySubmit').on("click", function() {
    
    togglePropertySaveModal()

    label = $('#entityTypeSelect').val()
    _name = $('#entityName').val()
    properties = []
    $.each($('input[id^="propertyInput_"]'), function(index, element) {
        properties.push({label: $(element).attr('propertyName'), value: $(element).val()})
    })
    
    createEntity(label, _name, properties,  updateStatistics)
    
});

$('#addEntityCancle').on("click", function() {   
    console.log("Cancle")   
});

function togglePropertySaveModal() {
    if (!propertySave_dontAskAgain) {
        $('#propertySaveModal').modal('show'); 
    }
    else {
        clearEntityAndPropertyInputs()
    }
}

function cancelPropertySaveModal(){
    if($('#propertieSave_dontAskAgain').is(':checked')) {
        propertySave_dontAskAgain = true
    }
    $('#propertySaveModal').modal('hide');
}

function savePropertySaveModal() {
    label = $('#entityTypeSelect').val()
    _name = $('#propertyBlueprintName').val()
    properties = []
    $.each($('input[id^="propertyInput_"]'), function(index, element) {
        properties.push({label: $(element).attr('propertyName'), value: $(element).val()})
    })
    createPropertyBlueprint(label, _name, properties, function(){})
    $('#propertySaveModal').modal('hide');
    clearEntityAndPropertyInputs()
}

function clearEntityAndPropertyInputs() {
    $('#entityName').val("")
    $.each($('input[id^="propertyInput_"]'), function(index, element) {
        $(element).val("")
    })
}

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

