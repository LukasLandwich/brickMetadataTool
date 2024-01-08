addAnotherEntity = false

function savePropertySaveModal() {
    entityValues = collectEntityValues()
    //TODO Need for callback??
    createPropertyBlueprint(entityValues, function(){})
    $('#propertySaveModal').modal('hide');
    clearEntityAndPropertyInputs()
}

function entitySumbmitClick() {
    
    entityValues = collectEntityValues()
    if (entityValues["label"] == "") {
        showAlertMessage("No entity type selected!", "entityAlert")
    }
    else if (entityValues["name"] == "") {
        showAlertMessage("No entity name spefified!", "entityAlert")
    }
    else {
        createEntity(entityValues, updateStatistics)
        clearEntityAndPropertyInputs()
        showAlertMessage("Entity sucessfully created: " + entityValues["name"], "entitySuccess")
    }
}

function clearEntityAndPropertyInputs() {
    if (!addAnotherEntity) {
        $('#entityName').val("")
        $('#propertyBlueprintName').val("")
        $.each($('input[id^="propertyInput_"]'), function(index, element) {
            $(element).val("")
        })
    }
}

function clearRelationshipForm() {
    selectFrom = $('#relationshipEntityFromSelect')
    selectType = $('#relationshipTypeSelect')
    selectTo = $('#relationshipEntityToSelect')
    $(selectFrom).val("")
    $(selectTo).val("")
    $(selectType).empty()
    buildSelectOption("Select Entity","", selectType)
}

function collectEntityValues(blueprint = false ) {
    properties = []
    $.each($('input[id^="propertyInput_"]'), function(index, element) {
        properties.push({label: $(element).attr('propertyName'), value: $(element).val()})
    })
    return {
        label: $('#entityTypeSelect').val(),
        name: blueprint ? $('#propertyBlueprintName').val() : $('#entityName').val(),
        properties: properties,
    };
}

function entityTypeSelectChange() {
    className = $(this).val()
    get_possible_properties_of(className, updatePropertieForm)
    get_definition_of(className, updateEntityDescription)
    getPossibleBlueprints(className, updateBlueprintSelection)
}

function addAnotherEntityCheckChange() {
    addAnotherEntity = $('#addAnotherEntityCheck').is(':checked')
}


function updatePropertieForm(data) {
    console.log(data)
    length = Object.keys(data).length;
    var el = $("#propertyForm_textInputs");
    el.empty(); 
    if (length > 0) {
        $('#propertyForm_textInputs').removeClass("d-none");

        $.each(data, function(key,value) {
            buildPropertyInput(value[0]['name'], value[0]['definition'], el)
        });
    }
    else {
        $('#propertyForm_textInputs').addClass("d-none");
    }
}

function updateBlueprintSelection(data) {
    length = Object.keys(data).length;
    var el = $("#propertyForm_availableBlueprintsSelect");
    el.empty(); 
    if (length > 0) {
        $('#propertyForm_availableBlueprints').removeClass("d-none");
        buildSelectOption("SelectBlueprint", "", el)
        $.each(data, function(key,value) {
            buildSelectOption(value['name'], value['id'], el)
        });
    }
    else {
        buildSelectOption("No Blueprint Available", "", el)
    }
}

function onAvailableBlueprintsSelectChange() {
    blueprintId = $(this).val()
    if (blueprintId != "") {
        getBlueprintById(blueprintId, updatePropteryForm)
    }
    else {
        clearEntityAndPropertyInputs()
    }
}

