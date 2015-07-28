    
// Handler for .ready() called.
$(function() {
    
    
    // set modal title for obstacle dialog
    $('#permission_modal').on('show.bs.modal', function(e) {
        
        if (mode == 1) {
            $('#permission_modal_title').text("Create New Permission"); 
        } 
    })
        
    $('#permission_modal_save_btn').click(function() {
        
        // validate all fields
        var id = $('#permission_id').val();
        var permission_operation_name = $('#permission_operation_name').val().split(' ').join('_');
        
        //alert(permission_operation_name);
        
        var permission_object_name = $('#permission_object_name').val().split(' ').join('_');
        //alert(permission_object_name);

        if (!permission_operation_name) {
            alert('Error: operation name cannot be empty.');
            $('#permission_operation_name').focus();
            $('#permission_operation_name').flash();
            return;
        }
        
        if (!permission_object_name) {
            alert('Error: object name cannot be empty.');
            $('#permission_object_name').focus();
            $('#permission_object_name').flash();
            return;
        }
        

        // create data
        var permission_data = new Permission(id, permission_operation_name, permission_object_name, mode);

        // post data
        $.ajax({
            method: "POST",
            url: url_dashboard,
            dataType: "json",
            data: permission_data
        }).done(function( msg ) {
            
            var permission_name = msg['permission_name'];
            var created = msg['created'];
            created = (created === "true");
            
            if (created) {
                $('#permission_modal').modal('toggle');
            } else {
                
                // create new mode
                if (mode == 1) {
                    alert('Error - failed to create permission: '+ permission_name);
                } else {
                    $('#permission_modal').modal('toggle');
                }
            }
            location.reload();            
        });    
    });    

});

$( '#create_permission_btn' ).click(function() {

    // set to new mode
    mode = 1;
    
    // reset all fields
    $('#permission_operation_name').val('');
    $('#permission_object_name').val('');
    
});

function delete_permission(id) {
    
    // fade out then remove
    $('#permission-' + id).fadeOut('slow', function(){ $(this).remove(); });    
    $.ajax({
        method: "POST",
        url: url_delete_permission,
        dataType: "json",
        data: {permission_id: id},
    }).done(function( msg ) {
        var deleted = msg['deleted'];
        deleted = (deleted === "true");
        if (!deleted) {
            alert( "Error - failed to delete permission" );
        }
    }).fail(function() {
        alert( "Error - failed to delete permission" );
  });  
}

function edit_condition(id) {

    mode = 2; // edit
    
    // get existing data and populate dialog
    $.ajax({
        method: "GET",
        url: url_edit_condition,
        dataType: "json",
        data: {condition_id: id},
    }).done(function( msg ) {

        // reset all fields
        $('#condition_id').val('');
        $('#condition_name').val('');
        
        var condition_name = msg['name'];

        // set input values
        $('#condition_id').val(id); //hidden
        $('#condition_name').val(condition_name);

        
        $('#condition_modal').modal('show');
                
    }).fail(function() {
        alert( "Error - Edit condition failed." );
  });    
}

// context menu functions
function perm_cardinality_constraints(id) {
    
    // get values from database
    mincardinality = 0
    maxcardinality = 0
    
    $.ajax({
        method: "GET",
        url: url_get_perm_cardinality_constraints,
        dataType: "json",
        data: {perm_id: id}
    }).done(function(data) {
        
        mincardinality = data['mincardinality'];
        maxcardinality = data['maxcardinality'];
        
        // set the min and max cardinality    
        $('#perm_cardinality_constraints_mincardinality').val(mincardinality);
        $('#perm_cardinality_constraints_maxcardinality').val(maxcardinality);
              
    }).fail(function() {
        alert( "Error - failed to get cardinality constraints." );
    });
    
    // set the permission id for this cardinality constraint modal
    $('#cardinality_constraint_perm_id').val(id);   
    
    $('#perm_cardinality_constraints_modal').modal('show');
}

$('#save_perm_cardinality_constraints').click(function() {
    
    // validate all fields
    var perm_id = $('#cardinality_constraint_perm_id').val();
    var mincardinality = $('#perm_cardinality_constraints_mincardinality').val();
    var maxcardinality = $('#perm_cardinality_constraints_maxcardinality').val();
        
    // create data
    var perm_data = new perm_cardinality_constraints_data(perm_id, mincardinality, maxcardinality);
    
    // post data
    $.ajax({
        method: "POST",
        url: url_dashboard,
        dataType: "json",
        data: perm_data
    }).done(function( msg ) {
        
        $('#perm_cardinality_constraints_modal').modal('toggle');        
    }).fail(function() {
        alert( "Error - failed to save cardinality constraints." );
  });
});    

