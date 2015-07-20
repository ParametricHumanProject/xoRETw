    
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

function permission_cardinality_constraints() {
    //alert('helloworld');
    $('#perm_cardinality_constraint_modal').modal('toggle');
    
}

function permission_SSD_constraints() {
    //alert('helloworld');
    $('#perm_ssd_constraint_modal').modal('toggle');
    
}

function permission_CC() {
    $('#permission_CC_modal').modal('toggle');
}

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

function cardinality_constraints() {
    $('#perm_cardinality_constraint_modal').modal('show');
}

function Permission(id, operation_name, object_name, mode) {
    this.id = id;
    this.operation_name = operation_name;
    this.object_name = object_name;
    this.mode = mode;
    this.object_type = OBJECT_TYPE_PERMISSION;
}
