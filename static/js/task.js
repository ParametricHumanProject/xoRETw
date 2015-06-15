 // Handler for .ready() called.
$(function() {
    
    
    // set modal title for obstacle dialog
    $('#task_modal').on('show.bs.modal', function(e) {
        
        if (mode == 1) {
            $('#task_modal_title').text("Create New Task"); 
        } else {
            $('#task_modal_title').text("Edit Task");   
        }
    })
    
    $( '#save_task_btn' ).click(function() {
        // validate all fields
        
        // used for edit        
        var id = $('#task_id').val();
        var name = $('#task_name').val().split(' ').join('_');

        if (!name) {
            alert('Error: task name cannot be empty.');
            $('#task_name').focus();
            $('#task_name').flash();
            return;
        }
        
        var scenarios = [];
        $('#task_scenarios option').each(function() {
            scenarios.push($(this).val().split(' ').join('_'));
        });    

        // create data
        var task_data = new Task(id, name, scenarios, mode);
        
        // post data
        $.ajax({
            method: "POST",
            url: url_dashboard,
            dataType: "json",
            data: task_data
        }).done(function( msg ) {
            
            var task_name = msg['task_name'];
            var created = msg['created'];
            created = (created === "true");
            
            if (created) {
                $('#task_modal').modal('toggle');
            } else {    // created is false
                
                // create new mode
                if (mode == 1) {
                    alert('Error - failed to create task: '+ task_name);
                } else {
                    $('#task_modal').modal('toggle');
                }
            }
            location.reload();            
        });    
    });    

});

// constraint
$( '#create_task_btn' ).click(function() {

    // set to new mode
    mode = MODE_CREATE;
    
    // reset all fields
    $('#task_name').val('');
    $('#task_available_scenarios').find('option').remove();
    $('#task_scenarios').find('option').remove();

/*    
    // get all available scenarios
    $.ajax({
        method: "GET",
        url: url_get_scenarios,
    }).done(function( msg ) {
        
        var scenarios = msg['scenarios'];
        
        // set input values
        var value = ''
        for (var i = 0; i < conditions.length; i++) {
            value = conditions[i];
            var option = '<option value=' + value.name.split(' ').join('_') + '>' + value.name + '</option>';
            $("#constraint_available_conditions").append(option);
        }        
        
        if (conditions.length) {
            $("#add_constraint_condition").prop('disabled', false);
        } else {
            $("#add_constraint_condition").prop('disabled', true);
        }
                                
    }).fail(function() {
        alert( "Error - Edit context constraint failed." );
  });     
  */  
});

$("#add_task_scenario").click(function(e){
    
    var value = $('#constraint_available_conditions').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    var option_values = [];
    $('#constraint_conditions option').each(function() {
        option_values.push($(this).val());
    });    
        
    for (i = 0; i < option_values.length; i++) { 
        if (option_values[i] == value) {
            alert('Error: ' + value + ' already exists');
            $("#constraint_available_conditions").focus();
            return;
        }
    }

    // all good - add condition
    var option = '<option value=' + value + '>' + value + '</option>';
    $("#constraint_conditions").append(option);
    
    $("#remove_constraint_condition").prop('disabled', false);

    return;
});

$("#remove_task_scenario").click(function(e){
 
    var value = $('#constraint_conditions').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    var selector = "#constraint_conditions option[value='" + value + "']";
    $(selector).remove();
    
    var size = $('#constraint_conditions option').size()
    if (!size) {
        $("#remove_constraint_condition").prop('disabled', true);
    }

    return;
});
    

function delete_task(id) {
    
    // fade out then remove
    $('#constraint-' + id).fadeOut('slow', function(){ $(this).remove(); });    

    $.ajax({
        method: "POST",
        url: url_delete_constraint,
        dataType: "json",
        data: {constraint_id: id},
    }).done(function( msg ) {
        var deleted = msg['deleted'];
        deleted = (deleted === "true");
        if (!deleted) {
            alert( "Error - failed to delete obstacle" );
        }
    }).fail(function() {
        alert( "Error - failed to delete obstacle" );
  });  
}

function edit_constraint(id) {

    mode = MODE_UPDATE; // edit
    
    // get existing data and populate dialog
    $.ajax({
        method: "GET",
        url: url_edit_constraint,
        dataType: "json",
        data: {constraint_id: id},
    }).done(function( msg ) {
        // reset all fields
        $('#constraint_id').val('');
        $('#constraint_name').val('');
        $('#constraint_available_conditions').find('option').remove();
        $('#constraint_conditions').find('option').remove();
        
        var constraint_name = msg['name'];
        var conditions = msg['conditions'];
        
        alert(conditions);

        // set input values
        $('#constraint_id').val(id); //hidden
        $('#constraint_name').val(constraint_name);

        var value = ''
        for (var i = 0; i < conditions.length; i++) {
            value = conditions[i];
            var option = '<option value=' + value + '>' + value + '</option>';
            $("#constraint_conditions").append(option);
        }        

        if (conditions.length) {
            $("#remove_constraint_condition").prop('disabled', false);
        } else {
            $("#remove_constraint_condition").prop('disabled', true);
        }
        
        $('#constraint_modal').modal('show');
                
    }).fail(function() {
        alert( "Error - Edit constraint failed." );
  });    
    
}

function Task(id, name, scenarios, mode) {
    
    if (mode == MODE_UPDATE) {
        this.id = id;    
    }
    
    this.name = name;
    this.scenarios = scenarios;
    this.mode = mode;
    this.object_type = OBJECT_TYPE_TASK;
}
