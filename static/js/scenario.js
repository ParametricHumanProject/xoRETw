    
// Handler for .ready() called.
$(function() {
    
    // set modal title for objective dialog
    $('#scenario_modal').on('show.bs.modal', function(e) {
        if (mode == 1) {
            $('#scenario_modal_title').text("Create New Scenario"); 
        } else {
            $('#scenario_modal_title').text("Edit Scenario");   
        }
    })

});

$('#scenario_modal_create_new_step').click(function() {
    $('#step_modal').modal('toggle');
});


$('#scenario_modal_add_step').click(function() {

    var value = $('#scenario_available_steps').val();
        
    if (!value) {
        alert('Error: no option selected - please select of the currently available steps.');
        $('#scenario_available_steps').focus();
        $('#scenario_available_steps').flash();

        return;
    }
    
    
    nodes.add({id: value[0], label:value[0], physics: false, x:100, y:(nodeIds.length*50) + 50});
    nodeIds.push(value[0]);
    network.addEdgeMode();
});

// scenario
$( '#create_scenario_btn' ).click(function() {
    //alert('init here');
    
    // default to edit mode
    $('#graph_edit_mode').click();

    // set to new mode
    mode = 1;
    
    // reset all fields
    $('#scenario_name').val('');
    $('#scenario_available_steps').find('option').remove();
    
    $("#scenario_modal_add_step").prop('disabled', true);
    
    // destroy graph
    if (network === null || network === undefined) {

        
        // create an array with nodes
        nodes = new vis.DataSet([]);

        //nodes.add({id: 7, label: 'Node 7', physics: false, x:50, y:150});
        
        // create an array with edges
        edges = new vis.DataSet([]);

        // create a network
        container = document.getElementById('digraph');

        // provide the data in the vis format
        data = {
            nodes: nodes,
            edges: edges
        };
        
        // these are all options in full.
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

    // initialize your network! - global var
    network = null;// = new vis.Network(container, data, options);
    
    // initialize your network!
    network = new vis.Network(container, data, options);
    
    //network.addEdgeMode();
    
    //network.on("dragStart", function (params) {
    //    network.addEdgeMode();
    //});

    network.on("dragEnd", function (params) {
        if (scenario_graph_mode == 1) {
            network.addEdgeMode();
        }
    });

    
    /*
    network.on("release", function (params) {
            alert('a');
        });    
    network.on("dragging", function (params) {
            alert('dragging');

    });
    network.on("dragEnd", function (params) {
        network.addEdgeMode();
    });
    */
    
 
        
        // by default
        //network.addEdgeMode();
        
    } else {
        // initialize and create graph
        alert('iancrrn');
    
    }
    
    // get all available steps
    $.ajax({
        method: "GET",
        url: url_get_steps,
    }).done(function(data) {
        
        var steps = data['steps'];
        
        // set input values
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


$('#scenario_modal_clear_graph').click(function() {
alert('hhhh');
alert(network);
    if (network !== null) {
        alert('destroy');
        network.destroy();
        network = null;
        nodes.clear();
        nodeIds = [];
    }
});

$('#save_scenario_btn').click(function() {
    
    // validate all fields    
    var id = $('#scenario_id').val();
    var scenario_name = $('#scenario_name').val().split(' ').join('_');

    if (!scenario_name) {
        alert('Error: scenario name cannot be empty.');
        $('#scenario_name').focus();
        $('#scenario_name').flash();
        return;
    }

    // create data
    var scenario_data = new Scenario(id, scenario_name, mode);
    
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
            if (mode == 1) {
                alert('Error - failed to create scenario: '+ scenario_name);
            } else {
                // do nothing
            }
        }
        location.reload();
    }); 
});

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

function Scenario(id, name, mode) {
    this.id = id;
    this.name = name;
    this.mode = mode;
    this.object_type = OBJECT_TYPE_SCENARIO;
}

function edit_scenario(id) {

    mode = 2; // edit
    
    // get existing data and populate dialog
    $.ajax({
        method: "GET",
        url: url_edit_scenario,
        dataType: "json",
        data: {scenario_id: id},
    }).done(function(data) {

        // reset all fields
        $('#scenario_name').val('');
        $('#scenario_available_steps').find('option').remove();
        
        $("#scenario_modal_add_step").prop('disabled', true);
        
        var scenario_name = data['name'];

        // set input values
        $('#scenario_id').val(id); //hidden
        $('#scenario_name').val(scenario_name);

        $('#scenario_modal').modal('show');
        
        var steps = data['steps'];
        
        // set input values
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
        alert( "Error - Edit scenario failed." );
  });    
  
}

$('#graph_edit_mode').click(function(){
    if ($(this).is(':checked'))
    {
      scenario_graph_mode = 1; // set to edit mode
      network.addEdgeMode();
    }
});

$('#graph_select_mode').click(function(){
    if ($(this).is(':checked'))
    {
      scenario_graph_mode = 2; // set to select mode
      network.disableEditMode();
    }
});

