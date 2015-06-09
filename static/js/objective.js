    
// Handler for .ready() called.
$(function() {
    
    // set modal title for objective dialog
    $('#objective_modal').on('show.bs.modal', function(e) {
        alert(mode);
        if (mode == 1) {
            $('#objective_modal_title').text("Create New Objective"); 
        } else {
            $('#obstacle_modal_title').text("Edit Objective");   
        }
    })

});

// objective
$( '#create_objective_btn' ).click(function() {

    // set to new mode
    mode = 1;
    
    // reset all fields
    $('#objective_name').val('');
    $('#objective_type_label').text('Select');
    $('#condition_input').val('');
    $('#condition_list').find('option').remove();
});

$( '#save_objective_btn' ).click(function() {
    
    // validate all fields
    var id = $('#objective_id').val();
    var name = $('#objective_name').val().split(' ').join('_');

    if (!name) {
        alert('Error: objective name cannot be empty.');
        $("#objective_name").focus();
        $( '#objective_name' ).flash();
        return;
    }
    
    var type = $('#objective_type_label').text();
    if (type == 'Select') {
        alert('Error: objective type not selected.');
        flash("#dropdown_objective_type");
        return;    
    }

    var conditions = [];
    $('#condition_list option').each(function() {
        conditions.push($(this).val().split(' ').join('_'));
    });    

    // create data
    var objective_data = new Objective(id, name, type, conditions, mode);

    // post data
    $.ajax({
        method: "POST",
        url: dashboard_url,
        dataType: "json",
        data: objective_data
    }).done(function( msg ) {
        
        var objective_name = msg['objective_name'];
        var created = msg['created'];
        //alert(created);
        
        created = (created === "true");
        
        if (created) {
            $('#objective_modal').modal('toggle');
            location.reload();            
        } else {    // created is false
            
            // create new mode
            if (mode == 1) {
                alert('Error - failed to create objective: '+ objective_name);
            } else {
                $('#objective_modal').modal('toggle');
            }
        }
    });    
});

function Objective(id, name, type, conditions, mode) {
    this.id = id;
    this.name = name;
    this.type = type;
    this.conditions = conditions;
    this.mode = mode;
    this.object_type = OBJECT_TYPE_OBJECTIVE;
}

$("#action-1").click(function(e){
    change_select_label(e);
});

$("#action-2").click(function(e){
    change_select_label(e);
});

$("#action-3").click(function(e){
    change_select_label(e);
});

$("#action-4").click(function(e){
    change_select_label(e);
});

$("#action-5").click(function(e){
    change_select_label(e);
});

$("#action-6").click(function(e){
    change_select_label(e);
});

$("#action-7").click(function(e){
    change_select_label(e);
});

$("#action-8").click(function(e){
    change_select_label(e);
});

$("#action-9").click(function(e){
    change_select_label(e);
});

$("#action-10").click(function(e){
    change_select_label(e);
});


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
    
    $('#objective-' + id).hide(1000);
    
    $.ajax({
        method: "POST",
        url: "{% url 'delete_objective' %}",
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
        url: "{% url 'edit_objective' %}",
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
