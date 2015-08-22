

$("#objective_type-1").click(function(e){
    change_select_label(e);
});

$("#objective_type-2").click(function(e){
    change_select_label(e);
});

$("#objective_type-3").click(function(e){
    change_select_label(e);
});

$("#objective_type-4").click(function(e){
    change_select_label(e);
});

$("#objective_type-5").click(function(e){
    change_select_label(e);
});

$("#objective_type-6").click(function(e){
    change_select_label(e);
});

$("#objective_type-7").click(function(e){
    change_select_label(e);
});

$("#objective_type-8").click(function(e){
    change_select_label(e);
});

$("#objective_type-9").click(function(e){
    change_select_label(e);
});

$("#objective_type-10").click(function(e){
    change_select_label(e);
});


// helper
function change_select_label(e) {
    var property_value = $( '#'+e.target.id ).text();
    $('#objective_type').text(property_value);
}
