    
// Handler for .ready() called.
$(function() {
    
    
    // set modal title for obstacle dialog
    $('#step_modal').on('show.bs.modal', function(e) {
        
        if (mode == 1) {
            $('#step_modal_title').text("Create New Step"); 
        } else {
            $('#step_modal_title').text("Edit Step");   
        }
    })
});


// step
$( '#scenario_modal_create_new_step' ).click(function() {

    // set to new mode
    mode = 1;
    
    // reset all fields
    $('#step_actor').val('');
    $('#step_action').val('');
    $('#step_target').val('');
});

$( '#save_step' ).click(function() {
    //alert('save_step_btn')
    // validate all fields
    var id = $('#step_id').val();
    var step_actor = $('#step_actor').val().split(' ').join('_');

    if (!step_actor) {
        alert('Error: step actor cannot be empty.');
        $('#step_actor').focus();
        $('#step_actor').flash();
        return;
    }

    var step_action = $('#step_action').val().split(' ').join('_');

    if (!step_action) {
        alert('Error: step action cannot be empty.');
        $('#step_action').focus();
        $('#step_action').flash();
        return;
    }

    var step_target = $('#step_target').val().split(' ').join('_');

    if (!step_target) {
        alert('Error: step target cannot be empty.');
        $('#step_target').focus();
        $('#step_target').flash();
        return;
    }

    // create data
    var step_data = new Step(id, step_actor, step_action, step_target, mode);
    
    // post data
    //alert('about to post data');
    $.ajax({
        method: "POST",
        url: url_dashboard,
        dataType: "json",
        data: step_data
    }).done(function(data) {
        //alert('11111')
        var step_name = data['step_name'];
        var created = data['created'];
        
        var s = 'created is ' + created;
        //alert(s);
        created = (created === "true");
        
        if (created) {
            $('#step_modal').modal('toggle');
            
            // add new step to list of all available steps in the scenario modal
            var option = '<option value=' + step_name + '>' + step_name + '</option>';
            $("#scenario_available_steps").append(option);
            $("#scenario_modal_add_step").prop('disabled', false);
            
        } else {    
            // and was the mode set to create
            if (mode == 1) {
                alert('Error - failed to create step: '+ step_name);
            } else {
                //$('#step_modal').modal('toggle');
            }
        }
    }); 

});

function Step(id, actor, action, target, mode) {
    this.id = id;
    this.actor = actor;
    this.action = action;
    this.target = target;
    this.mode = mode;
    this.object_type = OBJECT_TYPE_STEP;
}

function delete_step(id) {
    
    // fade out then remove
    $('#step-' + id).fadeOut('slow', function(){ $(this).remove(); });    
    $.ajax({
        method: "POST",
        url: url_delete_step,
        dataType: "json",
        data: {step_id: id},
    }).done(function( msg ) {
        var deleted = msg['deleted'];
        deleted = (deleted === "true");
        if (!deleted) {
            alert( "Error - failed to delete step" );
        }
    }).fail(function() {
        alert( "Error - failed to delete step" );
  });  
}


