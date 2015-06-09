    
// Handler for .ready() called.
$(function() {
    
    
    // set modal title for obstacle dialog
    $('#obstacle_modal').on('show.bs.modal', function(e) {
        alert(mode);
        if (mode == 1) {
            $('#obstacle_modal_title').text("Create New Obstacle"); 
        } else {
            $('#obstacle_modal_title').text("Edit Obstacle");   
        }
    })
    
$( '#save_obstacle_btn' ).click(function() {
    // validate all fields
    var id = $('#obstacle_id').val();
    var name = $('#obstacle_name').val().split(' ').join('_');

    if (!name) {
        alert('Error: obstacle name cannot be empty.');
        $("#obstacle_name").focus();
        $( '#obstacle_name' ).flash();
        return;
    }
    
    var type = $('#obstacle_type_label').text();

    var conditions = [];
    $('#condition_list2 option').each(function() {
        conditions.push($(this).val().split(' ').join('_'));
    });    

    // create data
    var obstacle_data = new Obstacle(id, name, type, conditions, mode);

    // post data
    $.ajax({
        method: "POST",
        url: dashboard_url,
        dataType: "json",
        data: obstacle_data
    }).done(function( msg ) {
        
        var obstacle_name = msg['obstacle_name'];
        var created = msg['created'];
        //alert('created i s '+ created);
        created = (created === "true");
        
        if (created) {
            $('#obstacle_modal').modal('toggle');
            location.reload();            
        } else {    // created is false
            
            // create new mode
            if (mode == 1) {
                alert('Error - failed to create obstacle: '+ obstacle_name);
            } else {
                $('#obstacle_modal').modal('toggle');
            }
        }
    });    
});    

});

// obstacle
$( '#create_obstacle_btn' ).click(function() {

    // set to new mode
    mode = 1;
    
    // reset all fields
    $('#obstacle_name').val('');
    $('#condition_input2').val('');
    $('#condition_list2').find('option').remove();
});




function Obstacle(id, name, type, conditions, mode) {
    this.id = id;
    this.name = name;
    this.type = type;
    this.conditions = conditions;
    this.mode = mode;
    this.object_type = OBJECT_TYPE_OBSTACLE;
    alert(this.object_type);

}

$("#add_condition2").click(function(e){
    
    var value = $('#condition_input2').val();
    
    if (!$.trim(value)) {
        // error
        alert('Error: condition value cannot be empty.');
        $( "#condition_input2" ).focus();
        return;
    }

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

    return;
});

$("#remove_condition2").click(function(e){
 
    var value = $('#condition_list2').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    var selector = "#condition_list2 option[value='" + value + "']";
    $(selector).remove();
    
    var size = $('#condition_list2 option').size()
    if (!size) {
        $("#remove_condition2").prop('disabled', true);
    }

    return;
});
    

function delete_obstacle(id) {
    
    $('#obstacle-' + id).hide(1000);
    
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

function edit_obstacle(id) {

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
