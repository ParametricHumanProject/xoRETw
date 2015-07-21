var CREATE_MODE = 1
var EDIT_MODE = 2

var GRAPH_EDIT_MODE = 1
var GRAPH_SELECT_MODE = 2
//-----------------------
// vis.js
//-----------------------

// global variables
var network = null; 
var nodes = null;
var edges = null;

// create a network
var container = null;

// provide the data in the vis format
var data = null;
var options = null;

// edit = 1 or select = 2 mode     
var scenario_graph_mode = 1;

var nodeIds = null;
