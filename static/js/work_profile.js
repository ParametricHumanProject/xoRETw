 // Handler for .ready() called.
$(function() {

    // set modal title for work profile dialog
    $('#work_profile_modal').on('show.bs.modal', function(e) {
        
        if (mode == 1) {
            $('#work_profile_modal_title').text("Create New Work Profile"); 
        } else {
            $('#work_profile_modal_title').text("Edit Work Profile");   
        }
    })
    
    $( '#save_work_profile_btn' ).click(function() {
        // validate all fields
        
        // used for edit        
        var work_profile_id = $('#work_profile_id').val();
        var work_profile_name = $('#work_profile_name').val().split(' ').join('_');

        if (!work_profile_name) {
            alert('Error: work profile name cannot be empty.');
            $('#work_profile_name').focus();
            $('#work_profile_name').flash();
            return;
        }
        
        var attached_tasks = [];
        $('#work_profile_attached_tasks option').each(function() {
            attached_tasks.push($(this).val().split(' ').join('_'));
        });    

        // create data
        var work_profile_data = new WorkProfile(work_profile_id, work_profile_name, attached_tasks, mode);
        
        // post data
        $.ajax({
            method: "POST",
            url: url_dashboard,
            dataType: "json",
            data: task_data
        }).done(function( msg ) {
            
            var work_profile_name = msg['work_profile_name'];
            var created = msg['created'];
            created = (created === "true");
            
            if (created) {
                $('#work_profile_modal').modal('toggle');
            } else {    
                // if created is false then if create new mode
                if (mode == 1) {
                    alert('Error - failed to create work profile: '+ work_profile_name);
                } else {
                    // toggle hide/close modal
                    $('#work_profile_modal').modal('toggle');
                }
            }
            location.reload();            
        });    
    });    

});

// work profile
$( '#create_work_profile_btn' ).click(function() {

    // set to new mode
    mode = MODE_CREATE;
    
    // reset all fields
    $('#work_profile_name').val('');
    $('#work_profile_available_tasks').find('option').remove();
    $('#work_profile_attached_tasks').find('option').remove();

});

$("#work_profile_add_task").click(function(e){
    
    var value = $('#work_profile_available_tasks').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    var option_values = [];
    $('#work_profile_available_tasks option').each(function() {
        option_values.push($(this).val());
    });    
        
    for (i = 0; i < option_values.length; i++) { 
        if (option_values[i] == value) {
            alert('Error: ' + value + ' already exists');
            $("#work_profile_available_tasks").focus();
            return;
        }
    }

    // all good - add condition
    var option = '<option value=' + value + '>' + value + '</option>';
    $("#work_profile_attached_tasks").append(option);
    
    $("#work_profile_remove_task").prop('disabled', false);

    return;
});

$("#work_profile_remove_task").click(function(e){
 
    var value = $('#work_profile_attached_tasks').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    var selector = "#work_profile_attached_tasks option[value='" + value + "']";
    $(selector).remove();
    
    var size = $('#work_profile_attached_tasks option').size()
    if (!size) {
        $("#work_profile_remove_task").prop('disabled', true);
    }

    return;
});
    

function delete_task(id) {
    
    // fade out then remove
    $('#work_profile-' + id).fadeOut('slow', function(){ $(this).remove(); });    

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
        $('#work_profile_id').val('');
        $('#work_profile_name').val('');
        $('#work_profile_available_tasks').find('option').remove();
        $('#work_profile_attached_tasks').find('option').remove();
        
        var work_profile_name = msg['name'];
        var attached_tasks = msg['conditions'];
        
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
