 // Handler for .ready() called.
$(function() {
    
});

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
    var id = $('#task_id').val();   // used for edit        
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
        } else {    
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

// create new task
$( '#create_task_btn' ).click(function() {

    // set to new mode
    mode = MODE_CREATE;
    
    // reset all fields
    $('#task_name').val('');
    $('#task_available_scenarios').find('option').remove();
    $('#task_scenarios').find('option').remove();

    
    // get all available scenarios
    $.ajax({
        method: "GET",
        url: url_get_scenarios,
    }).done(function(data) {
        
        var scenarios = data['scenarios'];
        
        // set input values
        var value = ''
        for (var i = 0; i < scenarios.length; i++) {
            value = scenarios[i];
            var option = '<option value=' + value.name.split(' ').join('_') + '>' + value.name + '</option>';
            $("#task_available_scenarios").append(option);
        }        
        
        if (scenarios.length) {
            $("#add_task_scenario").prop('disabled', false);
        } else {
            $("#add_task_scenario").prop('disabled', true);
        }
                                
    }).fail(function() {
        alert( "Error - Edit context constraint failed." );
  });     

});

$("#add_task_scenario").click(function(e){
    
    var value = $('#task_available_scenarios').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    var option_values = [];
    $('#task_scenarios option').each(function() {
        option_values.push($(this).val());
    });    
        
    for (i = 0; i < option_values.length; i++) { 
        if (option_values[i] == value) {
            alert('Error: ' + value + ' already exists');
            $("#task_available_scenarios").focus();
            return;
        }
    }

    // all good - add condition
    var option = '<option value=' + value + '>' + value + '</option>';
    $("#task_scenarios").append(option);
    
    $("#remove_task_scenario").prop('disabled', false);

    return;
});

$("#remove_task_scenario").click(function(e){
 
    var value = $('#task_scenarios').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    var selector = "#task_scenarios option[value='" + value + "']";
    $(selector).remove();
    
    var size = $('#task_scenarios option').size()
    if (!size) {
        $("#remove_task_scenario").prop('disabled', true);
    }

    return;
});
    

function delete_task(id) {
    
    // fade out then remove
    $('#task-' + id).fadeOut('slow', function(){ $(this).remove(); });    

    $.ajax({
        method: "POST",
        url: url_delete_task,
        dataType: "json",
        data: {task_id: id},
    }).done(function( msg ) {
        var deleted = msg['deleted'];
        deleted = (deleted === "true");
        if (!deleted) {
            alert( "Error - failed to delete task" );
        }
    }).fail(function() {
        alert( "Error - failed to delete task" );
  });  
}

// edit existing task
function edit_task(id) {

    mode = MODE_UPDATE; // edit
    
    // get existing data and populate dialog
    $.ajax({
        method: "GET",
        url: url_edit_task,
        dataType: "json",
        data: {task_id: id},
    }).done(function(data) {
        // reset all fields
        $('#task_id').val('');
        $('#task_name').val('');
        $('#task_available_scenarios').find('option').remove();
        $('#task_scenarios').find('option').remove();
        
        var task_name = data['name'];
        var scenarios = data['scenarios'];
        
        alert('task_name: ' + task_name);
        alert('scenarios: ' + scenarios);

        // set input values
        $('#task_id').val(id); //hidden
        $('#task_name').val(task_name);

        var value = ''
        for (var i = 0; i < scenarios.length; i++) {
            value = scenarios[i];
            var option = '<option value=' + value + '>' + value + '</option>';
            $("#task_scenarios").append(option);
        }        

        if (scenarios.length) {
            $("#remove_task_scenario").prop('disabled', false);
        } else {
            $("#remove_task_scenario").prop('disabled', true);
        }
        
        $('#task_modal').modal('show');
                
    }).fail(function() {
        alert( "Error - Edit task failed." );
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
