//=====================================================================>
// Scenario section
//

function Edit_Scenario_init(name) {

    $('#scenario_modal_title').text("Edit Scenario"); 
    
    $('#edit_scenario_name').val(name);
    $('#scenario_name').val(name);
    $('#step_list').find('option').remove();
    $("#add_selected_step").prop('disabled', true);

    clear_graph();
    init_graph();
    
    // get step list
    $.ajax({
        method: "GET",
        url: url_get_step_list,
    }).done(function(data) {
        
        var step_list = data['step_list'];
        
        var value = ''
        for (var i = 0; i < step_list.length; i++) {
            value = step_list[i];
            var option = '<option value=' + value + '>' + value + '</option>';
            $("#step_list").append(option);
        }
             
        if (step_list.length) {
            $("#add_selected_step").prop('disabled', false);
        } else {
            $("#add_selected_step").prop('disabled', true);
        }
                                
    }).fail(function() {
        alert( "Error - Create_Scenario_init failed." );
    });

    $("#cancel_scenario").show()
    $("#create_scenario").hide(); 
    $("#save_scenario").show(); 
 
    // get existing data and populate dialog
    $.ajax({
        method: "GET",
        url: url_edit_scenario_init,
        dataType: "json",
        data: {name: name},
    }).done(function(data) {
        
        var num = network.getViewPosition();
        var graph_dot = data['graph_dot'];
        var steps = data['steps'];
                        
        // import DOT into graph
        var parsedData = vis.network.convertDot(graph_dot);
        var x_pos = $('#scenario_modal').width()/5;
        var options1 = {};
        
        for (var i = 0; i < parsedData.nodes.length; i++) { 
            
            nodes.add({id: parsedData.nodes[i].id, label:parsedData.nodes[i].label, physics: false, x: x_pos, y:(nodeIds.length*50) + 50});
            nodeIds.push(parsedData.nodes[i].id);
        }
        
        for (var i = 0; i < parsedData.edges.length; i++) {
            edges.add(parsedData.edges[i]);
        }

        // default to select mode
        $('#graph_select_mode').click();    

        // show scenario modal
        $('#scenario_modal').modal('toggle');  
        
    }).fail(function() {
        alert( "Error - Edit scenario failed." );
  });    
}

function Edit_Scenario_save() {

    var name = $('#scenario_name').val().split(' ').join('_');

    if (!name) {
        alert('Error: scenario name cannot be empty.');
        $('#scenario_name').focus();
        $('#scenario_name').flash();
        return;
    }

    // get step graph in DOT notation
    var graph_dot = '';
    graph_dot = 'graph {'
    
    var all_edges = edges.get(); 
    
    var i;
    var edge;
    
    for (var i = 0; i < all_edges.length; i++) { 
        edge = all_edges[i];

        if (i == all_edges.length - 1) {
            graph_dot = graph_dot + String(edge['from']) + '->' + String(edge['to']);
        } else {
            graph_dot = graph_dot + String(edge['from']) + '->' + String(edge['to']) + ';';
        }
    }
    graph_dot = graph_dot + '}';

    var id = $('#edit_scenario_name').val();
    
    // post data
    $.ajax({
        method: "POST",
        url: url_edit_scenario_save,
        dataType: "json",
        data: {id:id, name:name, graph_dot:graph_dot}
    }).done(function( data ) {

    }); 

    $('#scenario_modal').modal('toggle');
    location.reload();           
}

$("#save_scenario").click(function(e){
    Edit_Scenario_save();
});

//<
//< End of Scenario section
//<=====================================================================


function Edit_CCCondMgmt_init(name) {
    
    $('#CC_modal_title').text("Context Constraint Condition Management"); 
    
    // reset all fields
    $('#CC_name').val(name);
    $('#CC_name').prop('disabled', true);
    $('#CC_available_conditions').find('option').remove();
    $('#CC_conditions').find('option').remove();
    
    // get condition list
    $.ajax({
        method: "GET",
        url: url_get_condition_list,
        dataType: "json",
    }).done(function(data) {
        
        var condition_list = data['condition_list'];

        var value = ''
        for (var i = 0; i < condition_list.length; i++) {
            value = condition_list[i];
            var option = '<option value=' + value.split(' ').join('_') + '>' + value + '</option>';
            $("#CC_available_conditions").append(option);
        }        

        if (condition_list.length) {
            $("#CC_unlinkbutton").prop('disabled', false);
        } else {
            $("#CC_unlinkbutton").prop('disabled', true);
        }
        
        $('#CC_modal').modal('show');
                
    }).fail(function() {
        alert( "Error - create context constraint failed." );
    });    
    
    // get all conditions
    $.ajax({
        method: "GET",
        url: url_get_all_conditions,
        dataType: "json",
        data: {name:name}
    }).done(function(data) {
        
        var condition_list = data['condition_list'];

        var value = ''
        for (var i = 0; i < condition_list.length; i++) {
            value = condition_list[i];
            var option = '<option value=' + value.split(' ').join('_') + '>' + value + '</option>';
            $("#CC_conditions").append(option);
        }        

        if (condition_list.length) {
            $("#CC_unlinkbutton").prop('disabled', false);
        } else {
            $("#CC_unlinkbutton").prop('disabled', true);
        }
        
        $('#CC_modal').modal('show');
                
    }).fail(function() {
        alert( "Error - create context constraint failed." );
    });    
    
    $("#cancel_CC").hide();
    $("#save_CC").hide();
    $("#create_CC").hide();
    
    $("#CC_add_condition").hide();
    $("#CC_remove_condition").hide();

    $("#CC_linkbutton").show();
    $("#CC_unlinkbutton").show();
    
    $("#close_CC").show();
    
    $('#CC_modal').modal('toggle');
    
}

function Edit_CCCondMgmt_linkCondition() {
    
    var name = $('#CC_name').val();
    var value = $('#CC_available_conditions').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    var option_values = [];
    $('#CC_conditions option').each(function() {
        option_values.push($(this).val());
    });    
        
    for (i = 0; i < option_values.length; i++) { 
        if (option_values[i] == value) {
            alert('Error: ' + value + ' already exists');
            $("#CC_available_conditions").focus();
            return;
        }
    }

    // all good - add condition
    var option = '<option value=' + value + '>' + value + '</option>';
    $("#CC_conditions").append(option);
    
    $("#CC_unlinkbutton").prop('disabled', false);

    // link condition to context constraint
    var condition = String(value);
        
    // api call
    $.ajax({
        method: "POST",
        url: url_link_condition_to_context_constraint,
        dataType: "json",
        data: {condition:condition, name:name}
    }).done(function(data) {
        
    });
    
    return;
}

