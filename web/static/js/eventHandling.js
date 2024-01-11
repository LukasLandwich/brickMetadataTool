//On Every Page Load
jQuery(updateStatistics)
jQuery(changeEntityCreationMode)

//Click Event Handlers
$('#propertySave_cancelButton').on("click", function(){$('#propertySaveModal').modal('hide')})
$('#addEntityBlueprint').on("click", function(){$('#propertySaveModal').modal('show')})
$('#propertySave_saveButton').on("click", savePropertySaveModal)
$('#propertySettignsDropdownButton').on("click", function() {$('#propertySettignsDropdown').toggle()})
$('#downloadDataButton').on("click", downloadData)
$('#addRelationshipOnExistingSubmit').on("click", submitRelationshipOnExisiting)
$('#addEntitySubmit').on("click", entitySumbmitClick);
$('#addEntityClear').on("click", clearEntityAndPropertyInputs)

//Change Event Handlers
$('#switch_existingEntities').on("change", changeEntityCreationMode)
$('#relationshipEntityFromSelect').on("change", onRelationshipEntityFromSelectChange)
$('#relationshipTypeSelect').on("change", onRelationshipEntityTypeSelectChange)
$('#entityTypeSelect').on("change", entityTypeSelectChange)
$('#addAnotherEntityCheck').on("change", addAnotherEntityCheckChange)
$('#propertyForm_availableBlueprintsSelect').on("change", onAvailableBlueprintsSelectChange)




$('#addEntityCancle').on("click", function() {   
    console.log("Cancle")   
});

