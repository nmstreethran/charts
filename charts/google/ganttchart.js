// Ingesting data from Google Sheets https://developers.google.com/chart/interactive/docs/spreadsheets
// Code courtesy of WhiteHat https://stackoverflow.com/questions/42332424/how-can-i-use-google-charts-to-draw-a-gantt-chart-using-data-from-a-google-sheet
var sheetid = '1EyXVLmkQ2jIvdkSvimjWw0RpbofLuMhL7ynmxofqtco';
var sheetgid = '0';
var sheethead = '1';

google.charts.load('current', {
  callback: drawChart,
  packages: ['gantt']
});

function drawChart() {
  var query = new google.visualization.Query('https://docs.google.com/spreadsheets/d/' + sheetid + '/gviz/tq?gid=' + sheetgid + '&headers=' + sheethead);
  query.send(function(response) {
    if (response.isError()) {
      console.log('Error in query: ' + response.getMessage() + ' ' + response.getDetailedMessage());
      return;
    }

    var options = {
      height: 830,
      width: 1634,
      gantt: {
        labelStyle: {
          fontName: '"Arial", sans-serif',
          fontSize: 12.5
        },
        barHeight: 11,
        barCornerRadius: 3,
        trackHeight: 20,
        innerGridDarkTrack: {
          fill: 'white'
        },
        labelMaxWidth: 325,
        arrow: {
          length: 5,
          radius: 10,
          spaceAfter: 0
        }
      },
    };

    var chart = new google.visualization.Gantt(document.getElementById('chart_div'));
    chart.draw(response.getDataTable(), options);

  });
}