function Edit_CCCondMgmt_unlinkCondition() {
    
    var name = $('#CC_name').val();
    var value = $('#CC_conditions').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    var selector = "#CC_conditions option[value='" + value + "']";
    $(selector).remove();
    
    var size = $('#CC_conditions option').size()
    
    if (!size) {
        $("#CC_unlinkbutton").prop('disabled', true);
    }

    // unlink condition from context constraint
    var condition = String(value);
        
    // api call
    $.ajax({
        method: "POST",
        url: url_unlink_condition_from_context_constraint,
        dataType: "json",
        data: {condition:condition, name:name}
    }).done(function(data) {
        
    });
    
    return;
}

$("#CC_linkbutton").click(function(e){
    Edit_CCCondMgmt_linkCondition();
});

$("#CC_unlinkbutton").click(function(e){
    Edit_CCCondMgmt_unlinkCondition();
});
    
function Edit_Objective_init(name) {
    $('#objective_modal_title').text("Edit control objective"); 
    
    // get existing data and populate dialog
    $.ajax({
        method: "GET",
        url: url_edit_objective_init,
        dataType: "json",
        data: {objective_name: name},
    }).done(function(data) {

        // reset all fields
        $('#objective_name').val(name);
        $('#objective_type').text('Select');
        $('#objective_abstract_context_condition_entry').val('');
        $('#objective_abstract_context_condition_list').find('option').remove();    
        
        var objective_name = name;
        var objective_type = data['type'];
        var objective_id = data['id'];
        
        var objective_abstract_context_condition_list = data['abstract_context_condition_list'];

        // set input values
        $('#objective_id').val(objective_id);
        $('#objective_name').val(objective_name);
        $('#objective_type').text(objective_type);

        var value = ''
        for (var i = 0; i < objective_abstract_context_condition_list.length; i++) {
            value = objective_abstract_context_condition_list[i];
            var option = '<option value=' + value.split(' ').join('_') + '>' + value + '</option>';
            $("#objective_abstract_context_condition_list").append(option);
        }        

        if (objective_abstract_context_condition_list.length) {
            $("#objective_remove_condition").prop('disabled', false);
        } else {
            $("#objective_remove_condition").prop('disabled', true);
        }
        
        $('#objective_modal').modal('show');
                
    }).fail(function() {
        alert( "Error - Edit objective failed." );
    });    
    
    $("#create_objective").hide()
    $("#save_objective").show()
}

function Edit_Objective_save() {

    // validate all fields
    var name = $('#objective_name').val().split(' ').join('_');
    //var id = $('#objective_id').val();

    if (!name) {
        alert('Error: objective name cannot be empty.');
        $("#objective_name").focus();
        $( '#objective_name' ).flash();
        return;
    }
    
    var type = $('#objective_type').text();
    if (type == 'Select') {
        alert('Error: objective type not selected.');
        flash("#dropdown_objective_type");
        return;    
    }
    
    // api call
    $.ajax({
        method: "POST",
        url: url_edit_objective_save,
        dataType: "json",
        data: {id:id, name:name, type:type}
    }).done(function(data) {
    });
    
    // api call
    $.ajax({
        method: "POST",
        url: url_clear_derived_condition_list_of_objective,
        dataType: "json",
        data: {name:name}
    }).done(function(data) {
        
    });
      
    var abstract_context_conditions = [];
    var abstract_context_condition = '';
    
    $('#objective_abstract_context_condition_list option').each(function() {
        abstract_context_condition = $(this).val().split(' ').join('_');
        
        // api call
        $.ajax({
            method: "POST",
            url: url_add_derived_abstract_context_condition_to_objective,
            dataType: "json",
            data: {abstract_context_condition:abstract_context_condition, objective_name:name}
        }).done(function(data) {
            
        });
    });

    $('#objective_modal').modal('toggle');
    location.reload();            
}

$("#save_objective").click(function(e){
    Edit_Objective_save();
});



//=======================================================

function Edit_Obstacle_init(name) {
    
    $('#obstacle_modal_title').text("Edit Obstacle"); 
    
    // get existing data and populate dialog
    $.ajax({
        method: "GET",
        url: url_edit_obstacle_init,
        dataType: "json",
        data: {name: name},
    }).done(function(data) {

        // reset all fields
        $('#obstacle_name').val(name);
        $('#obstacle_type').text('Avoid');
        $('#obstacle_abstract_context_condition_entry').val('');
        $('#objective_abstract_context_condition_list').find('option').remove();    
        
        var obstacle_name = name;
        var obstacle_type = data['type'];
        var obstacle_id = data['id'];
        
        var obstacle_abstract_context_condition_list = data['abstract_context_condition_list'];

        // set input values
        $('#obstacle_id').val(obstacle_id);
        $('#obstacle_name').val(obstacle_name);
        $('#obstacle_type').text(obstacle_type);

        var value = ''
        for (var i = 0; i < obstacle_abstract_context_condition_list.length; i++) {
            value = obstacle_abstract_context_condition_list[i];
            var option = '<option value=' + value.split(' ').join('_') + '>' + value + '</option>';
            $("#obstacle_abstract_context_condition_list").append(option);
        }        

        if (obstacle_abstract_context_condition_list.length) {
            $("#obstacle_remove_condition").prop('disabled', false);
        } else {
            $("#obstacle_remove_condition").prop('disabled', true);
        }
        
        $('#obstacle_modal').modal('show');
                
    }).fail(function() {
        alert( "Error - Edit obstacle failed." );
    });    
    
    $("#create_obstacle").hide()
    $("#save_obstacle").show()
}

