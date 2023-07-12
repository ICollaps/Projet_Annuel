function createAgeDistributionChart(ages) {
    const ageData = Array(10).fill(0);
    console.log(ageData)

    for (let age of ages) {
        console.log(age)
        ageData[Math.floor(age / 10)]++;
    }
    console.log(ageData)

    const option = {
        title: {
            text: 'Distribution de l\'âge'
        },
        xAxis: {
            type: 'category',
            data: ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-99']
        },
        yAxis: {
            type: 'value'
        },
        series: [{
            data: ageData,
            type: 'bar'
        }]
    };

    const chart = echarts.init(document.getElementById('age-distribution-chart'));
    chart.setOption(option);
}

function createPredictionChart(predictionCounts) {
    let chartDom = document.getElementById('prediction-chart');
    let myChart = echarts.init(chartDom);
    let option;

    option = {
        title: {
            text: 'Distribution des Prédictions'
        },
        tooltip: {},
        legend: {
            orient: 'vertical',
            left: 'right',
            data: ['0', '1'] // les noms de vos séries
        },
        xAxis: {
            data: ["0", "1"],
            show: false,  // Add this line
        },
        yAxis: {},
        series: [{
            name: 'Count',
            type: 'pie',
            data: predictionCounts.map((count, index) => {
                return {value: count, name: index.toString()}  // assigner un nom à chaque série
            })
        }]
    };

    option && myChart.setOption(option);
}

