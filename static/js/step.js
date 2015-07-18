    
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


// objective
$( '#scenario_modal_create_new_step' ).click(function() {

    // set to new mode
    mode = 1;
    
    // reset all fields
    $('#step_actor').val('');
    $('#step_action').val('');
    $('#step_target').val('');
});

$( '#save_step_btn' ).click(function() {
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
    $.ajax({
        method: "POST",
        url: url_dashboard,
        dataType: "json",
        data: step_data
    }).done(function( msg ) {
        var step_name = msg['step_name'];
        var created = msg['created'];
        
        created = (created === "true");
        
        if (created) {
            $('#step_modal').modal('toggle');
        } else {    
            // and mode is create
            if (mode == 1) {
                alert('Error - failed to create step: '+ step_name);
            } else {
                $('#step_modal').modal('toggle');
            }
        }
        location.reload();            
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

/*

$("#add_condition").click(function(e){
    
    var value = $('#condition_input').val();
    
    if (!$.trim(value)) {
        // error
        alert('Error: condition value cannot be empty.');
        $( "#condition_input" ).focus();
        return;
    }

    var option_values = [];
    $('#condition_list option').each(function() {
        option_values.push($(this).val());
    });    
        
    for (i = 0; i < option_values.length; i++) { 
        if (option_values[i] == value.split(' ').join('_')) {
            alert('Error: ' + value.split(' ').join('_') + ' already exists');
            $( "#condition_input" ).focus();
            return;
        }
    }

    // add to list
    var option = '<option value=' + value.split(' ').join('_') + '>' + value + '</option>';
    $("#condition_list").append(option);

    // clear input value
    $('#condition_input').val('');
    $("#remove_condition").prop('disabled', false);

    return;
});

$("#remove_condition").click(function(e){
 
    var value = $('#condition_list').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    var selector = "#condition_list option[value='" + value + "']";
    $(selector).remove();
    
    var size = $('#condition_list option').size()
    if (!size) {
        $("#remove_condition").prop('disabled', true);
    }

    return;
});


// helper
function change_select_label(e) {
    var property_value = $( '#'+e.target.id ).text();
    $('#objective_type_label').text(property_value);
}

function delete_objective(id) {
    
    // fade out then remove
    $('#objective-' + id).fadeOut('slow', function(){ $(this).remove(); });    

    
    $.ajax({
        method: "POST",
        url: url_delete_objective,
        dataType: "json",
        data: {objective_id: id},
    }).done(function( msg ) {
        var message = JSON.parse(msg);
    }).fail(function() {
        alert( "Error - failed to delete objective" );
  });    
}

function edit_objective_btn(id) {

    mode = 2; // edit
    
    // get existing data and populate dialog
    $.ajax({
        method: "GET",
        url: url_edit_objective,
        dataType: "json",
        data: {objective_id: id},
    }).done(function( msg ) {

        // reset all fields
        $('#objective_id').val('');
        $('#objective_name').val('');
        $('#objective_type_label').text('Select');
        $('#condition_input').val('');
        $('#condition_list').find('option').remove();
        
        var objective_name = msg['name'];
        var objective_type = msg['type'];
        var conditions = msg['conditions'];

        // set input values
        $('#objective_id').val(id); //hidden
        $('#objective_name').val(objective_name);
        $('#objective_type_label').text(objective_type);

        var value = ''
        for (var i = 0; i < conditions.length; i++) {
            value = conditions[i];
            var option = '<option value=' + value.split(' ').join('_') + '>' + value + '</option>';
            $("#condition_list").append(option);
        }        

        if (conditions.length) {
            $("#remove_condition").prop('disabled', false);
        } else {
            $("#remove_condition").prop('disabled', true);
        }
        
        $('#objective_modal').modal('show');
                
    }).fail(function() {
        alert( "Error - Edit objective failed." );
  });    
    
}
*/
