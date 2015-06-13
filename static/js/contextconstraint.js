    
// Handler for .ready() called.
$(function() {
    
    
    // set modal title for obstacle dialog
    $('#constraint_modal').on('show.bs.modal', function(e) {
        
        if (mode == 1) {
            $('#constraint_modal_title').text("Create New Condition"); 
        } else {
            $('#constraint_modal_title').text("Edit Condition");   
        }
    })
    
    $( '#save_condition_btn' ).click(function() {
        // validate all fields
        var id = $('#condition_id').val();
        var name = $('#condition_name').val().split(' ').join('_');

        if (!name) {
            alert('Error: constraint name cannot be empty.');
            $("#constraint_name").focus();
            $( '#constraint_name' ).flash();
            return;
        }
        
        var conditions = [];
        $('#constraint_conditions option').each(function() {
            conditions.push($(this).val().split(' ').join('_'));
        });    

        // create data
        var obstacle_data = new Obstacle(id, name, type, conditions, mode);

        // post data
        $.ajax({
            method: "POST",
            url: url_dashboard,
            dataType: "json",
            data: obstacle_data
        }).done(function( msg ) {
            
            var obstacle_name = msg['obstacle_name'];
            var created = msg['created'];
            created = (created === "true");
            
            if (created) {
                $('#obstacle_modal').modal('toggle');
                //location.reload();            
            } else {    // created is false
                
                // create new mode
                if (mode == 1) {
                    alert('Error - failed to create obstacle: '+ obstacle_name);
                } else {
                    $('#obstacle_modal').modal('toggle');
                }
            }
            location.reload();            
        });    
    });    

});

// constraint
$( '#create_constraint_btn' ).click(function() {

    // set to new mode
    mode = 1;
    
    // reset all fields
    $('#constraint_name').val('');
    $('#constraint_available_conditions').find('option').remove();
    $('#constraint_conditions').find('option').remove();
    
    // get all available conditions
    $.ajax({
        method: "GET",
        url: url_get_conditions,
    }).done(function( msg ) {
        
        var conditions = msg['conditions'];
        
        //alert(conditions.length);

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
        
        //$('#obstacle_modal').modal('show');
                        
    }).fail(function() {
        alert( "Error - Edit context constraint failed." );
  });        
});

$("#add_constraint_condition").click(function(e){
    
    var value = $('#constraint_available_conditions').val();
    //alert(value)
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    //alert('you selected ' + value)
    
    if (!$.trim(value)) {
        // error
        alert('Error: condition value cannot be empty.');
        $( "#constraint_conditions" ).focus();
        return;
    }

    var option_values = [];
    $('#constraint_conditions option').each(function() {
        //alert($(this).val())
        option_values.push($(this).val());
    });    
        
    for (i = 0; i < option_values.length; i++) { 
        if (option_values[i] == value) {
            alert('Error: ' + value + ' already exists');
            $("#constraint_available_conditions").focus();
            return;
        }
    }

    var option = '<option value=' + value + '>' + value + '</option>';
    $("#constraint_conditions").append(option);
    
    $("#remove_constraint_condition").prop('disabled', false);

/*
    var option_values = [];
    $('#condition_list2 option').each(function() {
        option_values.push($(this).val());
    });    
        
    for (i = 0; i < option_values.length; i++) { 
        if (option_values[i] == value.split(' ').join('_')) {
            alert('Error: ' + value.split(' ').join('_') + ' already exists');
            $( "#condition_input2" ).focus();
            return;
        }
    }

    // add to list
    var option = '<option value=' + value.split(' ').join('_') + '>' + value + '</option>';
    $("#condition_list2").append(option);

    // clear input value
    $('#condition_input2').val('');
    $("#remove_condition2").prop('disabled', false);
*/
    return;
});

$("#remove_constraint_condition").click(function(e){
 
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
    

function delete_obstacle(id) {
    
    // fade out then remove
    $('#obstacle-' + id).fadeOut('slow', function(){ $(this).remove(); });    

    $.ajax({
        method: "POST",
        url: url_delete_obstacle,
        dataType: "json",
        data: {obstacle_id: id},
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

function edit_obstacle(id) {

    mode = 2; // edit
    
    // get existing data and populate dialog
    $.ajax({
        method: "GET",
        url: url_edit_obstacle,
        dataType: "json",
        data: {obstacle_id: id},
    }).done(function( msg ) {

        // reset all fields
        $('#obstacle_id').val('');
        $('#obstacle_name').val('');
        $('#obstacle_type_label').text('Avoid');
        $('#condition_input2').val('');
        $('#condition_list2').find('option').remove();
        
        var obstacle_name = msg['name'];
        var obstacle_type = msg['type'];
        var conditions = msg['conditions'];

        // set input values
        $('#obstacle_id').val(id); //hidden
        $('#obstacle_name').val(obstacle_name);
        $('#obstacle_type_label').text(obstacle_type);

        var value = ''
        for (var i = 0; i < conditions.length; i++) {
            value = conditions[i];
            var option = '<option value=' + value.split(' ').join('_') + '>' + value + '</option>';
            $("#condition_list2").append(option);
        }        

        if (conditions.length) {
            $("#remove_condition2").prop('disabled', false);
        } else {
            $("#remove_condition2").prop('disabled', true);
        }
        
        $('#obstacle_modal').modal('show');
                
    }).fail(function() {
        alert( "Error - Edit obstacle failed." );
  });    
    
}

function Constraint(id, name, conditions, mode) {
    this.id = id;
    this.name = name;
    this.conditions = conditions;
    this.mode = mode;
    this.object_type = OBJECT_TYPE_CONTEXT_CONSTRAINT;
}
