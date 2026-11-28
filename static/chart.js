let ctx = null;
let chart = null;
let LABEL_SIZE = 20;
let tick = 0;

let config = {
    type: 'line',

    data: {
        labels: [],
        datasets: [
            {
                label: '왼쪽 눈',
                borderColor: 'black',
                borderWidth: 2,
                data: [],
                fill: false
            },
            {
                label: '오른쪽 눈',
                borderColor: 'gray',
                borderDash: [5, 5],
                borderWidth: 2,
                data: [],
                fill: false
            }
        ]
    },

    options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: false,

        scales: {
            x: {
                display: true,
                title: { display: true, text: '측정 순서' }
            },
            y: {
                display: true,
                title: { display: true, text: '눈 감김 점수' },
                min: 0,
                max: 1,
                ticks: { stepSize: 0.2 }
            }
        }
    }
};

function drawChart() {
    ctx = document.getElementById('canvas').getContext('2d');
    chart = new Chart(ctx, config);
}

function addChartData(left, right) {
    chart.data.labels.push(tick++);
    chart.data.datasets[0].data.push(left);
    chart.data.datasets[1].data.push(right);

    // 최근 20개의 데이터만 유지
    if (chart.data.labels.length > LABEL_SIZE) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
        chart.data.datasets[1].data.shift();
    }

    chart.update();
}
