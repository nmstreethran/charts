google.charts.load('current', {
  'packages': ['corechart']
});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
  var query = new google.visualization.Query(
    'https://docs.google.com/spreadsheets/d/1CIkj1xhkPyo0LQEIZplKNGS7S6jmcM3MpDlTMghN23Q/gviz/tq?gid=0&headers=1'
  );

  query.send(function(response) {
    if (response.isError()) {
      console.log('Error in query: ' + response.getMessage() + ' ' +
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
      document.getElementById('chart_div'));
    chart.draw(response.getDataTable(), options);
  });
}
