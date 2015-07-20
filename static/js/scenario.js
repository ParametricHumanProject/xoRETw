    
// Handler for .ready() called.
$(function() {
    
    // set modal title for objective dialog
    $('#scenario_modal').on('show.bs.modal', function(e) {
        if (mode == 1) {
            $('#scenario_modal_title').text("Create New Scenario"); 
        } else {
            $('#scenario_modal_title').text("Edit Scenario");   
        }
    })

});

$('#scenario_modal_create_new_step').click(function() {
    $('#step_modal').modal('toggle');
});


$('#scenario_modal_add_step').click(function() {

    var value = $('#scenario_available_steps').val();
        
    if (!value) {
        alert('Error: no option selected - please select of the currently available steps.');
        $('#scenario_available_steps').focus();
        $('#scenario_available_steps').flash();

        return;
    }
    
    alert('adding step ' + value);
});

// scenario
$( '#create_scenario_btn' ).click(function() {

    // set to new mode
    mode = 1;
    
    // reset all fields
    $('#scenario_name').val('');
    $('#scenario_available_steps').find('option').remove();
    
    $("#scenario_modal_add_step").prop('disabled', true);
    
    // get all available steps
    $.ajax({
        method: "GET",
        url: url_get_steps,
    }).done(function(data) {
        
        var steps = data['steps'];
        
        // set input values
        var value = ''
        for (var i = 0; i < steps.length; i++) {
            value = steps[i];
            var option = '<option value=' + value.name.split(' ').join('_') + '>' + value.name + '</option>';
            $("#scenario_available_steps").append(option);
        }
             
        if (steps.length) {
            $("#scenario_modal_add_step").prop('disabled', false);
        } else {
            $("#scenario_modal_add_step").prop('disabled', true);
        }
                                
    }).fail(function() {
        alert( "Error - Edit context constraint failed." );
  });
      
});

$('#save_scenario_btn').click(function() {
    
    // validate all fields    
    var id = $('#scenario_id').val();
    var scenario_name = $('#scenario_name').val().split(' ').join('_');

    if (!scenario_name) {
        alert('Error: scenario name cannot be empty.');
        $('#scenario_name').focus();
        $('#scenario_name').flash();
        return;
    }

    // create data
    var scenario_data = new Scenario(id, scenario_name, mode);
    
    // post data
    $.ajax({
        method: "POST",
        url: url_dashboard,
        dataType: "json",
        data: scenario_data
    }).done(function( data ) {
        var scenario_name = data['scenario_name'];
        var created = data['created'];
        
        created = (created === "true");
        
        if (created) {
            $('#scenario_modal').modal('toggle');
        } else {    
            // and was the mode set to create
            if (mode == 1) {
                alert('Error - failed to create scenario: '+ scenario_name);
            } else {
                // do nothing
            }
        }
        location.reload();
    }); 
});

function delete_scenario(id) {
    
    // fade out then remove
    $('#scenario-' + id).fadeOut('slow', function(){ $(this).remove(); });    
    $.ajax({
        method: "POST",
        url: url_delete_scenario,
        dataType: "json",
        data: {scenario_id: id},
    }).done(function( msg ) {
        var deleted = msg['deleted'];
        deleted = (deleted === "true");
        if (!deleted) {
            alert( "Error - failed to delete scenario" );
        }
    }).fail(function() {
        alert( "Error - failed to delete scenario" );
  });  
}

function Scenario(id, name, mode) {
    this.id = id;
    this.name = name;
    this.mode = mode;
    this.object_type = OBJECT_TYPE_SCENARIO;
}

function edit_scenario(id) {

    mode = 2; // edit
    
    // get existing data and populate dialog
    $.ajax({
        method: "GET",
        url: url_edit_scenario,
        dataType: "json",
        data: {scenario_id: id},
    }).done(function(data) {

        // reset all fields
        $('#scenario_name').val('');
        $('#scenario_available_steps').find('option').remove();
        
        $("#scenario_modal_add_step").prop('disabled', true);
        
        var scenario_name = data['name'];

        // set input values
        $('#scenario_id').val(id); //hidden
        $('#scenario_name').val(scenario_name);

        $('#scenario_modal').modal('show');
        
        var steps = data['steps'];
        
        // set input values
        var value = ''
        for (var i = 0; i < steps.length; i++) {
            value = steps[i];
            var option = '<option value=' + value.name.split(' ').join('_') + '>' + value.name + '</option>';
            $("#scenario_available_steps").append(option);
        }
             
        if (steps.length) {
            $("#scenario_modal_add_step").prop('disabled', false);
        } else {
            $("#scenario_modal_add_step").prop('disabled', true);
        }
        
                
    }).fail(function() {
        alert( "Error - Edit scenario failed." );
  });    
  
        
          
}


