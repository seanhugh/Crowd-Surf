// $ (function() {
//     var availableTags = $('#my-data').data()['list'];
//     $( "#concertSearch" ).autocomplete({
//       source: availableTags
//     });
//   } );

$("#concertSearch").kendoAutoComplete({
    dataTextField: "Name",
    select: function(e) {
        var dataItem = this.dataItem(e.item.index());
        
        //output selected dataItem
        $("#result").html(kendo.stringify(dataItem));       
    },
    dataSource: {
        data: [
            { Name : "GB1", value: 1 },
            { Name : "GB2", value: 2 },
            { Name : "GB3", value: 3 },
            { Name : "GB4", value: 4 }
        ]
    }
});




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