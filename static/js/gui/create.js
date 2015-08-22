//======================================================================
//  Objective section
//======================================================================

function Create_Objective_init() {
    
    $('#objective_modal_title').text("Create new control objective"); 
    
    // reset all fields
    $('#objective_name').val('');
    $('#objective_type').text('Select');
    $('#objective_abstract_context_condition_entry').val('');
    $('#objective_abstract_context_condition_list').find('oscption').remove();    
    
    $("#save_objective").hide()
    $("#create_objective").show()
    
    $('#objective_modal').modal('toggle');
}

function Create_Objective_create() {

    // validate all fields
    var name = $('#objective_name').val().split(' ').join('_');

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
    
    // api call - post data
    $.ajax({
        method: "POST",
        url: url_create_objective_create,
        dataType: "json",
        data: {name:name, type:type}
    }).done(function(data) {
        
    });
    
    var abstract_context_conditions = [];
    var abstract_context_condition = '';
    
    $('#objective_abstract_context_condition_list option').each(function() {
        abstract_context_condition = $(this).val().split(' ').join('_');

        // api call - post data
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

function Create_Objective_addCondition() {
    var value = $('#objective_abstract_context_condition_entry').val();
    
    if (!$.trim(value)) {
        // error
        alert('Error: condition value cannot be empty.');
        $( "#objective_abstract_context_condition_entry" ).focus();
        return;
    }

    var option_values = [];
    $('#objective_abstract_context_condition_list option').each(function() {
        option_values.push($(this).val());
    });    
        
    for (i = 0; i < option_values.length; i++) { 
        if (option_values[i] == value.split(' ').join('_')) {
            alert('Error: ' + value.split(' ').join('_') + ' already exists');
            $( "#objective_abstract_context_condition_entry" ).focus();
            return;
        }
    }

    // add to list
    var option = '<option value=' + value.split(' ').join('_') + '>' + value + '</option>';
    $("#objective_abstract_context_condition_list").append(option);

    // clear input value
    $('#objective_abstract_context_condition_entry').val('');
    $("#objective_remove_condition").prop('disabled', false);

    return;
}

function Create_Objective_removeCondition() {
    
    var value = $('#objective_abstract_context_condition_list').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    var selector = "#objective_abstract_context_condition_list option[value='" + value + "']";
    $(selector).remove();
    
    var size = $('#objective_abstract_context_condition_list option').size()
    if (!size) {
        $("#objective_remove_condition").prop('disabled', true);
    }

    return;
}

$('#create_objective_btn').click(function() {
    Create_Objective_init();
});


$("#objective_remove_condition").click(function(e){
    Create_Objective_removeCondition(); // used for both create and edit
});

$("#objective_add_condition").click(function(e){
    Create_Objective_addCondition(); // used for both create and edit
});

$("#create_objective").click(function(e){
    Create_Objective_create();
});

//======================================================================
//  Obstacle section
//======================================================================

function Create_Obstacle_init() {
    
    $('#obstacle_modal_title').text("Create new obstacle"); 
    
    // reset all fields
    $('#obstacle_name').val('');
    $('#obstacle_type').text('Avoid');
    $('#obstacle_abstract_context_condition_entry').val('');
    $('#obstacle_abstract_context_condition_list').find('option').remove();    
    
    $("#save_obstacle").hide()
    $("#create_obstacle").show()
    
    $('#obstacle_modal').modal('toggle');
}

function Create_Obstacle_create() {

    // validate all fields
    var name = $('#obstacle_name').val().split(' ').join('_');

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
        url: url_create_obstacle_create,
        dataType: "json",
        data: {name:name, type:type}
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

function Create_Obstacle_addCondition() {
    var value = $('#obstacle_abstract_context_condition_entry').val();
    
    if (!$.trim(value)) {
        // error
        alert('Error: condition value cannot be empty.');
        $( "#obstacle_abstract_context_condition_entry" ).focus();
        return;
    }

    var option_values = [];
    $('#obstacle_abstract_context_condition_list option').each(function() {
        option_values.push($(this).val());
    });    
        
    for (i = 0; i < option_values.length; i++) { 
        if (option_values[i] == value.split(' ').join('_')) {
            alert('Error: ' + value.split(' ').join('_') + ' already exists');
            $( "#obstacle_abstract_context_condition_entry" ).focus();
            return;
        }
    }

    // add to list
    var option = '<option value=' + value.split(' ').join('_') + '>' + value + '</option>';
    $("#obstacle_abstract_context_condition_list").append(option);

    // clear input value
    $('#obstacle_abstract_context_condition_entry').val('');
    $("#obstacle_remove_condition").prop('disabled', false);

    return;
}

function Create_Obstacle_removeCondition() {
    
    var value = $('#obstacle_abstract_context_condition_list').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    var selector = "#obstacle_abstract_context_condition_list option[value='" + value + "']";
    $(selector).remove();
    
    var size = $('#obstacle_abstract_context_condition_list option').size()
    if (!size) {
        $("#obstacle_remove_condition").prop('disabled', true);
    }

    return;
}

$('#create_obstacle_btn').click(function() {
    Create_Obstacle_init();
});

$("#obstacle_remove_condition").click(function(e){
    Create_Obstacle_removeCondition(); // used for both create and edit
});

$("#obstacle_add_condition").click(function(e){
    Create_Obstacle_addCondition(); // used for both create and edit
});

$("#create_obstacle").click(function(e){
    Create_Obstacle_create();
});

//======================================================================
// condition 
//======================================================================
function Create_Condition_init() {
    
    $('#condition_modal_title').text("Create new condition"); 
    
    // reset all fields
    $('#condition_name').val('');
    
    $("#save_condition").hide()
    $("#create_condition").show()
    
    $('#condition_modal').modal('toggle');
}

function Create_Condition_create() {

    // validate all fields
    var name = $('#condition_name').val().split(' ').join('_');

    if (!name) {
        alert('Error: condition name cannot be empty.');
        $("#condition_name").focus();
        $( '#condition_name' ).flash();
        return;
    }
        
    // api call
    $.ajax({
        method: "POST",
        url: url_create_condition_create,
        dataType: "json",
        data: {name:name}
    }).done(function(data) {
        
    });
        
    $('#condition_modal').modal('toggle');
    location.reload();           
}


$('#create_condition_btn').click(function() {
    Create_Condition_init();
});

$("#create_condition").click(function(e){
    Create_Condition_create();
});

//======================================================================
//  Context Constraint section
//======================================================================

function Create_CC_init() {
    
    $('#CC_modal_title').text("Create New Context Constraint"); 
    
    // reset all fields
    $('#CC_name').val('');
    $('#CC_name').prop('disabled', false);
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
            $("#remove_CC_condition").prop('disabled', false);
        } else {
            $("#remove_CC_condition").prop('disabled', true);
        }
        
        $('#CC_modal').modal('show');
                
    }).fail(function() {
        alert( "Error - create context constraint failed." );
    });    
    
    
    $("#close_CC").hide()
    $("#save_CC").hide()
    $("#CC_linkbutton").hide()
    $("#CC_unlinkbutton").hide()
    
    $("#CC_add_condition").show()
    $("#create_CC").show()
    
    
    $('#CC_modal').modal('toggle');
}
    
$("#CC_add_condition").click(function(e){
    
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
    
    $("#CC_remove_condition").prop('disabled', false);

    return;
});

$("#CC_remove_condition").click(function(e){
 
    var value = $('#CC_conditions').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    var selector = "#CC_conditions option[value='" + value + "']";
    $(selector).remove();
    
    var size = $('#CC_conditions option').size()
    if (!size) {
        $("#CC_remove_condition").prop('disabled', true);
    }

    return;
});

function Create_CC_create() {

    // validate all fields
    var name = $('#CC_name').val().split(' ').join('_');

    if (!name) {
        alert('Error: context constraint name cannot be empty.');
        $("#CC_name").focus();
        $( '#CC_name' ).flash();
        return;
    }
        
    // api call
    $.ajax({
        method: "POST",
        url: url_create_CC_create,
        dataType: "json",
        data: {name:name}
    }).done(function(data) {
        
    });
    
    var condition = '';
    
    $('#CC_conditions option').each(function() {
        condition = $(this).val().split(' ').join('_');

        // api call
        $.ajax({
            method: "POST",
            url: url_link_condition_to_context_constraint,
            dataType: "json",
            data: {condition:condition, name:name}
        }).done(function(data) {
            
        });
    });
    
    $('#CC_modal').modal('toggle');
    location.reload();           
}
    




$('#create_CC_btn').click(function() {
    Create_CC_init();
});

$("#create_CC").click(function(e){
    Create_CC_create();
});


//======================================================================
//  Step section
//======================================================================

function Create_Step_init() {
    
    $('#step_modal_title').text("Create New Step"); 
    
    // reset all fields
    $('#step_actor').val('');
    $('#step_action').val('');
    $('#step_target').val('');
    
    $("#close_step").hide()
    $("#save_step").hide()    
    $("#create_step").show()
    
    $('#step_modal').modal('toggle');
}
    
function Create_Step_create() {

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
    
    var step_name = '';
    $.ajax({
        method: "POST",
        url: url_create_step_create,
        dataType: "json",
        data: {actor:actor, action:action, target:target}
    }).done(function(data) {
        step_name = data['name'];

        // refresh step list
        $('#step_list').find('option').remove();
        
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
    }); 

    $('#step_modal').hide();
}

$('#create_step_btn').click(function() {
   Create_Step_init();
});

$("#create_step").click(function(e){
    Create_Step_create();
});


//=====================================================================>
//  Scenario section
//

function Create_Scenario_init() {
    
    $('#scenario_modal_title').text("Create New Scenario"); 
    
    $('#scenario_name').val('');
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

    //$("#cancel_scenario").show()
    $("#save_scenario").hide();  
    $("#create_scenario").show(); 

    $('#scenario_modal').modal('toggle');  
}
function Create_Scenario_addSelectedStep() {
    
    var selected_option = $('#step_list').val();
        
    // TODO: check if more than one selected option; that is an error
    if (!selected_option) {
        alert('Error: no option selected - please select one of the currently available steps.');
        $('#step_list').focus();
        $('#step_list').flash();
        return;
    }
    
    // check if selected step already added
    var node = null;
    node = nodes.get(selected_option[0]);
    
    if (node !== null) {
        alert('Error: the step ' + '"' + selected_option[0] + '"' +  ' already exists in the graph.');
        return;
    }
    
    // add step to graph
    var x_pos = $('#scenario_modal').width()/3;
    nodes.add({id: selected_option[0], label:selected_option[0], physics:false, x: x_pos, y: (nodeIds.length * 50) + 50});
    nodeIds.push(selected_option[0]);
        
    // default to edit mode
    $('#graph_edit_mode').click();
}

function Create_Scenario_create() {

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
    
    // post data
    $.ajax({
        method: "POST",
        url: url_create_scenario_create,
        dataType: "json",
        data: {name:name, graph_dot:graph_dot}
    }).done(function( data ) {

    }); 

    $('#scenario_modal').modal('toggle');
    location.reload();           
}

function Create_Scenario_clearDialog() {
    
    var r = confirm("Do you really want to clear the scenario graph?");
    if (r == true) {
        clear_graph();
        init_graph();        
    }
}

$('#create_scenario_btn').click(function() {
    Create_Scenario_init();
});

$("#create_scenario").click(function(e){
    Create_Scenario_create();
});

$('#create_new_step').click(function() {
    Create_Step_init();
});

$('#add_selected_step').click(function() {
    Create_Scenario_addSelectedStep();
});

$('#clear_graph').click(function() {
    Create_Scenario_clearDialog();
});

$('#graph_edit_mode').click(function(){
    network.addEdgeMode();
});

$('#graph_select_mode').click(function(){
    network.disableEditMode();
});

$('#graph_edit_mode').click(function(){
    if ($(this).is(':checked'))
    {
        graph_mode = GRAPH_EDIT_MODE;
        network.addEdgeMode();
    }
});

$('#graph_select_mode').click(function(){
    if ($(this).is(':checked'))
    {
        graph_mode = GRAPH_SELECT_MODE;
        network.disableEditMode();
    }
});

function clear_graph() {
    
    if (network != null) {
        network.destroy();
        network = null;
    }

    if (nodes != null) {
        nodes.clear();
        nodes = null;
    }

    if (edges != null) {
        edges.clear();
        edges = null;
    }
    
    data = {};
    options = {};
    nodeIds = [];
}

function init_graph() {
    
    // create an array with nodes
    nodes = new vis.DataSet([]);

    // create an array with edges
    edges = new vis.DataSet([]);

    // create a network
    container = document.getElementById('digraph');

    // provide the data in the vis format
    data = {
        nodes: nodes,
        edges: edges
    };
        
    options = {
        nodes:{shape: 'box'},
        edges:{
        arrows: 'to',
        color: 'red',
        font: '12px arial #ff0000',
        scaling:{
          label: true,
        },
        shadow: true,
        smooth: false,
        length: 50,
        physics: false,
        }, 
        manipulation: {
            enabled: false,
            addEdge: function (data, callback) {
                if (data.from == data.to) {
                    
                } else {
                    var connected_nodes = network.getConnectedNodes(data.to);
                    if (connected_nodes) {
        
                        var i;
                        var found = false;
                        for (i = 0; i < connected_nodes.length; i++) {
                            if (data.from == connected_nodes[i]) {
                                found = true;
                            }
                        }
                    }
                    if (!found) {
                        callback(data);
                    }
                }
            }
        },
        physics:{
            stabilization: true
          },        
    }
    
    // initialize your network!
    network = new vis.Network(container, data, options);
 
    network.on("dragEnd", function (params) {
        if (graph_mode == GRAPH_EDIT_MODE) {
            network.addEdgeMode();
        }
    });
}

//<
//< End of Scenario section
//<=====================================================================

//=====================================================================>
//  Permission section
//

function Create_Perm_init() {
    
    $('#perm_modal_title').text("Create New Permission"); 
    
    // reset all fields
    $('#opentry').val('');
    $('#obentry').val('');
    
    $("#close_perm").hide()
    $("#save_perm").hide()    
    $("#cancel_perm").show()
    $("#create_perm").show()
    
    $('#perm_modal').modal('toggle');
}
    
function Create_Perm_create() {

    var opentry = $('#opentry').val().split(' ').join('_');
    var obentry = $('#obentry').val().split(' ').join('_');

    // validate all fields
    if (!opentry) {
        alert('Error: operation name cannot be empty.');
        $('#opentry').focus();
        $('#opentry').flash();
        return;
    }
    
    if (!obentry) {
        alert('Error: object name cannot be empty.');
        $('#obentry').focus();
        $('#obentry').flash();
        return;
    }

    // post data
    $.ajax({
        method: "POST",
        url: url_create_perm_create,
        dataType: "json",
        data: {opentry:opentry, obentry:obentry}
    }).done(function( msg ) {

    }).fail(function() {
        alert( "Error - create permission failed." );
    });    
        

    $('#perm_modal').modal('toggle');
    location.reload();           
}

$('#create_perm_btn').click(function() {
    Create_Perm_init();
});

$("#create_perm").click(function(e){
    Create_Perm_create();
});

//
// End of Permission section
//<======================================================================


//=====================================================================>
//  Profile section
//

function Create_Profile_init() {
    
    $('#profile_modal_title').text("Create new work profile"); 
    
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
            var option = '<option value=' + value + '>' + value + '</option>';
            $("#task_list").append(option);
        }        
                
    }).fail(function() {
        alert( "Error - Create_Profile_init failed." );
    });    
    
    $("#close_profile").hide()
    $("#cancel_profile").show()    
    $("#save_profile").hide()
    $("#create_profile").show()
    
    $('#profile_modal').modal('toggle');
}
    