function Edit_Obstacle_save() {

    // validate all fields
    var name = $('#obstacle_name').val().split(' ').join('_');
    var id = $('#obstacle_id').val();

    if (!name) {
        alert('Error: obstacle name cannot be empty.');
        $("#obstacle_name").focus();
        $( '#obstacle_name' ).flash();
        return;
    }
    
    var type = $('#obstacle_type').text();
    if (type == 'Select') {
        alert('Error: obstacle type not selected.');
        flash("#dropdown_objective_type");
        return;    
    }
    
    // api call
    $.ajax({
        method: "POST",
        url: url_edit_obstacle_save,
        dataType: "json",
        data: {id:id, name:name, type:type}
    }).done(function(data) {
    });
    
    // api call
    $.ajax({
        method: "POST",
        url: url_clear_derived_condition_list_of_obstacle,
        dataType: "json",
        data: {name:name}
    }).done(function(data) {
        
    });
      
    var abstract_context_conditions = [];
    var abstract_context_condition = '';
    
    $('#obstacle_abstract_context_condition_list option').each(function() {
        abstract_context_condition = $(this).val().split(' ').join('_');
        
        // api call
        $.ajax({
            method: "POST",
            url: url_add_derived_abstract_context_condition_to_obstacle,
            dataType: "json",
            data: {abstract_context_condition:abstract_context_condition, name:name}
        }).done(function(data) {
            
        });
    });

    $('#obstacle_modal').modal('toggle');
    location.reload();            
}

$("#save_obstacle").click(function(e){
    Edit_Obstacle_save();
});


//======================================================================
//
//======================================================================

function Edit_Step_init(name) {
    
    $('#step_modal_title').text("Edit Step"); 
    
    // get existing data and populate modal
    $.ajax({
        method: "GET",
        url: url_edit_step_init,
        dataType: "json",
        data: {name: name},
    }).done(function(data) {

        // reset all fields
        $('#step_actor').val('');
        $('#step_action').val('');
        $('#step_target').val('');

        var actor = data['actor'];
        var action = data['action'];
        var target = data['target'];
        

        // set input values
        $('#step_name').val(name);
        $('#step_actor').val(actor);
        $('#step_action').val(action);
        $('#step_target').val(target);
        
        $('#step_modal').modal('show');
                
    }).fail(function() {
        alert( "Error - Edit step failed." );
    });    

    $("#close_step").hide()    
    $("#create_step").hide()
    $("#save_step").show()
}

function Edit_Step_save() {
   
   var name = $('#step_name').val(); 
   
   var actor = $('#step_actor').val().split(' ').join('_');

    if (!actor) {
        alert('Error: step actor cannot be empty.');
        $('#step_actor').focus();
        $('#step_actor').flash();
        return;
    }

    var action = $('#step_action').val().split(' ').join('_');

    if (!action) {
        alert('Error: step action cannot be empty.');
        $('#step_action').focus();
        $('#step_action').flash();
        return;
    }

    var target = $('#step_target').val().split(' ').join('_');

    if (!target) {
        alert('Error: step target cannot be empty.');
        $('#step_target').focus();
        $('#step_target').flash();
        return;
    }
    
    $.ajax({
        method: "POST",
        url: url_edit_step_save,
        dataType: "json",
        data: {name:name, actor:actor, action:action, target:target}
    }).done(function(data) {

    }); 

    $('#step_modal').modal('toggle');
    location.reload();           
}

$("#save_step").click(function(e){
    Edit_Step_save();
});

//======================================================================
// PermCard
//======================================================================
function Edit_PermCard_init(name) {
        
    // get existing data and populate modal
    $.ajax({
        method: "GET",
        url: url_edit_permcard_init,
        dataType: "json",
        data: {name: name},
    }).done(function(data) {

        // reset all fields
        $('#perm_card_for_perm_name').val('');
        $('#perm_card_mincardinality').val('');
        $('#perm_card_maxcardinality').val('');

        var mincardinality = data['mincardinality'];
        var maxcardinality = data['maxcardinality'];
        
        // set input values
        $('#perm_card_for_perm_name').val(name);
        $('#perm_card_mincardinality').val(mincardinality);
        $('#perm_card_maxcardinality').val(maxcardinality);
        
        $('#permcard_modal').modal('toggle');
                
    }).fail(function() {
        alert( "Error - Edit PermCard failed." );
    });    
    
    $("#cancel_permcard").show()
    $("#save_permcard").show()
}

function Edit_PermCard_save() {
    
    var name = $('#perm_card_for_perm_name').val();
    var min = $('#perm_card_mincardinality').val();
    var max = $('#perm_card_maxcardinality').val();
    
    if ((min < -1) || (max < -1)) {
        alert('min max cardinality cannot be less that 0.')
    }
    
    // get existing data and populate modal
    $.ajax({
        method: "POST",
        url: url_edit_permcard_save,
        dataType: "json",
        data: {name:name, min:min, max:max},
    }).done(function(data) {
        $('#permcard_modal').modal('toggle');
        location.reload();           

    }).fail(function() {
        alert( "Error - Edit_PermCard_save failed." );
    });        
}

$("#save_permcard").click(function(e){
    Edit_PermCard_save();
});


//======================================================================
// Profile section
//======================================================================
function Edit_Profile_init(name) {
    
    $('#profile_modal_title').text("Edit work profile"); 

    // reset all fields
    $('#profile_name').val('');
    $('#task_list').find('option').remove();
    $('#tasks').find('option').remove();

    // get task list
    $.ajax({
        method: "GET",
        url: url_get_task_list,
        dataType: "json",
    }).done(function(data) {
        
        var task_list = data['task_list'];

        var value = ''
        for (var i = 0; i < task_list.length; i++) {
            value = task_list[i];
            var option = '<option value=' + value.split(' ').join('_') + '>' + value + '</option>';
            $("#task_list").append(option);
        }        
                
    }).fail(function() {
        alert( "Error - Edit_Profile_init failed." );
    });    
    
    // get existing data and populate dialog
    $.ajax({
        method: "GET",
        url: url_edit_profile_init,
        dataType: "json",
        data: {name: name},
    }).done(function(data) {
        
        var tasks = data['tasks'];

        // set input values
        $('#profile_name').val(name);

        var value = ''
        for (var i = 0; i < tasks.length; i++) {
            value = tasks[i];
            var option = '<option value=' + value.split(' ').join('_') + '>' + value + '</option>';
            $("#tasks").append(option);
        }        

        if (tasks.length) {
            $("#profile_remove_task").prop('disabled', false);
        } else {
            $("#profile_remove_task").prop('disabled', true);
        }
        
        $('#profile_modal').modal('show');
                
    }).fail(function() {
        alert( "Error - Edit_Profile_init failed." );
    });    
    
    $("#create_profile").hide()
    $("#close_profile").hide()
    $("#save_profile").show()
}

