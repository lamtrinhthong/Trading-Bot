document.addEventListener('DOMContentLoaded', function() {
    // Extract data from a global variable set by Django
    const data = JSON.parse(document.getElementById('chart-data').textContent);

    // Initialize arrays to store candlestick data
    let trace = {
        x: [],
        close: [],
        high: [],
        low: [],
        open: [],
        type: 'candlestick',
        increasing: {line: {color: 'green'}},
        decreasing: {line: {color: 'red'}}
    };

    // Iterate over each data point and extract values
    data.forEach(d => {
        trace.x.push(new Date(d.time));
        trace.open.push(d.open);
        trace.high.push(d.high);
        trace.low.push(d.low);
        trace.close.push(d.close);
    });

    // Layout for the chart
    const layout = {
        title: 'Candlestick Chart',
        uirevision:'true',
        xaxis: {
            title: 'Time',
            autorange: true
        },
        yaxis: {
            title: 'Price',
            autorange: true
        }
    };

    // Plot the chart
    Plotly.newPlot('candlestick-chart', [trace], layout, {responsive: true});
});