$("#profile_add_task").click(function(e){
    
    var value = $('#task_list').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    var option_values = [];
    $('#tasks option').each(function() {
        option_values.push($(this).val());
    });    
        
    for (i = 0; i < option_values.length; i++) { 
        if (option_values[i] == value) {
            alert('Error: ' + value + ' already exists');
            $("#task_list").focus();
            return;
        }
    }

    // all good - add condition
    var option = '<option value=' + value + '>' + value + '</option>';
    $("#tasks").append(option);
    
    $("#profile_remove_task").prop('disabled', false);

    return;
});

$("#profile_remove_task").click(function(e){
 
    var value = $('#tasks').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    var selector = "#tasks option[value='" + value + "']";
    $(selector).remove();
    
    var size = $('#tasks option').size()
    if (!size) {
        $("#profile_remove_task").prop('disabled', true);
    }

    return;
});

function Create_Profile_create() {

    // validate all fields
    var name = $('#profile_name').val().split(' ').join('_');

    if (!name) {
        alert('Error: profile name cannot be empty.');
        $("#profile_name").focus();
        $( '#profile_name' ).flash();
        return;
    }
        
    // api call
    $.ajax({
        method: "POST",
        url: url_create_profile_create,
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

$('#create_profile_btn').click(function() {
    Create_Profile_init();
});

$("#create_profile").click(function(e){
    Create_Profile_create();
});

//======================================================================
//  Task section
//======================================================================

function Create_Task_init() {
    
    $('#task_modal_title').text("Create New Task"); 
    
    // reset all fields
    $('#task_name').val('');
    $('#task_name').prop('disabled', false);
    $('#task_available_scenarios').find('option').remove();
    $('#task_scenarios').find('option').remove();
    
    
    // get scenario list
    $.ajax({
        method: "GET",
        url: url_get_scenario_list,
        dataType: "json",
    }).done(function(data) {
        
        var scenario_list = data['scenario_list'];

        var value = ''
        for (var i = 0; i < scenario_list.length; i++) {
            value = scenario_list[i];
            var option = '<option value=' + value + '>' + value + '</option>';
            $("#scenario_list").append(option);
        }        
                
    }).fail(function() {
        alert( "Error - create task failed." );
    });    
    
    
    $("#close_task").hide()
    $("#save_task").hide()    
    $("#save_task").hide()
    $("#create_task").show()
    
    $('#task_modal').modal('toggle');
}
    
$("#add_scenario").click(function(e){
    
    var value = $('#scenario_list').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    var option_values = [];
    $('#scenario option').each(function() {
        option_values.push($(this).val());
    });    
        
    for (i = 0; i < option_values.length; i++) { 
        if (option_values[i] == value) {
            alert('Error: ' + value + ' already exists');
            $("#scenario_list").focus();
            return;
        }
    }

    // all good - add condition
    var option = '<option value=' + value + '>' + value + '</option>';
    $("#scenarios").append(option);
    
    $("#remove_scenario").prop('disabled', false);

    return;
});

$("#remove_scenario").click(function(e){
 
    var value = $('#scenarios').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    var selector = "#scenarios option[value='" + value + "']";
    $(selector).remove();
    
    var size = $('#scenarios option').size()
    if (!size) {
        $("#remove_scenario").prop('disabled', true);
    }

    return;
});

function Create_Task_create() {

    // validate all fields
    var name = $('#task_name').val().split(' ').join('_');

    if (!name) {
        alert('Error: task name cannot be empty.');
        $("#task_name").focus();
        $( '#task_name' ).flash();
        return;
    }
        
    // api call
    $.ajax({
        method: "POST",
        url: url_create_task_create,
        dataType: "json",
        data: {name:name}
    }).done(function(data) {
        
    });
    
    var scenarios = [];
    var scenario = '';
    
    $('#scenarios option').each(function() {
        scenarios.push($(this).val().split(' ').join('_'));
    });    

    $.ajax({
        method: "POST",
        url: url_add_scenarios_to_task,
        dataType: "json",
        data: {scenarios:scenarios, name:name}
    }).done(function(data) {

    });
    
    $('#task_modal').modal('toggle');
    location.reload();           
}

$('#create_task_btn').click(function() {
    Create_Task_init();
});

$("#create_task").click(function(e){
    Create_Task_create();
});

//=====================================================================>
//  Role section
//

function Create_Role_init() {
    
    $('#role_modal_title').text("Create New Role"); 
    
    // reset all fields
    $('#role_name').val('');
    $('#role_list').find('option').remove();
    $('#junior_roles').find('option').remove();
    $('#senior_roles').find('option').remove();
    
    // get role list
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
            $("#role_list").append(option);
        }        
/*
//test
        var value = "IAN CRRN";
        var option = '<option value=' + value + '>' + value + '</option>';
        $("#role_list").append(option);
//test                
*/

    }).fail(function() {
        alert( "Error -Create_Role_init failed." );
    });    

    $("#save_role").hide()    
    $("#create_role").show()
    
    $('#role_modal').modal('toggle');
}

