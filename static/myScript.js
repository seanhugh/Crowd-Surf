$ (function() {
    var availableTags = $('#my-data').data()['list'];
    $( "#concertSearch" ).autocomplete({
      source: availableTags
    });
  } );

console.log($('#my-data').data());
var data = $('#my-data').data()['list'];
console.log(data);


// $('#concertSearch').autocomplete({
//     source: url,
//     select: function (event, ui) {
//         $("#txtAllowSearch").val(ui.item.label); // display the selected text
//         $("#txtAllowSearchID").val(ui.item.value); // save selected id to hidden input
//     }
// });

// $('#button').click(function() {
//     alert($("#txtAllowSearchID").val()); // get the id from the hidden input
// }); 