// delete objective
function deleteObjective(name) {
        
    // fade out then remove
    $('#objective-' + name).fadeOut('slow', function(){ $(this).remove(); });
    
    $.ajax({
        method: "POST",
        url: url_delete_objective,
        dataType: "json",
        data: {name:name},
    }).done(function( msg ) {
        
    }).fail(function() {
        alert('Error: deleteObjective');
    });  
}

// delete obstacle
function deleteObstacle(name) {
    
    // fade out then remove
    $('#obstacle-' + name).fadeOut('slow', function(){ $(this).remove(); });
    
    $.ajax({
        method: "POST",
        url: url_delete_obstacle,
        dataType: "json",
        data: {name:name},
    }).done(function( msg ) {
        
    }).fail(function() {
        alert('Error: deleteObstacle');
    });  
}

// delete condition
function deleteCondition(name) {
    
    // fade out then remove
    $('#condition-' + name).fadeOut('slow', function(){ $(this).remove(); });
    
    $.ajax({
        method: "POST",
        url: url_delete_condition,
        dataType: "json",
        data: {name:name},
    }).done(function( msg ) {
        
    }).fail(function() {
        alert('Error: deleteCondition');
    });  
}

// delete context constraint
function deleteContextConstraint(name) {
    
    // fade out then remove
    $('#CC-' + name).fadeOut('slow', function(){ $(this).remove(); });
    
    $.ajax({
        method: "POST",
        url: url_delete_context_constraint,
        dataType: "json",
        data: {name:name},
    }).done(function( msg ) {
        
    }).fail(function() {
        alert('Error: deleteContextConstraint');
    });  
}

// delete task
function deleteTask(name) {
    
    // fade out then remove
    $('#task-' + name).fadeOut('slow', function(){ $(this).remove(); });
    
    $.ajax({
        method: "POST",
        url: url_delete_task,
        dataType: "json",
        data: {name:name},
    }).done(function( msg ) {
        
    }).fail(function() {
        alert('Error: deleteTask');
    });  
}

// delete step
function deleteStep(name) {
    
    // fade out then remove
    $('#step-' + name).fadeOut('slow', function(){ $(this).remove(); });
    
    $.ajax({
        method: "POST",
        url: url_delete_step,
        dataType: "json",
        data: {name:name},
    }).done(function( msg ) {
        
    }).fail(function() {
        alert('Error: deleteStep');
    });  
}

// delete permission
function deletePermission(name) {
    
    // fade out then remove
    $('#perm-' + name).fadeOut('slow', function(){ $(this).remove(); });
    
    $.ajax({
        method: "POST",
        url: url_delete_permission,
        dataType: "json",
        data: {name:name},
    }).done(function( msg ) {
        
    }).fail(function() {
        alert('Error: deletePermission');
    });  
}

// delete profile
function deleteProfile(name) {
    
    // fade out then remove
    $('#profile-' + name).fadeOut('slow', function(){ $(this).remove(); });
    
    $.ajax({
        method: "POST",
        url: url_delete_profile,
        dataType: "json",
        data: {name:name},
    }).done(function( msg ) {
        
    }).fail(function() {
        alert('Error: deleteProfile');
    });  
}

// delete scenario
function deleteScenario(name) {
    // fade out then remove
    $('#scenario-' + name).fadeOut('slow', function(){ $(this).remove(); });
    $.ajax({
        method: "POST",
        url: url_delete_scenario,
        dataType: "json",
        data: {name:name},
    }).done(function( msg ) {
        
    }).fail(function() {
        alert('Error: deleteScenario');
    });  
}

// delete role
function deleteRole(name) {
    // fade out then remove
    $('#role-' + name).fadeOut('slow', function(){ $(this).remove(); });
    $.ajax({
        method: "POST",
        url: url_delete_role,
        dataType: "json",
        data: {name:name},
    }).done(function( msg ) {
        
    }).fail(function() {
        alert('Error: deleteRole');
    });  
}