$("#add_junior").click(function(e) {

    var value = $('#role_list').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    var option_values = [];
    $('#junior_roles option').each(function() {
        option_values.push($(this).val());
    });    
        
    for (i = 0; i < option_values.length; i++) { 
        if (option_values[i] == value) {
            alert('Error: ' + value + ' already exists');
            $("#role_list").focus();
            return;
        }
    }

    var option = '<option value=' + value + '>' + value + '</option>';

    $("#junior_roles").append(option);
    
    $("#remove_junior").prop('disabled', false);

    return;
});

$("#add_senior").click(function(e) {

    var value = $('#role_list').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    var option_values = [];
    $('#senior_roles option').each(function() {
        option_values.push($(this).val());
    });    
        
    for (i = 0; i < option_values.length; i++) { 
        if (option_values[i] == value) {
            alert('Error: ' + value + ' already exists');
            $("#role_list").focus();
            return;
        }
    }

    var option = '<option value=' + value + '>' + value + '</option>';

    $("#senior_roles").append(option);
    
    $("#remove_senior").prop('disabled', false);

    return;
});

$("#remove_junior").click(function(e) {
 
    var value = $('#junior_roles').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    var selector = "#junior_roles option[value='" + value + "']";
    $(selector).remove();
    
    var size = $('#junior_roles option').size()
    if (!size) {
        $("#remove_junior").prop('disabled', true);
    }

    return;
});