function Edit_Profile_save() {
    
    // validate all fields
    var name = $('#profile_name').val();

    if (!name) {
        alert('Error: work profile name cannot be empty.');
        $("#profile_name").focus();
        $( '#profile_name' ).flash();
        return;
    }
        
    // api call
    $.ajax({
        method: "POST",
        url: url_edit_profile_save,
        dataType: "json",
        data: {name:name}
    }).done(function(data) {
    });
    
    // api call
    $.ajax({
        method: "POST",
        url: url_clear_task_list_of_work_profile,
        dataType: "json",
        data: {name:name}
    }).done(function(data) {
        
    });

    var tasks = [];
    var task = '';
    
    $('#tasks option').each(function() {
        tasks.push($(this).val().split(' ').join('_'));
    });    

    $.ajax({
        method: "POST",
        url: url_add_tasks_to_work_profile,
        dataType: "json",
        data: {tasks:tasks, name:name}
    }).done(function(data) {

    });
          
    $('#profile_modal').modal('toggle');
    location.reload();            
}

$("#save_profile").click(function(e){
    Edit_Profile_save();
});

//======================================================================
// Task section
//======================================================================
function Edit_Task_init(name) {
    
    $('#task_modal_title').text("Edit task"); 

    // reset all fields
    $('#task_name').val('');
    $('#task_list').find('option').remove();
    $('#tasks').find('option').remove();

    // get task list
    $.ajax({
        method: "GET",
        url: url_get_scenario_list,
        dataType: "json",
    }).done(function(data) {
        
        var scenario_list = data['scenario_list'];

        var value = ''
        for (var i = 0; i < scenario_list.length; i++) {
            value = scenario_list[i];
            var option = '<option value=' + value.split(' ').join('_') + '>' + value + '</option>';
            $("#scenario_list").append(option);
        }        
                
    }).fail(function() {
        alert( "Error - Edit_Task_init failed." );
    });    
    
    // get existing data and populate dialog
    $.ajax({
        method: "GET",
        url: url_edit_task_init,
        dataType: "json",
        data: {name: name},
    }).done(function(data) {
        
        var scenarios = data['scenarios'];

        // set input values
        $('#task_name').val(name);

        var value = ''
        for (var i = 0; i < scenarios.length; i++) {
            value = scenarios[i];
            var option = '<option value=' + value + '>' + value + '</option>';
            $("#scenarios").append(option);
        }        

        if (tasks.length) {
            $("#remove_scenario").prop('disabled', false);
        } else {
            $("#remove_scenario").prop('disabled', true);
        }
        
        $('#task_modal').modal('show');
                
    }).fail(function() {
        alert( "Error - Edit_Task_init failed." );
    });    
    
    $("#create_task").hide()
    $("#close_task").hide()
    $("#save_task").show()
}

function Edit_Task_save() {
    
    // validate all fields
    var name = $('#task_name').val();

    if (!name) {
        alert('Error: task name cannot be empty.');
        $("#task_name").focus();
        $( '#task_name' ).flash();
        return;
    }
        
    // api call
    $.ajax({
        method: "POST",
        url: url_edit_task_save,
        dataType: "json",
        data: {name:name}
    }).done(function(data) {
    });
    
    // api call
    $.ajax({
        method: "POST",
        url: url_clear_scenario_list_of_task,
        dataType: "json",
        data: {name:name}
    }).done(function(data) {
        
    });
      
    var scenarios = [];
    var scenario = '';
    
    $('#scenarios option').each(function() {
        scenario.push($(this).val().split(' ').join('_'));
    });    

    $.ajax({
        method: "POST",
        url: url_add_scenarios_to_task,
        dataType: "json",
        data: {scenarios:scenarios, name:name}
    }).done(function(data) {

    });

    $('#profile_modal').modal('toggle');
    location.reload();            
}

$("#save_profile").click(function(e){
    Edit_Profile_save();m
});

//======================================================================
// PermCCMgmt
//======================================================================
function Edit_PermCCMgmt_init(name) {
        
    // reset all fields
    $('#CC_mgmt_for_perm').val(name);
    $('#CC_mgmt_for_perm').prop('disabled', true);
    $('#cclist').find('option').remove();
    $('#ccs').find('option').remove();
    
    // get_context_constraint_list
    $.ajax({
        method: "GET",
        url: url_get_context_constraint_list,
        dataType: "json",
    }).done(function(data) {
        
        var cclist = data['cclist'];

        var value = ''
        for (var i = 0; i < cclist.length; i++) {
            value = cclist[i];
            var option = '<option value=' + value + '>' + value + '</option>';
            $("#cclist").append(option);
        }        

        if (cclist.length) {
            $("#unlink_constraint").prop('disabled', false);
        } else {
            $("#unlink_constraint").prop('disabled', true);
        }
    }).fail(function() {
        alert( "Error - Edit_PermCCMgmt_init - url_get_context_constraint_list failed." );
    });    
    
    // get context constraints for this permission (e.g. name)
    $.ajax({
        method: "GET",
        url: url_get_context_constraints,
        dataType: "json",
        data: {name:name}
    }).done(function(data) {
        
        var ccs = data['ccs'];

        var value = ''
        for (var i = 0; i < ccs.length; i++) {
            value = ccs[i];
            var option = '<option value=' + value + '>' + value + '</option>';
            $("#ccs").append(option);
        }        

        if (ccs.length) {
            $("#unlink_constraint").prop('disabled', false);
        } else {
            $("#unlink_constraint").prop('disabled', true);
        }
        
        $('#perm_CC_mgmt_modal').modal('show');
                
    }).fail(function() {
        alert( "Error - Edit_PermCCMgmt_init - url_get_context_constraints failed." );
    });    
        
    $('#perm_CC_mgmt_modal').modal('show');
}

function Edit_PermCCMgmt_linkConstraint() {
    
    var value = $('#cclist').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    var option_values = [];
    $('#ccs option').each(function() {
        option_values.push($(this).val());
    });    
        
    for (i = 0; i < option_values.length; i++) { 
        if (option_values[i] == value) {
            alert('Error: ' + value + ' already exists');
            $("#cclist").focus();
            return;
        }
    }

    var option = '<option value=' + value + '>' + value + '</option>';
    $("#ccs").append(option);
    
    $("#unlink_constraint").prop('disabled', false);
    return;
}

function Edit_PermCCMgmt_unlinkConstraint() {
    
    var value = $('#ccs').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    var selector = "#ccs option[value='" + value + "']";
    $(selector).remove();
    
    var size = $('#ccs option').size()
    
    if (!size) {
        $("#unlink_constraint").prop('disabled', true);
    }

    return;
}

