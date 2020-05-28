google.charts.load('current', {
  callback: drawChart,
  packages: ['gantt']
});

function drawChart() {
  //import data from Google Sheets
  var query = new google.visualization.Query(
    'https://docs.google.com/spreadsheets/d/1EyXVLmkQ2jIvdkSvimjWw0RpbofLuMhL7ynmxofqtco/gviz/tq?gid=0&headers=1');

  query.send(function (response) {
    if (response.isError()) {
      console.log('Error in query: ' + response.getMessage() + ' ' +
      response.getDetailedMessage());
      return;
    }

    var options = {
      height: 830,
      width: 1634,
      gantt: {
        barHeight: 11,
        barCornerRadius: 3,
        trackHeight: 20,
        innerGridDarkTrack: {
          fill: 'white',
        },
        labelMaxWidth: 325,
        arrow: {
          length: 5,
          radius: 10,
          spaceAfter: 0,
        },
        labelStyle: {
          fontName: "'Arial', sans-serif",
          fontSize: 12.5,
        },
      },
    };

    var chart = new google.visualization.Gantt(
      document.getElementById('chart_div'));
    chart.draw(response.getDataTable(), options);
  });
}
