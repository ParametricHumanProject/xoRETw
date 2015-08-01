/*
It depends on the context, but in most cases it is different. And usually one implies the other.
If a user clicks on "Edit" , he/she can change the values, but the Update is not performed until they click on "Save". In 99% of the cases , a user who edits a record will want to update it...
*  * */
 
// Handler for .ready() called.
$(function() {

});

// set modal title for obstacle dialog
$('#role_modal').on('show.bs.modal', function(e) {
    
    if (mode == 1) {
        $('#role_modal_title').text("Create New Role"); 
    } else {
        $('#role_modal_title').text("Edit Role");   
    }
})

$('#create_role').click(function() {

    // set to new mode
    mode = MODE_CREATE;
    
    // reset all fields
    $('#role_name').val('');
    $('#role_available_roles').find('option').remove();
    $('#role_junior_roles').find('option').remove();
    $('#role_senior_roles').find('option').remove();
    
    // get all available conditions
    $.ajax({
        method: "GET",
        url: url_get_roles,
    }).done(function(data) {
        
        var roles = data['roles'];
        
        // set input values
        var value = ''
        for (var i = 0; i < roles.length; i++) {
            value = roles[i];
            var option = '<option value=' + value.name.split(' ').join('_') + '>' + value.name + '</option>';
            $("#role_available_roles").append(option);
        }        
        
        if (roles.length) {
            $("#role_add_junior_role").prop('disabled', false);
            $("#role_add_senior_role").prop('disabled', false);
        } else {
            $("#role_add_junior_role").prop('disabled', true);
            $("#role_add_senior_role").prop('disabled', true);
        }
                                
    }).fail(function() {
        alert( "Error - create role failed." );
  });
         
});

$('#save_role').click(function() {

    var role_name = $('#role_name').val().split(' ').join('_');
    
    var exists_role = false;
    
    // alternative way is to check <select> with id="role_available_roles"
    // check if role exists
    $.ajax({
        method: "GET",
        url: url_exists_role,
        async: false,
        dataType: "json",
        data: {role_name: role_name},
    }).done(function(data) {
                
        exists_role = (String(data['exists']) === "true");
                
    }).fail(function() {
        alert( "Error - exists role failed." );
        return;
    });  
        
    if (exists_role) {
        
        // error role already exists
        alert('Error: the role ' + '"' + role_name + '"' + ' already exists.');
        $('#role_name').focus();
        $('#role_name').flash();
        return;        
    }
    
    var id = $('#role_id').val();    
    
    // check for empty string
    if (!role_name) {
        alert('Error: role name cannot be empty.');
        $('#role_name').focus();
        $('#role_name').flash();
        return;
    }
    
    // get all the junior roles
    var junior_roles = [];
    $('#role_junior_roles option').each(function() {
        junior_roles.push($(this).val().split(' ').join('_'));
    });    

    // get all the senior roles
    var senior_roles = [];
    $('#role_senior_roles option').each(function() {
        senior_roles.push($(this).val().split(' ').join('_'));
    });    
    
    if (junior_roles.length) {
        // now check if two or more of the intended juniorRoles are defined as 
        // mutual exclusive or own mutual exclusive permissions
        var i;
        var j;
        for (i = 0; i < junior_roles.length; i++) {
            for (i = 0; i < junior_roles.length; i++) {
                if (junior_roles[i] !== junior_roles[j]) {

                if (isStaticallyMutualExclusive(junior_roles[i], junior_roles[j])) {
                 alert( "[self] [self proc] FAILED, at least two of the intended junior-roles\
                                         of <<$name>> are mutual exclusive.\
                                         <<$r1>> and <<$r2>> are mutual exclusive or own permissions that\
                                         are mutual exclusive.");
                  return
                
                }
            }            
        }
    }
}

    // create data
    var role_data = new Role(id, role_name, junior_roles, senior_roles, mode);
    
    // post data
    $.ajax({
        method: "POST",
        url: url_dashboard,
        dataType: "json",
        data: role_data
    }).done(function(data) {
        
        var role_name = data['name'];
        var created = data['created'];
        created = (created === "true");
        
        if (created) {
            $('#role_modal').modal('toggle');
        } else {    
            // check if create new mode
            if (mode == 1) {
                alert('Error - failed to create role: '+ role_name);
            } else {
                $('#role_modal').modal('toggle');
            }
        }
        location.reload();            
    });    
});    

function delete_role(id) {
    
    // fade out then remove
    $('#role-' + id).fadeOut('slow', function(){ $(this).remove(); });    
    $.ajax({
        method: "POST",
        url: url_delete_role,
        dataType: "json",
        data: {role_id: id},
    }).done(function( msg ) {
        var deleted = msg['deleted'];
        deleted = (deleted === "true");
        if (!deleted) {
            alert( "Error - failed to delete role" );
        }
    }).fail(function() {
        alert( "Error - failed to delete role" );
  });  
}

