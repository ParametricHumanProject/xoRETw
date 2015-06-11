    
// Handler for .ready() called.
$(function() {
    
    
    // set modal title for obstacle dialog
    $('#condition_modal').on('show.bs.modal', function(e) {
        if (mode == 1) {
            $('#condition_modal_title').text("Create New Condition"); 
        } else {
            $('#condition_modal_title').text("Edit Condition");   
        }
    })
    
    $( '#save_condition_btn' ).click(function() {
        // validate all fields
        var id = $('#condition_id').val();
        var name = $('#condition_name').val().split(' ').join('_');

        if (!name) {
            alert('Error: condition name cannot be empty.');
            $("#condition_name").focus();
            $( '#condition_name' ).flash();
            return;
        }
        
        var type = $('#condition_type_label').text();

        // create data
        var condition_data = new Condition(id, name, mode);

        // post data
        $.ajax({
            method: "POST",
            url: url_dashboard,
            dataType: "json",
            data: condition_data
        }).done(function( msg ) {
            
            var condition_name = msg['condition_name'];
            var created = msg['created'];
            created = (created === "true");
            
            if (created) {
                $('#condition_modal').modal('toggle');
            } else {
                
                // create new mode
                if (mode == 1) {
                    alert('Error - failed to create condition: '+ name);
                } else {
                    $('#condition_modal').modal('toggle');
                }
            }
            location.reload();            
        });    
    });    

});

$( '#create_condition_btn' ).click(function() {

    // set to new mode
    mode = 1;
    
    // reset all fields
    $('#condition_name').val('');
});

function delete_condition(id) {
    
    // fade out then remove
    $('#condition-' + id).fadeOut('slow', function(){ $(this).remove(); });    
    $.ajax({
        method: "POST",
        url: url_delete_condition,
        dataType: "json",
        data: {condition_id: id},
    }).done(function( msg ) {
        var deleted = msg['deleted'];
        deleted = (deleted === "true");
        if (!deleted) {
            alert( "Error - failed to delete condition" );
        }
    }).fail(function() {
        alert( "Error - failed to delete condition" );
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

function Condition(id, name, mode) {
    this.id = id;
    this.name = name;
    this.mode = mode;
    this.object_type = OBJECT_TYPE_CONDITION;
}
