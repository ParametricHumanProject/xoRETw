
// Handler for .ready() called.
$(function() {
    
});

// set modal title for scenario modal
$('#scenario_modal').on('show.bs.modal', function(e) {
    if (mode == CREATE_MODE) {
        $('#scenario_modal_title').text("Create New Scenario"); 
    } else {
        $('#scenario_modal_title').text("Edit Scenario");   
    }
})

$('#scenario_modal_create_new_step').click(function() {
    $('#step_modal').modal('toggle');
});

$('#scenario_modal_add_step').click(function() {

    var selected_options = $('#scenario_available_steps').val();
        
    // TODO: check if more than one selected option; that is an error
    if (!selected_options) {
        alert('Error: no option selected - please select one of the currently available steps.');
        $('#scenario_available_steps').focus();
        $('#scenario_available_steps').flash();

        return;
    }
    //alert(selected_options[0]);
    // check if selected step already added
    var node = null;
    node = nodes.get(selected_options[0]);
    
    if (node !== null) {
        alert('Error: the step ' + '"' + selected_options[0] + '"' +  ' already exists in the graph.');
        return;
    }
    
    // add step to graph
    nodes.add({id: selected_options[0], label:selected_options[0], physics: false, x:100, y:(nodeIds.length*50) + 50});
    nodeIds.push(selected_options[0]);
    
    // default to edit mode
    $('#graph_edit_mode').click();    
});

// create new scenario
$( '#create_scenario_btn' ).click(function() {
    
    // set to new mode
    mode = CREATE_MODE;
    
    // reset all fields
    $('#scenario_name').val('');
    $('#scenario_available_steps').find('option').remove();
    $("#scenario_modal_add_step").prop('disabled', true);

    clear_graph();
    init_graph();
    
    // get all available steps from the server
    $.ajax({
        method: "GET",
        url: url_get_steps,
    }).done(function(data) {
        
        var steps = data['steps'];
        
        // populate available step select
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

function edit_scenario(id) {

    mode = EDIT_MODE; // edit
    
    // get existing data and populate dialog
    $.ajax({
        method: "GET",
        url: url_edit_scenario,
        dataType: "json",
        data: {scenario_id: id},
    }).done(function(data) {

        // reset all fields and step graph
        $('#scenario_name').val('');
        $('#scenario_available_steps').find('option').remove();
        $("#scenario_modal_add_step").prop('disabled', true);

        clear_graph();
        init_graph();
        
        var scenario_name = data['name'];
        var scenario_graph_dot = data['graph_dot'];
        var steps = data['steps'];
        
        // set input values
        $('#scenario_id').val(id); //hidden
        $('#scenario_name').val(scenario_name);

        // steps
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
                
        // import DOT into graph
        
        var parsedData = vis.network.convertDot(scenario_graph_dot);//scenario_graph_dot);
        
        for (var i = 0; i < parsedData.nodes.length; i++) {
            nodes.add(parsedData.nodes[i]);
        }
        
        for (var i = 0; i < parsedData.edges.length; i++) {
            edges.add(parsedData.edges[i]);
        }

        // provide the data in the vis format
        data = {
          nodes: nodes,
          edges: edges
        }

        // create a network
        container = document.getElementById('digraph');
            
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
            smooth: true,
            } , 
            manipulation: {
                enabled: false,
            }
        };
        
        // create a network
        network = new vis.Network(container, data, options);    

        // default to select mode
        $('#graph_select_mode').click();    

        // show scenario modal
        $('#scenario_modal').modal('show');
        

    }).fail(function() {
        alert( "Error - Edit scenario failed." );
  });    
  
}

$('#scenario_modal_clear_graph').click(function() {
    clear_graph();
    init_graph();
});

$('#save_scenario_btn').click(function() {
    
    // get and validate all fields    
    var id = $('#scenario_id').val();
    var scenario_name = $('#scenario_name').val().split(' ').join('_');

    if (!scenario_name) {
        alert('Error: scenario name cannot be empty.');
        $('#scenario_name').focus();
        $('#scenario_name').flash();
        return;
    }

    // get step graph
    // DOT string
    var graph_dot = '';
    graph_dot = 'graph {'
    var all_edges = edges.get(); 
    
    var i;
    var edge;
    //var temp;
    
    for (i = 0; i < all_edges.length; i++) { 
        edge = all_edges[i];

        if (i == all_edges.length - 1) {
            graph_dot = graph_dot + String(edge['from']) + '->' + String(edge['to']);
        } else {
            graph_dot = graph_dot + String(edge['from']) + '->' + String(edge['to']) + ';';
        }
    }
    graph_dot = graph_dot + '}';
    
    //alert(graph_dot);
    //alert(typeof(graph_dot));
    
    // create data
    var scenario_data = new Scenario(id, scenario_name, graph_dot, mode);
    
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
            if (mode == CREATE_MODE) {
                alert('Error - failed to create scenario: '+ scenario_name);
            } else {
                // do nothing
            }
        }
        location.reload();
    }); 
    
});

$('#graph_edit_mode').click(function(){
    //if ($(this).is(':checked'))
    //{
      scenario_graph_mode = GRAPH_EDIT_MODE; // set to edit mode
      network.addEdgeMode();
    //}
});

$('#graph_select_mode').click(function(){
    if ($(this).is(':checked'))
    {
      scenario_graph_mode = GRAPH_SELECT_MODE; // set to select mode
      network.disableEditMode();
    }
});

function clear_graph() {
    
    if (network !== null) {
        network.destroy();
        network = null;
    }
    if (nodes !== null) {
        nodes.clear();
        nodes = null;
    }
    if (edges !== null) {
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
        smooth: true,
        physics: true,
        }, 
        manipulation: {
            enabled: false,
        },
}
    
    // initialize your network!
    network = new vis.Network(container, data, options);
    
    network.on("dragEnd", function (params) {
        if (scenario_graph_mode == 1) {
            network.addEdgeMode();
        }
    });
}

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

function Scenario(id, name, graph_dot, mode) {
    this.id = id;
    this.name = name;
    this.graph_dot = graph_dot;
    this.mode = mode;
    this.object_type = OBJECT_TYPE_SCENARIO;
}
