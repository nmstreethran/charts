google.charts.load('current', {packages: ['corechart']});
google.charts.setOnLoadCallback(drawColColors);

function drawColColors() {
  var query = new google.visualization.Query(
    'https://docs.google.com/spreadsheets/d/1CIkj1xhkPyo0LQEIZplKNGS7S6jmcM3MpDlTMghN23Q/gviz/tq?gid=1117722966&headers=1');

  query.send(function (response) {
    if (response.isError()) {
      console.log('Error in query: ' + response.getMessage() + ' ' +
      response.getDetailedMessage());
      return;
    }

    var options = {
      fontName: "'Lato', 'Arial', sans-serif",
      title: 'Energy emissions by subsector in Germany in 2012 ' +
        '(MtCO²ₑ). Data: WRI CAIT.',
      colors: ['#9575cd', '#33ac71', '#f08080', '#f0e68c', '#66cdaa'],
      hAxis: {
        title: 'Electricity generation technology',
        viewWindow: {
          min: [7, 30, 0],
          max: [17, 30, 0],
        },
      },
      vAxis: {
        title: 'Baseline cost breakdown (US$/MWh)',
      },
    };

    var chart = new google.visualization.PieChart(
      document.getElementById('chart_div'));
    chart.draw(response.getDataTable(), options);
  });
}
