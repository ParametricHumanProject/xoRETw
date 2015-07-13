    
// Handler for .ready() called.
$(function() {
    
    
    // set modal title for obstacle dialog
    $('#step_modal').on('show.bs.modal', function(e) {
        
        if (mode == 1) {
            $('#step_modal_title').text("Create New Step"); 
        } 
    })
        


});