function Edit_PermCCMgmt_save() {
    
    // validate all fields
    var name = $('#CC_mgmt_for_perm').val();
    
    // api call
    $.ajax({
        method: "POST",
        url: url_unlink_context_constraints_from_perm,
        dataType: "json",
        data: {name:name}
    }).done(function(data) {
        
    });
      
    var ccs = [];
    var cc = '';
    
    $('#ccs option').each(function() {
        ccs.push($(this).val().split(' ').join('_'));
    });    

    $.ajax({
        method: "POST",
        url: url_link_context_constraints_to_perm,
        dataType: "json",
        data: {ccs:ccs, name:name}
    }).done(function(data) {

    });

    $('#perm_CC_mgmt_modal').modal('toggle');
    location.reload();            
}

$("#save_perm_CC_mgmt").click(function(e){
    Edit_PermCCMgmt_save();
});

$("#link_constraint").click(function(e){
    Edit_PermCCMgmt_linkConstraint();
});

$("#unlink_constraint").click(function(e){
    Edit_PermCCMgmt_unlinkConstraint();
});

//======================================================================
// SSDPerm section
//======================================================================
function Edit_SSDPerm_init(name) {
        
    // reset all fields
    $('#SSD_for_perm').val(name);
    $('#SSD_for_perm').prop('disabled', true);
    $('#perm_list').find('option').remove();
    $('#dmeps').find('option').remove();
    
    // get_permission_list
    $.ajax({
        method: "GET",
        url: url_get_permission_list,
        dataType: "json",
    }).done(function(data) {
        
        var perm_list = data['perm_list'];

        var value = ''
        for (var i = 0; i < perm_list.length; i++) {
            value = perm_list[i];
            var option = '<option value=' + value + '>' + value + '</option>';
            $("#perm_list").append(option);
        }        

        if (perm_list.length) {
            $("#unset_constraint").prop('disabled', false);
        } else {
            $("#unset_constraint").prop('disabled', true);
        }
    }).fail(function() {
        alert( "Error - Edit_SSDPerm_init - url_get_permission_list failed." );
    });    
    
    // get ssd context constraints for this permission (e.g. name: is the permission name)
    $.ajax({
        method: "GET",
        url: url_get_ssd_perm_constraints,
        dataType: "json",
        data: {name:name}
    }).done(function(data) {
        
        var dmeps= data['dmeps'];

        var value = ''
        for (var i = 0; i < dmeps.length; i++) {
            value = dmeps[i];
            var option = '<option value=' + value + '>' + value + '</option>';
            $("#dmeps").append(option);
        }        

        if (dmeps.length) {
            $("#unset_constraint").prop('disabled', false);
        } else {
            $("#unset_constraint").prop('disabled', true);
        }

        $('#ssd_perm_modal').modal('show');
                
    }).fail(function() {
        alert( "Error - Edit_SSDPerm_init - url_get_ssd_perm_constraints failed." );
    });    
}

function Edit_SSDPerm_setConstraint() {
    alert('12')
    var perm = $('#SSD_for_perm').val();
    var mutlexcl = $('#perm_list').val()[0];

    if (!mutlexcl) {
        alert('Error: no option selected');
        return;
    }
    
    if (perm == mutlexcl) {
        alert('Edit_SSDPerm_setConstraint for permission "' + perm + '", FAILED, a permission cannot be mutual exclusive to itself.');
        $('perm_list').focus();
        $('#perm_list').flash();
        return;
    }
    
    var option_values = [];
    $('#dmeps option').each(function() {
        option_values.push($(this).val());
    });    
        
    for (i = 0; i < option_values.length; i++) { 
        if (option_values[i] == mutlexcl) {
            alert('Error: ' + mutlexcl + ' already exists');
            $("#dmeps").focus();
            return;
        }
    }
    
    $.ajax({
        method: "POST",
        url: url_set_ssd_perm_constraint,
        dataType: "json",
        data: {perm:perm, mutlexcl:mutlexcl}
    }).done(function(data) {
        
    });
    
    var option = '<option value=' + mutlexcl + '>' + mutlexcl + '</option>';
    $("#dmeps").append(option);
    
    $("#unset_constraint").prop('disabled', false);
    return;
}

function Edit_SSDPerm_unsetConstraint() {
    
    var perm = $('#SSD_for_perm').val();
    var mutlexcl = $('#dmeps').val()[0];
        
    if (!mutlexcl) {
        alert('Error: no option selected');
        return;
    }
    
    var selector = "#dmeps option[value='" + mutlexcl + "']";
    $(selector).remove();
    
    var size = $('#dmeps option').size()
    
    if (!size) {
        $("#unset_constraint").prop('disabled', true);
    }

    $.ajax({
        method: "POST",
        url: url_unset_ssd_perm_constraint,
        dataType: "json",
        data: {perm:perm, mutlexcl:mutlexcl}
    }).done(function(data) {
        
    });

    return;
}

$("#perm_set_constraint").click(function(e) {
    alert('1')
    Edit_SSDPerm_setConstraint();
});

$("#perm_unset_constraint").click(function(e) {
    Edit_SSDPerm_unsetConstraint();
});


//======================================================================
// RoleCard
//======================================================================
function Edit_RoleCard_init(name) {
        
    // get existing data and populate modal
    $.ajax({
        method: "GET",
        url: url_edit_rolecard_init,
        dataType: "json",
        data: {name: name},
    }).done(function(data) {

        // reset all fields
        $('#rolecard_role').val('');
        $('#rolecard_mincardinality').val('');
        $('#rolecard_maxcardinality').val('');

        var mincardinality = data['mincardinality'];
        var maxcardinality = data['maxcardinality'];
        
        // set input values
        $('#rolecard_role').val(name);
        $('#rolecard_mincardinality').val(mincardinality);
        $('#rolecard_maxcardinality').val(maxcardinality);
        
        $('#rolecard_modal').modal('toggle');
                
    }).fail(function() {
        alert( "Error - Edit_RoleCard_init failed." );
    });    
    
    $("#save_rolecard").show()
}

function Edit_RoleCard_save() {
    
    var name = $('#rolecard_role').val();
    var min = $('#rolecard_mincardinality').val();
    var max = $('#rolecard_maxcardinality').val();
    
    // get existing data and populate modal
    $.ajax({
        method: "POST",
        url: url_edit_rolecard_save,
        dataType: "json",
        data: {name:name, min:min, max:max},
    }).done(function(data) {
        $('#rolecard_modal').modal('toggle');
        location.reload();           

    }).fail(function() {
        alert( "Error - Edit_RoleCard_save failed." );
    });        
}