$('#role_add_junior_role').click(function(e) {
    
    var value = $('#role_available_roles').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    // check if role exists in senior roles, if so, error
    var senior_roles = [];
    $('#role_senior_roles option').each(function() {
        senior_roles.push($(this).val());
    });    
        
    for (i = 0; i < senior_roles.length; i++) { 
        if (senior_roles[i] == value) {
            alert('Error: acyclic constraint violated. Role/class hierarchies are directed acyclic graphs. Cannot have a role as both junior and senior.');
            $("#role_available_roles").focus();
            return;
        }
    }
    
    var option_values = [];
    $('#role_junior_roles option').each(function() {
        option_values.push($(this).val());
    });    
        
    for (i = 0; i < option_values.length; i++) { 
        if (option_values[i] == value) {
            alert('Error: ' + value + ' already exists');
            $("#role_available_roles").focus();
            return;
        }
    }

    // all good - add condition
    var option = '<option value=' + value + '>' + value + '</option>';
    $("#role_junior_roles").append(option);
    
    $("#role_remove_junior_role").prop('disabled', false);

    return;
});

$('#role_add_senior_role').click(function(e) {
    
    var value = $('#role_available_roles').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    // check if role exists in junior roles, if so, error
    var junior_roles = [];
    $('#role_junior_roles option').each(function() {
        junior_roles.push($(this).val());
    });    
        
    for (i = 0; i < junior_roles.length; i++) { 
        if (junior_roles[i] == value) {
            alert('Error: acyclic constraint violated. Role/class hierarchies are directed acyclic graphs. Cannot have a role as both junior and senior.');
            $("#role_available_roles").focus();
            return;
        }
    }
    
    var option_values = [];
    $('#role_senior_roles option').each(function() {
        option_values.push($(this).val());
    });    
        
    for (i = 0; i < option_values.length; i++) { 
        if (option_values[i] == value) {
            alert('Error: ' + value + ' already exists');
            $("#role_available_roles").focus();
            return;
        }
    }

    // all good - add condition
    var option = '<option value=' + value + '>' + value + '</option>';
    $("#role_senior_roles").append(option);
    
    $("#role_remove_senior_role").prop('disabled', false);

    return;
});

$("#role_remove_junior_role").click(function(e){
 
    var value = $('#role_junior_roles').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    var selector = "#role_junior_roles option[value='" + value + "']";
    $(selector).remove();
    
    var size = $('#role_junior_roles option').size()
    if (!size) {
        $("#role_remove_junior_role").prop('disabled', true);
    }

    return;
});

$("#role_remove_senior_role").click(function(e){
 
    var value = $('#role_senior_roles').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    var selector = "#role_senior_roles option[value='" + value + "']";
    $(selector).remove();
    
    var size = $('#role_senior_roles option').size()
    if (!size) {
        $("#role_remove_senior_role").prop('disabled', true);
    }

    return;
});

// context menu functions
function role_cardinality_constraints(id) {
    
    // get values from database
    mincardinality = 0
    maxcardinality = 0
    
    $.ajax({
        method: "GET",
        url: url_get_role_cardinality_constraints,
        dataType: "json",
        data: {role_id: id}
    }).done(function(data) {
        
        mincardinality = data['mincardinality'];
        maxcardinality = data['maxcardinality'];
        
        // set the min and max cardinality    
        $('#role_cardinality_constraints_mincardinality').val(mincardinality);
        $('#role_cardinality_constraints_maxcardinality').val(maxcardinality);
        $('#role_cardinality_constraints_modal').modal('show');
              
    }).fail(function() {
        alert( "Error - failed to get cardinality constraints." );
    });
    
    // set the role id for this cardinality constraint modal
    $('#cardinality_constraint_role_id').val(id);       
}

$('#save_role_cardinality_constraints').click(function() {
    
    // validate all fields
    var role_id = $('#cardinality_constraint_role_id').val();
    var mincardinality = $('#role_cardinality_constraints_mincardinality').val();
    var maxcardinality = $('#role_cardinality_constraints_maxcardinality').val();
        
    // create data
    var role_data = new role_cardinality_constraints_data(role_id, mincardinality, maxcardinality);
    
    // post data
    $.ajax({
        method: "POST",
        url: url_dashboard,
        dataType: "json",
        data: role_data
    }).done(function(data) {
        
        $('#role_cardinality_constraints_modal').modal('toggle');        
    }).fail(function() {
        alert( "Error - failed to save cardinality constraints." );
  });
});    

function role_perm_to_role_assignment(id) {
    alert(id);
    $('#role_perm_to_role_assignment_modal').modal('show');
}

function role_ssd_role_constraints(id) {
    //alert(id);
    $('#role_ssd_role_constraints_modal').modal('show');
}

function create_role() {
    $('#create_role_btn').click();
    $('#role_modal').modal('show');
}

function Role(id, name, junior_roles, senior_roles, mode) {
    
    if (mode == MODE_UPDATE) {
        this.id = id;    
    }
    
    this.name = name;
    this.junior_roles = junior_roles;
    this.senior_roles = senior_roles;
    this.mode = mode;
    this.object_type = OBJECT_TYPE_ROLE;
}

function role_cardinality_constraints_data(role_id, mincardinality, maxcardinality) {
    this.id = role_id;
    this.mincardinality = mincardinality;
    this.maxcardinality = maxcardinality;
    this.object_type = ROLE_CARDINALITY_CONSTRAINT;
}
