// PIE CHART

// References:
// Ingesting data from Google Sheets (CC-BY-4.0 and Apache-2.0)
// https://developers.google.com/chart/interactive/docs/spreadsheets
// StackOverflow answer by WhiteHat (CC-BY-SA-3.0)
// https://stackoverflow.com/a/42335062

// define variables
var sid = '1CIkj1xhkPyo0LQEIZplKNGS7S6jmcM3MpDlTMghN23Q'; // Google Sheet ID
var sgid = '1117722966'; // Google Sheet GID (string)
var sheader = '1'; // Google Sheet header (string)

google.charts.load(
  'current', {
    packages: ['corechart']
  }
);
google.charts.setOnLoadCallback(drawColColors);

function drawColColors() {
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
        fontName: '"Arial", sans-serif',
        title: 'Energy emissions by subsector in Germany in 2012' +
          ' (MtCO²ₑ). Data: WRI CAIT.',
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
        document.getElementById('chart_div')
      );
      chart.draw(response.getDataTable(), options);
    }
  );
}
