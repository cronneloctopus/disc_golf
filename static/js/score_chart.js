$(function () {
    if (nine_score_arr.length > 0 || eighteen_score_arr.length > 0 ) {
        $('#score_chart').highcharts({
            chart: {
                type: 'spline'
            },
            title: {
                text: ''
            },
            xAxis: [{
                "type": "datetime",
                "labels": {
                    "formatter": function() {
                     return Highcharts.dateFormat("%b %e", this.value)
                    }                    
                }
            }],
            yAxis: {
                title: {
                    text: 'Score'
                },
                // set minimum y-value to lowest possible score
                min: 9
            },
            tooltip: {
                formatter: function() {
                        return '<b>'+ this.series.name +'</b><br/>'+
                        Highcharts.dateFormat('%e %b', this.x) +': '+ '<strong>'+this.y+'</strong>';
                }
            },
            
            series: [{
                name: 'Nine Baskets',
                // Define the data points. All series have a dummy year
                // of 1970/71 in order to be compared on the same x axis. Note
                // that in JavaScript, months start at 0 for January, 1 for February etc.
                data: nine_score_arr.sort()
              }, {
                name: 'Eighteen Baskets',
                // Define the data points. All series have a dummy year
                // of 1970/71 in order to be compared on the same x axis. Note
                // that in JavaScript, months start at 0 for January, 1 for February etc.
                data: eighteen_score_arr.sort()
              },
            ]
        });
    }; 
});   