$("#save_rolecard").click(function(e){
    Edit_RoleCard_save();
});
$("#rolecard_btn").click(function(e){
    Edit_RoleCard_init('');
});

//=====================================================================>
// SSDRole section
//=====================================================================>
function Edit_SSDRole_init(name) {
        
    // reset all fields
    $('#SSD_for_role').val(name);
    $('#SSD_for_role').prop('disabled', true);
    $('#ssd_role_role_list').find('option').remove();
    $('#dmer').find('option').remove();
    $('#tssdrc').find('option').remove();
    $('#issdc').find('option').remove();
    
    $.ajax({
        method: "GET",
        url: url_get_role_list,
        dataType: "json",
    }).done(function(data) {
        
        var role_list = data['role_list'];

        var value = ''
        for (var i = 0; i < role_list.length; i++) {
            value = role_list[i];
            var option = '<option value=' + value + '>' + value + '</option>';
            $("#ssd_role_role_list").append(option);
        }        

        if (role_list.length) {
            $("#role_unset_constraint").prop('disabled', false);
        } else {
            $("#role_unset_constraint").prop('disabled', true);
        }
    }).fail(function() {
        alert( "Error - Edit_SSDRole_init - url_get_role_list failed." );
    });
    
    $.ajax({
        method: "GET",
        url: url_get_direct_ssd_role_constraints,
        dataType: "json",
        data: {name:name},
    }).done(function(data) {
        
        var dmer = data['dmer'];

        var value = ''
        for (var i = 0; i < dmer.length; i++) {
            value = dmer[i];
            var option = '<option value=' + value + '>' + value + '</option>';
            $("#dmer").append(option);
        }        

        if (dmer.length) {
            $("#role_unset_constraint").prop('disabled', false);
        } else {
            $("#role_unset_constraint").prop('disabled', true);
        }
    }).fail(function() {
        alert( "Error - url_get_direct_ssd_role_constraints failed." );
    });


    $.ajax({
        method: "GET",
        url: url_get_transitive_ssd_role_constraints,
        dataType: "json",
        data: {name:name},
    }).done(function(data) {
        
        var tssdrc = data['tssdrc'];

        var value = ''
        for (var i = 0; i < tssdrc.length; i++) {
            value = tssdrc[i];
            var option = '<option value=' + value + '>' + value + '</option>';
            $("#tssdrc").append(option);
        }        

    }).fail(function() {
        alert( "Error - url_get_transitive_ssd_role_constraints failed." );
    });
    
    $.ajax({
        method: "GET",
        url: url_get_inherited_ssd_role_constraints,
        dataType: "json",
        data: {name:name},
    }).done(function(data) {
        
        var issdc = data['issdc'];

        var value = ''
        for (var i = 0; i < issdc.length; i++) {
            value = issdc[i];
            var option = '<option value=' + value + '>' + value + '</option>';
            $("#issdc").append(option);
        }        

    }).fail(function() {
        alert( "Error - url_get_inherited_ssd_role_constraints failed." );
    });    
    $('#ssd_role_modal').modal('show');      
}

function Edit_SSDRole_setConstraint() {

    var role = $('#SSD_for_role').val();
    var mutlexcl = $('#ssd_role_role_list').val()[0];
    alert('role:' + role)
    alert('mutlexcl:' + mutlexcl)
    
    if (!mutlexcl) {
        alert('Error: no option selected');
        return;
    }
    
    if (role == mutlexcl) {
        alert('Edit_SSDRole_setConstraint for role "' + role + '", FAILED, a role cannot be mutually exclusive to itself.');
        $('role_list').focus();
        $('#role_list').flash();
        return;
    }
    
    
    var option_values = [];
    $('#dmer option').each(function() {
        option_values.push($(this).val());
    });    
        
    for (i = 0; i < option_values.length; i++) { 
        if (option_values[i] == mutlexcl) {
            alert('Error: ' + mutlexcl + ' already exists');
            $("#dmer").focus();
            return;
        }
    }
    
    $.ajax({
        method: "POST",
        url: url_set_ssd_role_constraint,
        dataType: "json",
        data: {role:role, mutlexcl:mutlexcl}
    }).done(function(data) {
       
        var option = '<option value=' + mutlexcl + '>' + mutlexcl + '</option>';
        $("#dmer").append(option);
        
        $("#role_unset_constraint").prop('disabled', false);
        
    });
    
    return;
}

function Edit_SSDRole_unsetConstraint() {
    
    alert('Edit_SSDRole_unsetConstraint');
    
    var role = $('#SSD_for_role').val();
    var mutlexcl = $('#dmer').val();
        
    if (!mutlexcl) {
        alert('Error: no option selected');
        $('#dmer').focus();
        $('#dmer').flash();
        
        return;
    }
    
    var selector = "#dmer option[value='" + mutlexcl[0] + "']";
    $(selector).remove();
    
    var size = $('#dmer option').size()
    
    if (!size) {
        $("#role_unset_constraint").prop('disabled', true);
    }
    
    $.ajax({
        method: "POST",
        url: url_unset_ssd_role_constraint,
        dataType: "json",
        data: {role:role, mutlexcl:mutlexcl[0]}
    }).done(function(data) {
        
    });

    return;
}

$("#create_ssd_role_btn").click(function(e){
    Edit_SSDRole_init('');
});

$("#role_set_constraint").click(function(e){
    Edit_SSDRole_setConstraint();
});

$("#role_unset_constraint").click(function(e){
    Edit_SSDRole_unsetConstraint();
});

