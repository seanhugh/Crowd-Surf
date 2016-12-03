/*
 * jQuery UI Autocomplete: Using Label-id Pairs
 * http://salman-w.blogspot.com/2013/12/jquery-ui-autocomplete-examples.html
 */

var data = $('#my-data').data().list;

console.log(data);
$(function() {
    $("#autocomplete2").autocomplete({
        source: data,
        focus: function(event, ui) {
            // prevent autocomplete from updating the textbox
            event.preventDefault();
            // manually update the textbox
            $(this).val(ui.item.label);
        },
        select: function(event, ui) {
            // prevent autocomplete from updating the textbox
            event.preventDefault();
            // manually update the textbox and hidden field
            // $(this).val(ui.item.label);
            
            // $("#autocomplete2-id").val(ui.item.id);
            window.location = "concert/" + ui.item.id;
        }
        // open: function(event, ui) {
        //     $('.ui-autocomplete').append('<div class="ui-menu-item-wrapper"><li class = "ui-menu-item"><a href="all">Show all Concerts...</a></li></div>'); //See all results
        // }
    });
});