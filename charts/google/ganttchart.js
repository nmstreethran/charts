// GANTT CHART

// References:
// Ingesting data from Google Sheets (CC-BY-4.0 and Apache-2.0)
// https://developers.google.com/chart/interactive/docs/spreadsheets
// StackOverflow answer by WhiteHat (CC-BY-SA-3.0)
// https://stackoverflow.com/a/42335062/4573584

// define variables
var sid = '1EyXVLmkQ2jIvdkSvimjWw0RpbofLuMhL7ynmxofqtco'; // Google Sheet ID
var sgid = '0'; // Google Sheet GID (string)
var sheader = '1'; // Google Sheet header (string)
var cheight = 830; // chart height
var cwidth = 1634; // chart width
var lfont = '"Arial", sans-serif'; // label font family
var lfontsize = 12.5; // label font size
var lmaxwidth = 325; // label max width
var bheight = 11; // bar height
var bcrad = 3; // bar corner radius
var theight = 20; // track height
var tfill = 'white'; // inner track fill
var alength = 5; // arrow length
var arad = 10; // arrow radius
var aspace = 0; // space after arrow

// plot the chart
google.charts.load(
  'current', {
    callback: drawChart,
    packages: ['gantt']
  }
);

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
        height: cheight,
        width: cwidth,
        gantt: {
          labelStyle: {
            fontName: lfont,
            fontSize: lfontsize
          },
          barHeight: bheight,
          barCornerRadius: bcrad,
          trackHeight: theight,
          innerGridDarkTrack: {
            fill: tfill
          },
          labelMaxWidth: lmaxwidth,
          arrow: {
            length: alength,
            radius: arad,
            spaceAfter: aspace
          }
        },
      };

      var container = document.getElementById('chart_div');
      var chart = new google.visualization.Gantt(container);

      chart.draw(response.getDataTable(), options);
    }
  );
}