//======================================================================
// PRA section
//======================================================================
function Edit_PRA_init(name) {
        
    // reset all fields
    $('#PRA_for_role').val(name);
    $('#PRA_for_role').prop('disabled', true);
    $('#PRA_perm_list').find('option').remove();
    $('#dp').find('option').remove();
    $('#tp').find('option').remove();
    
    $.ajax({
        method: "GET",
        url: url_get_permission_list,
        dataType: "json",
    }).done(function(data) {
        
        var perm_list = data['perm_list'];

        var value = ''
        for (var i = 0; i < perm_list.length; i++) {
            value = perm_list[i];
            var option = '<option value=' + value + '>' + value + '</option>';
            $("#PRA_perm_list").append(option);
        }        

        if (perm_list.length) {
            $("#revoke_permission").prop('disabled', false);
        } else {
            $("#revoke_permission").prop('disabled', true);
        }
    }).fail(function() {
        alert( "Error - Edit_PRA_init - url_get_permission_list failed." );
    });
          
    $.ajax({
        method: "GET",
        url: url_get_all_directly_assigned_perms,
        dataType: "json",
        data: {name:name},
    }).done(function(data) {
        
        var dp = data['dp'];

        var value = ''
        for (var i = 0; i < dp.length; i++) {
            value = dp[i];
            var option = '<option value=' + value + '>' + value + '</option>';
            $("#dp").append(option);
        }        

        if (dp.length) {
            $("#revoke_permission").prop('disabled', false);
        } else {
            $("#revoke_permission").prop('disabled', true);
        }
    }).fail(function() {
        alert( "Error - url_get_all_directly_assigned_perms failed." );
    });

    $.ajax({
        method: "GET",
        url: url_get_all_transitively_assigned_perms,
        dataType: "json",
        data: {name:name},
    }).done(function(data) {
        
        var tp = data['tp'];

        var value = ''
        for (var i = 0; i < tp.length; i++) {
            value = tp[i];
            var option = '<option value=' + value + '>' + value + '</option>';
            $("#tp").append(option);
        }        

    }).fail(function() {
        alert( "Error - url_get_all_transitively_assigned_perms failed." );
    });
        
    $('#PRA_modal').modal('show');
}

function Edit_PRA_assignPermission() {
        
    var role = $('#PRA_for_role').val();
    var perm = $('#PRA_perm_list').val();

    if (!perm) {
        alert('Error: no option selected');
        return;
    }
        
    var option_values = [];
    $('#dp option').each(function() {
        option_values.push($(this).val());
    });    
        
    for (i = 0; i < option_values.length; i++) { 
        if (option_values[i] == perm[0]) {
            alert('Error: ' + perm[0] + ' already exists');
            $("#dp").focus();
            return;
        }
    }
    
    $.ajax({
        method: "POST",
        url: url_assign_permission,
        dataType: "json",
        data: {role:role, perm:perm[0]}
    }).done(function(data) {
        
    });
    
    var option = '<option value=' + perm + '>' + perm + '</option>';
    $("#dp").append(option);
    
    $("#revoke_permission").prop('disabled', false);
    return;
}

function Edit_PRA_revokePermission() {
        
    var role = $('#PRA_for_role').val();
    var perm = $('#dp').val();
        
    if (!perm) {
        alert('Error: no option selected');
        return;
    }
    
    $.ajax({
        method: "POST",
        url: url_revoke_permission,
        dataType: "json",
        data: {role:role, perm:perm[0]}
    }).done(function(data) {
        var selector = "#dp option[value='" + perm[0] + "']";
        $(selector).remove();
        
        var size = $('#dp option').size()
        
        if (!size) {
            $("#revoke_permission").prop('disabled', true);
        }        
    });

    return;
}

$("#create_PRA_btn").click(function(e) {
    Edit_PRA_init('');
});

$("#assign_permission").click(function(e) {
    Edit_PRA_assignPermission();
});

$("#revoke_permission").click(function(e) {
    Edit_PRA_revokePermission();
});


//======================================================================
// RRA section
//======================================================================
function Edit_RRA_init(name) {
    
    var modal_title = 'Role-to-Role Assignment for Role: ' + name;
    $('#RRA_modal_title').text(modal_title);
    
    // reset all fields
    $('#RRA_role').val(name);
    $('#RRA_role').prop('disabled', true);
    $('#RRA_role_list_JR').find('option').remove();
    $('#RRA_role_list_SR').find('option').remove();
    $('#djr').find('option').remove();
    $('#tjr').find('option').remove();
    $('#dsr').find('option').remove();
    $('#tsr').find('option').remove();
    
    // foreach r [lsort -dictionary [$pm getRoleList]] {
    // set djr [$obj getDirectJuniorRoles]
    // set tjr [$obj getTransitiveJuniorRoles]
    // set dsr [$obj info subclass]
    // set tsr [$obj getTransitiveSeniorRoles]

    $.ajax({
        method: "GET",
        url: url_get_role_list,
        dataType: "json",
    }).done(function(data) {
        
        var role_list = data['role_list'];

        var value = ''
        for (var i = 0; i < role_list.length; i++) {
            value = role_list[i];
            var option = '<option value=' + value + '>' + value + '</option>';
            $("#RRA_role_list_JR").append(option);
        }        

        value = ''
        for (var i = 0; i < role_list.length; i++) {
            value = role_list[i];
            var option = '<option value=' + value + '>' + value + '</option>';
            $("#RRA_role_list_SR").append(option);
        }
                
    }).fail(function() {
        alert( "Error - Edit_RRA_init - url_get_role_list failed." );
    });
      
    // getDirectJuniorRoles
    $.ajax({
        method: "GET",
        url: url_get_direct_junior_roles,
        dataType: "json",
        data: {name:name}
    }).done(function(data) {
        
        var djr= data['djr'];

        var value = ''
        for (var i = 0; i < djr.length; i++) {
            value = djr[i];
            var option = '<option value=' + value + '>' + value + '</option>';
            $("#djr").append(option);
        }        

        if (djr.length) {
            $("#revoke_junior").prop('disabled', false);
        } else {
            $("#revoke_junior").prop('disabled', true);
        }
                
    }).fail(function() {
        alert( "Error - Edit_RRA_init - url_get_direct_junior_roles failed." );
    });    

    // getTransitiveJuniorRoles
    $.ajax({
        method: "GET",
        url: url_get_transitive_junior_roles,
        dataType: "json",
        data: {name:name}
    }).done(function(data) {
        
        var tjr = data['tjr'];

        var value = ''
        for (var i = 0; i < tjr.length; i++) {
            value = tjr[i];
            var option = '<option value=' + value + '>' + value + '</option>';
            $("#tjr").append(option);
        }                        
    }).fail(function() {
        alert( "Error - Edit_PermCCMgmt_init - url_get_transitive_junior_roles failed." );
    });    
   
    // getDirectSeniorRoles
    $.ajax({
        method: "GET",
        url: url_get_direct_senior_roles,
        dataType: "json",
        data: {name:name}
    }).done(function(data) {
        
        var dsr= data['dsr'];

        var value = ''
        for (var i = 0; i < dsr.length; i++) {
            value = dsr[i];
            var option = '<option value=' + value + '>' + value + '</option>';
            $("#dsr").append(option);
        }        
        
        if (dsr.length) {
            $("#revoke_senior").prop('disabled', false);
        } else {
            $("#revoke_senior").prop('disabled', true);
        }
                
    }).fail(function() {
        alert( "Error - Edit_RRA_init - url_get_direct_senior_roles failed." );
    });  

    // getTransitiveSeniorRoles
    $.ajax({
        method: "GET",
        url: url_get_transitive_senior_roles,
        dataType: "json",
        data: {name:name}
    }).done(function(data) {
        
        var tsr = data['tsr'];

        var value = ''
        for (var i = 0; i < tsr.length; i++) {
            value = tsr[i];
            var option = '<option value=' + value + '>' + value + '</option>';
            $("#tsr").append(option);
        }                        
    }).fail(function() {
        alert( "Error - Edit_PermCCMgmt_init - url_get_transitive_senior_roles failed." );
    });    
            
    $('#RRA_modal').modal('show');    
}


