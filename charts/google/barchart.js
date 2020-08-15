google.charts.load('current', {
  packages: ['corechart', 'bar']
});
google.charts.setOnLoadCallback(drawColColors);

function drawColColors() {
  var query = new google.visualization.Query(
    'https://docs.google.com/spreadsheets/d/1CIkj1xhkPyo0LQEIZplKNGS7S6jmcM3MpDlTMghN23Q/gviz/tq?gid=2084461080&headers=1'
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
      title: 'Baseline cost breakdown of electricity generation' +
        'technologies from the NREL-SEAC-2008 dataset',
      colors: ['#9575cd', '#33ac71', '#f08080'],
      hAxis: {
        title: 'Electricity generation technology',
        viewWindow: {
          min: [7, 30, 0],
          max: [17, 30, 0],
        },
        titleTextStyle: {
          fontName: '"Arial", sans-serif',
        },
        textStyle: {
          fontName: '"Arial", sans-serif',
        },
      },
      vAxis: {
        title: 'Baseline cost breakdown (%)',
        titleTextStyle: {
          fontName: '"Arial", sans-serif',
        },
        textStyle: {
          fontName: '"Arial", sans-serif',
        },
      },
      isStacked: 'percent',
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

    var chart = new google.visualization.BarChart(
      document.getElementById('chart_div'));
    chart.draw(response.getDataTable(), options);
  });
}
