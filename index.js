function stock_sub() {
        
        var form_data = new FormData();
        form_data.append('stock_name',document.getElementById('stock_name').value);
            
        setTimeout(function() {

                $.ajax({
                   type: "POST",
                   url: "http://localhost:8888/stock",
                   data: form_data,
                   cache: false,
                   contentType: false,
                   processData: false,
                   dataType: 'json',
                   success: function (response) {
                       console.log(response);
                       create_chart(response);
                   },
                   error: function (response) {
                   }
                });
                
            },0); 
}

//Plot graph, HighCharts
function create_chart(data){

    // split the data set into ohlc and volume
    var ohlc = [],
        volume = [],
        dataLength = data['data'].length,
        // set the allowed units for data grouping
        groupingUnits = [[
            'week',                         // unit name
            [1]                             // allowed multiples
        ], [
            'month',
            [1, 2, 3, 4, 6]
        ]],

        i = 0;
    console.log(dataLength);
    for (i; i < dataLength; i += 1) {
        ohlc.push([
            data['data'][i][0], // the date
            data['data'][i][1], // open
            data['data'][i][2], // high
            data['data'][i][3], // low
            data['data'][i][4] // close
        ]);

        volume.push([
            data['data'][i][0], // the date
            data['data'][i][5] // the volume
        ]);
    }


    // create the chart
    Highcharts.stockChart('container', {

        rangeSelector: {
            selected: 1
        },

        title: {
            text: data['info']['2. Symbol']
        },

        yAxis: [{
            labels: {
                align: 'right',
                x: -3
            },
            title: {
                text: 'OHLC'
            },
            height: '60%',
            lineWidth: 2
        }, {
            labels: {
                align: 'right',
                x: -3
            },
            title: {
                text: 'Volume'
            },
            top: '65%',
            height: '35%',
            offset: 0,
            lineWidth: 2
        }],

        tooltip: {
            split: true
        },

        series: [{
            type: 'candlestick',
            name: 'AAPL',
            data: ohlc,
            dataGrouping: {
                units: groupingUnits
            }
        }, {
            type: 'column',
            name: 'Volume',
            data: volume,
            yAxis: 1,
            dataGrouping: {
                units: groupingUnits
            }
        }]
    });
}