$("#remove_senior").click(function(e) {
 
    var value = $('#senior_roles').val();
        
    if (!value) {
        alert('Error: no option selected');
        return;
    }
    
    var selector = "#senior_roles option[value='" + value + "']";
    $(selector).remove();
    
    var size = $('#senior_roles option').size()
    if (!size) {
        $("#remove_senior").prop('disabled', true);
    }

    return;
});

function Create_Role_create() {

    // validate all fields
    var name = $('#role_name').val().split(' ').join('_');

    if (!name) {
        alert('Error: role name cannot be empty.');
        $("#role_name").focus();
        $( '#role_name' ).flash();
        return;
    }
    
    var exists = false;
    
    $.ajax({
        method: "GET",
        url: url_exist_role,
        dataType: "json",
        data: {name:name}
    }).done(function(data) {
        
        if (data['exists'] == 1) {
            exists = true;
        }

        if (exists) {
            alert('Error: Role "' + name + '" already exists.');
            return;
        }
        
        var junior = [];
        
        $('#junior_roles option').each(function() {
            junior.push($(this).val().split(' ').join('_'));
        });    

        var senior = [];
        
        $('#senior_roles option').each(function() {
            senior.push($(this).val().split(' ').join('_'));
        });    
                
        $.ajax({
            method: "POST",
            url: url_create_role_create,
            dataType: "json",
            data: {name:name, junior:junior, senior:senior}
        }).done(function(data) {
            
            var success = data['success'];
            
            if (success == 'false') {
                alert(data['error_message'])
                return;
            } else {
                $('#role_modal').modal('toggle');
                location.reload();               
            }
        });

    });
    
 
    
}

$('#create_role_btn').click(function() {
    Create_Role_init();
});

$("#create_role").click(function(e){
    Create_Role_create();
});

//
//  Role section
//<=====================================================================

