/*
It depends on the context, but in most cases it is different. And usually one implies the other.
If a user clicks on "Edit" , he/she can change the values, but the Update is not performed until they click on "Save". In 99% of the cases , a user who edits a record will want to update it...
*  * */
 
// Handler for .ready() called.
$(function() {
    
    
    // set modal title for obstacle dialog
    $('#constraint_modal').on('show.bs.modal', function(e) {
        
        if (mode == 1) {
            $('#constraint_modal_title').text("Create New Context Constraint"); 
        } else {
            $('#constraint_modal_title').text("Edit Context Constraint");   
        }
    })
    
    $( '#save_constraint_btn' ).click(function() {
        // validate all fields
        
        // used for edit
        alert('mode is ' + mode);
        
        var id = $('#constraint_id').val();
        alert(id)
        var name = $('#constraint_name').val().split(' ').join('_');

        if (!name) {
            alert('Error: constraint name cannot be empty.');
            $('#constraint_name').focus();
            $('#constraint_name').flash();
            return;
        }
        
        var conditions = [];
        $('#constraint_conditions option').each(function() {
            conditions.push($(this).val().split(' ').join('_'));
        });    

        // create data
        var constraint_data = new Constraint(id, name, conditions, mode);
        
        alert('a')
        // post data
        $.ajax({
            method: "POST",
            url: url_dashboard,
            dataType: "json",
            data: constraint_data
        }).done(function( msg ) {
            
            var obstacle_name = msg['constraint_name'];
            var created = msg['created'];
            created = (created === "true");
            
            if (created) {
                $('#constraint_modal').modal('toggle');
            } else {    // created is false
                
                // create new mode
                if (mode == 1) {
                    alert('Error - failed to create constraint: '+ constraint_name);
                } else {
                    $('#constraint_modal').modal('toggle');
                }
            }
            location.reload();            
        });    
    });    

});

// constraint
$( '#create_constraint_btn' ).click(function() {

    // set to new mode
    mode = MODE_CREATE;
    
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
});

$("#add_constraint_condition").click(function(e){
    
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
    

function delete_constraint(id) {
    
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
        alert('done');
        // reset all fields
        $('#constraint_id').val('');
        $('#constraint_name').val('');
        $('#constraint_available_conditions').find('option').remove();
        $('#constraint_conditions').find('option').remove();
        alert('aaaaaa')
        
        var constraint_name = msg['name'];
        alert('d')
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

function Constraint(id, name, conditions, mode) {
    
    if (mode == MODE_UPDATE) {
        this.id = id;    
    }
    
    this.name = name;
    this.conditions = conditions;
    this.mode = mode;
    this.object_type = OBJECT_TYPE_CONTEXT_CONSTRAINT;
}