function updatePropteryForm(data) {
    
    $.each(data["properties"], function(key,value) {
        inputName = "#propertyInput_" + key
        $(inputName).val(value)
        console.log(value)
        console.log(inputName)
    });
   
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


function updateRelationshipTypeSelect(data) {
    length = Object.keys(data).length;
    var el = $("#relationshipTypeSelect");
    el.empty(); 
    if (length > 0) {
        buildSelectOption("Select Relationship Type", "", el)
        $.each(data, function(key,value) {
            buildSelectOption(value['label'], value['name'], el)
        });
    }
    else {
        buildSelectOption("There are no Possible Relationship Types", "", el)
    }
}

function updateRelationshipEntitySelect(data) {
    length = Object.keys(data).length;
    var el1 = $("#relationshipEntityFromSelect");
    el1.empty(); 
    var el2 = $("#relationshipEntityToSelect");
    el2.empty(); 
    if (length > 0) {
        buildSelectOption("Select Entity", "", el1)
        buildSelectOption("Select Entity", "", el2)
        $.each(data, function(key,value) {
            buildSelectOption(value['name'], value['id'], el1)
            buildSelectOption(value['name'], value['id'], el2)
        });
    }
    else {
        buildSelectOption("There are no Existing Entities", "", el1)
        buildSelectOption("There are no Existing Entities", "", el2)
    }
}

function buildSelectOption(text, value, el) {
    var option = $('<option>', {
        value: value,
        text: text,
    })
    el.append(option)
}

function onRelationshipEntityFromSelectChange() {
    value = $("#relationshipEntityFromSelect").val()
    get_possible_relationships_byId(value, updateRelationshipTypeSelect)
}

function changeEntityCreationMode() {
    
    on = $('#switch_existingEntities').is(':checked')
    //On Existing Entities
    if(on) {
        get_all_existing_entities(updateRelationshipEntitySelect)
        $('.entityCreationmode_Existing').each(function(i, obj) {
            $(obj).removeClass("d-none")
        });

        $('.entityCreationmode_New').each(function(i, obj) {
            $(obj).addClass("d-none")
        });        
    }
    //On New Entities
    else {
        $('.entityCreationmode_New').each(function(i, obj) {
            $(obj).removeClass("d-none")
        });

        $('.entityCreationmode_Exiting').each(function(i, obj) {
            $(obj).addClass("d-none")
        });
    }
}

function submitRelationshipOnExisiting() {
    fromId = $('#relationshipEntityFromSelect').val()
    toId = $('#relationshipEntityToSelect').val()
    relType = $('#relationshipTypeSelect').val()
    if (fromId == "") {
        showAlertMessage("No entity selected.", "relationshipAlert")
    }
    else if (relType == "") {
        showAlertMessage("No relationship type selected.", "relationshipAlert")
    }
    else if (toId == "") {
        showAlertMessage("Second entity not selected.", "relationshipAlert")
    }
    else {
        createRelationship(fromId, toId, relType)
        clearRelationshipForm()
        showAlertMessage(relType + " relationship from " + fromId + " to " + toId + " created.", "relationshipSuccess")
    }
}

function updateStatistics() {
    getMetadataStatistics(updateStatisticsCallback)
}

function updateStatisticsCallback(data) {
    $("#numberOfEntities").text((data["numberOfEntities"]))
    $("#numberOfRelationships").text(data["numberOfRelationships"])
    $('#topEntitiesTableBody').empty()
    for (key in data["topNClasses"]){
        className = key
        description = data["topNClasses"][key]["description"]
        count = data["topNClasses"][key]["count"]
        row = createEntityTableEntry(className, description, count)
        $('#topEntitiesTableBody').append(row)
    }

}

function createEntityTableEntry(className, description, count) {

    var row = $('<tr>')
    var className = $('<td>', {
        text: className,
    })
    var description = $('<td>', {
        text: description,
    })
    var count = $('<td>', {
        text: count,
    })

    row.append(className)
    row.append(description)
    row.append(count)

    return row
}

function updateEntityDescription(data) {
    $("#entityDescription").attr('title', data["definition"])
}

function showAlertMessage(message, type) {
    if (type == "entityAlert") {
        altertbox = $('#entityAlert')
        alterText = $('#entityAlertText')
    }
    else if (type == "entitySuccess") {
        altertbox = $('#entitySuccess')
        alterText = $('#entitySuccessText')
    }
    else if (type == "relationshipSuccess") {
        altertbox = $('#relationshipSuccess')
        alterText = $('#relationshipSuccessText')
    }
    else if (type == "relationshipAlert") {
        altertbox = $('#relationshipAlert')
        alterText = $('#relationshipAlertText')
    }
    $(alterText).empty()
    $(alterText).text(message)
    $(altertbox).removeClass("d-none")
}

$('.alert .close').on('click', function(e) {
    $(this).parent().addClass("d-none");
});

function downloadData() {
    //TODO implement
}
