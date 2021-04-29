// AREA CHART

// References:
// Ingesting data from Google Sheets (CC-BY-4.0 and Apache-2.0)
// https://developers.google.com/chart/interactive/docs/spreadsheets
// StackOverflow answer by WhiteHat (CC-BY-SA-3.0)
// https://stackoverflow.com/a/42335062/4573584

// define variables
var sid = '1CIkj1xhkPyo0LQEIZplKNGS7S6jmcM3MpDlTMghN23Q'; // Google Sheet ID
var sgid = '0'; // Google Sheet GID (string)
var sheader = '1'; // Google Sheet header (string)

google.charts.load(
  'current', {
    'packages': ['corechart']
  }
);
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
  var query = new google.visualization.Query(
    'https://docs.google.com/spreadsheets/d/' + sid + '/gviz/tq?gid=' +
    sgid + '&headers=' + sheader
  );

  query.send(
    function(response) {
      if (response.isError()) {
        console.log(
          'Error in query: ' + response.getMessage() + ' ' +
          response.getDetailedMessage());
        return;
      }

      var options = {
        titleTextStyle: {
          fontName: '"Arial", sans-serif',
        },
        title: 'Gross electricity generation by source in EU-28 from' +
          ' 2000 to 2050 based on the 2016 reference scenario',
        isStacked: 'percent',
        width: 1000,
        hAxis: {
          title: 'Year',
          titleTextStyle: {
            fontName: '"Arial", sans-serif',
          },
          textStyle: {
            fontName: '"Arial", sans-serif',
          },
        },
        vAxis: {
          title: 'Gross electricity generation (%)',
          minValue: 0,
          titleTextStyle: {
            fontName: '"Arial", sans-serif',
          },
          textStyle: {
            fontName: '"Arial", sans-serif',
          },
        },
        series: {
          0: {
            color: 'blue'
          },
          1: {
            color: 'orange'
          },
          2: {
            color: 'grey'
          },
          3: {
            color: 'yellow'
          },
          4: {
            color: 'cyan'
          },
          5: {
            color: 'green'
          },
          6: {
            color: 'red'
          },
          7: {
            color: 'brown'
          },
          8: {
            color: 'black'
          },
        },
        legend: {
          textStyle: {
            fontName: '"Arial", sans-serif',
          }
        },
        tooltip: {
          textStyle: {
            fontName: '"Arial", sans-serif',
          },
        },
      };

      var chart = new google.visualization.AreaChart(
        document.getElementById('chart_div')
      );
      chart.draw(response.getDataTable(), options);
    }
  );
}
