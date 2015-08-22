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

// default graph mode
var graph_mode = GRAPH_EDIT_MODE;

var nodeIds = null;


function flash(selector) {
    $(selector).fadeOut(250).fadeIn(250);
}

jQuery.fn.extend({
  flash: function() {
    return this.each(function() {
    $(this).fadeOut();
    $(this).fadeIn();
    });
  }
});