function Edit_RRA_assignJunior() {
    
    var role = $('#RRA_role').val();
    var junior = $('#RRA_role_list_JR').val();

    if (!junior) {
        alert('Error: no option selected');
        $('#RRA_role_list_JR').flash();
        $('#RRA_role_list_JR').focus();
        return;
    }
    
    if (role == junior) {
        alert('FAILED: a role cannot be a junior of itself."')
        $("#RRA_role_list_JR").flash();
        $("#RRA_role_list_JR").focus();
        return;
    }
        
    var option_values = [];
    $('#djr option').each(function() {
        option_values.push($(this).val());
    });    
        
    for (i = 0; i < option_values.length; i++) { 
        if (option_values[i] == junior[0]) {
            alert('Error: ' + junior[0] + ' already exists');
            $("#RRA_role_list_JR").flash();
            $("#RRA_role_list_JR").focus();
            return;
        }
    }
        
    $.ajax({
        method: "POST",
        url: url_add_junior_role_relation,
        dataType: "json",
        data: {role:role, junior:junior[0]}
    }).done(function(data) {
        
    });
    
    var option = '<option value=' + junior[0] + '>' + junior[0] + '</option>';
    $("#djr").append(option);
    
    $("#revoke_permission").prop('disabled', false);
    return;

    // set tjr [$obj getTransitiveJuniorRoles]
    // getTransitiveJuniorRoles
    $.ajax({
        method: "GET",
        url: url_get_transitive_junior_roles,
        dataType: "json",
        data: {name:name}
    }).done(function(data) {
        
        var tjr = data['tjr'];

        var value = ''
        for (var i = 0; i < tjr.length; i++) {
            value = tjr[i];
            var option = '<option value=' + value + '>' + value + '</option>';
            $("#tjr").append(option);
        }                        
    }).fail(function() {
        alert( "Error - Edit_RRA_assignJunior - url_get_transitive_junior_roles failed." );
    });  
}

function Edit_RRA_revokeJunior() {
        
    var role = $('#RRA_role').val();
    var junior = $('#djr').val();
        
    if (!junior) {
        alert('Error: no option selected');
        $('#djr').flash();
        $('#djr').focus();        
        return;
    }
    
    $.ajax({
        method: "POST",
        url: url_remove_junior_role_relation,
        dataType: "json",
        data: {role:role, junior:junior[0]}
    }).done(function(data) {
        var selector = "#djr option[value='" + junior[0] + "']";
        $(selector).remove();
        
        var size = $('#djr option').size()
        
        if (!size) {
            $("#revoke_junior").prop('disabled', true);
        }        
    });

    return;
    
}
//TODO
function Edit_RRA_assignSenior() {
    
    var role = $('#RRA_role').val();
    var senior = $('#RRA_role_list_SR').val();

    if (!senior) {
        alert('Error: no option selected');
        $('#RRA_role_list_SR').flash();
        $('#RRA_role_list_SR').focus();
        return;
    }
    
    if (role == senior) {
        alert('FAILED: a role cannot be a senior of itself."')
        $("#RRA_role_list_SR").flash();
        $("#RRA_role_list_SR").focus();
        return;
    }
        
    var option_values = [];
    $('#dsr option').each(function() {
        option_values.push($(this).val());
    });    
        
    for (i = 0; i < option_values.length; i++) { 
        if (option_values[i] == senior[0]) {
            alert('Error: ' + senior[0] + ' already exists');
            $("#RRA_role_list_SR").flash();
            $("#RRA_role_list_SR").focus();
            return;
        }
    }
    // STOPPED HERE    
    $.ajax({
        method: "POST",
        url: url_add_junior_role_relation,
        dataType: "json",
        data: {role:role, junior:junior[0]}
    }).done(function(data) {
        
    });
    
    var option = '<option value=' + junior[0] + '>' + junior[0] + '</option>';
    $("#djr").append(option);
    
    $("#revoke_permission").prop('disabled', false);
    return;

    // set tjr [$obj getTransitiveJuniorRoles]
    // getTransitiveJuniorRoles
    $.ajax({
        method: "GET",
        url: url_get_transitive_junior_roles,
        dataType: "json",
        data: {name:name}
    }).done(function(data) {
        
        var tjr = data['tjr'];

        var value = ''
        for (var i = 0; i < tjr.length; i++) {
            value = tjr[i];
            var option = '<option value=' + value + '>' + value + '</option>';
            $("#tjr").append(option);
        }                        
    }).fail(function() {
        alert( "Error - Edit_RRA_assignJunior - url_get_transitive_junior_roles failed." );
    });  
}

//TODO
function Edit_RRA_revokeSenior() {
    //alert('Edit_RRA_revokeSenior');
}


$("#assign_junior").click(function(e){
    Edit_RRA_assignJunior();
});

$("#revoke_junior").click(function(e){
    Edit_RRA_revokeJunior();
});

$("#assign_senior").click(function(e){
    Edit_RRA_assignSenior();
});

$("#revoke_senior").click(function(e){
    Edit_RRA_revokeSenior();
});


/*
$("#create_PRA_btn").click(function(e){
    Edit_PRA_init('');
});

$("#role_set_constraint").click(function(e){
    Edit_SSDRole_setConstraint();
});

$("#role_unset_constraint").click(function(e){
    Edit_SSDRole_unsetConstraint();
});

*/