// context menu function
function perm_context_constraints(id) {
    $('#perm_context_constraints_modal').modal('show');
    
    // create and update
    $.ajax({
        method: "GET",
        url: url_get_perm_context_constraints,
        dataType: "json",
        data: {perm_id: id}
    }).done(function(data) {
                
        // reset all
        $('#perm_available_context_constraints').find('option').remove();
        $('#perm_context_constraints').find('option').remove();
        
        var available_context_constraints = data['available_context_constraints'];
        var perm_context_constraints = data['perm_context_constraints'];
        
        
        // set input values
        $('#perm_context_constraint_perm_id').val(id); //hidden
        
        var value = ''
        for (var i = 0; i < available_context_constraints.length; i++) {
            value = available_context_constraints[i];
            var option = '<option value=' + value.name + '>' + value.name + '</option>';
            $("#perm_available_context_constraints").append(option);
        }        

        value = ''
        for (var i = 0; i < perm_context_constraints.length; i++) {
            value = perm_context_constraints[i];
            var option = '<option value=' + value + '>' + value + '</option>';
            $("#perm_context_constraints").append(option);
        }        

        if (perm_context_constraints.length) {
            $("#perm_unlink_context_constraint").prop('disabled', false);
        } else {
            $("#perm_unlink_context_constraint").prop('disabled', true);
        }
        // set the permission id for this cardinality constraint modal
        $('#perm_context_constraints_perm_id').val(id);   

        $('#perm_context_constraints_modal').modal('show');
              
    }).fail(function() {
        alert( "Error - failed to get context constraints." );
    });
    
    // set the permission id for this context constraint modal
    $('#perm_context_constraint_perm_id').val(id);   
}

$('#perm_link_context_constraint').click(function(e){
    
    var value = $('#perm_available_context_constraints').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    var option_values = [];
    $('#perm_context_constraints option').each(function() {
        option_values.push($(this).val());
    });    
        
    for (i = 0; i < option_values.length; i++) { 
        if (option_values[i] == value) {
            alert('Error: ' + value + ' already exists');
            $("#perm_available_context_constraints").focus();
            return;
        }
    }

    // all good - add condition
    var option = '<option value=' + value + '>' + value + '</option>';
    $("#perm_context_constraints").append(option);
    
    $("#perm_unlink_context_constraint").prop('disabled', false);

    return;
});

$('#perm_unlink_context_constraint').click(function(e){
 
    var value = $('#perm_context_constraints').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    var selector = "#perm_context_constraints option[value='" + value + "']";
    $(selector).remove();
    
    var size = $('#perm_context_constraints option').size()
    if (!size) {
        $("#perm_unlink_context_constraint").prop('disabled', true);
    }

    return;
});

$('#save_perm_context_constraints').click(function() {
    
    // validate all fields
    var perm_id = $('#perm_context_constraints_perm_id').val();
    
    var context_constraints = [];
    $('#perm_context_constraints option').each(function() {
        context_constraints.push($(this).val());
    });    

    // create data
    var data = new perm_context_constraints_data(perm_id, context_constraints);
  
    // post data
    $.ajax({
        method: "POST",
        url: url_dashboard,
        dataType: "json",
        data: data
    }).done(function( msg ) {
        $('#perm_context_constraints_modal').modal('toggle');       
    });    
        
});    

function perm_ssd_constraints(id) {
    $('#perm_ssd_constraints_modal').modal('show');
}


function Permission(id, operation_name, object_name, mode) {
    this.id = id;
    this.operation_name = operation_name;
    this.object_name = object_name;
    this.mode = mode;
    this.object_type = OBJECT_TYPE_PERMISSION;
}

function perm_cardinality_constraints_data(perm_id, mincardinality, maxcardinality) {
    this.id = perm_id;
    this.mincardinality = mincardinality;
    this.maxcardinality = maxcardinality;
    this.object_type = PERM_CARDINALITY_CONSTRAINTS;
}

function perm_context_constraints_data(perm_id, context_constraints) {
    this.id = perm_id;
    this.context_constraints = context_constraints;
    this.object_type = PERM_CONTEXT_CONSTRAINTS;
}

