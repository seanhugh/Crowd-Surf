var pricedata = $('#chart-data').data().list;
google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);
console.log(pricedata)
function drawChart() {

    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Date/Time');
    data.addColumn('number', 'Low Price');
    data.addColumn('number', 'Average Price');
    data.addColumn('number', 'High Price');

    for(i = 0; i < pricedata.length; i++)
        data.addRow([pricedata[i][1], pricedata[i][0], pricedata[i][2], pricedata[i][3]]);

    var options = {
        title: 'Ticket Pricing Over Time',
          legend: { position: 'top' }
    };

    // chart = google.visualization.LineChart(document.getElementById('visualization'))

    // chart.draw(data, options);

    var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

    chart.draw(data, options);
};