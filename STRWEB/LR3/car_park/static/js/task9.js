const COUNT_ELEMENT = 10;
const START = 0;
const END = 3;
const COUNT_TERM = 9;
const STEP = (END - START) / (COUNT_ELEMENT - 1);


let xValues = [];

for (let i = 0; i < COUNT_ELEMENT; ++i) {
    xValues.push(i * STEP);
}

function calculateSeries(x, n) {
    let term = 1.0;
    let sum = term;
    for (let k = 1; k < n; k++) {
        term *= x / k;
        sum += term;
    }
    return sum;
}

const seriesValues = xValues.map((x, i) => calculateSeries(x, COUNT_TERM));


const mathValues = xValues.map(x => Math.E ** x);


const ctx = document.getElementById('myChart').getContext('2d');
const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: xValues.map(x => Math.round(x * 1000) / 1000), 
        datasets: [
            {
                label: 'Ряд F(x)',
                data: seriesValues,
                borderColor: 'red',
                fill: false,
            },
            {
                label: 'Функция Math F(x)',
                data: mathValues,
                borderColor: 'blue',
                fill: false,
            }
        ]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: true,
            },
            tooltip: {
                enabled: true,
            },
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Аргумент x',
                },
            },
            y: {
                title: {
                    display: true,
                    text: 'Значение функции',
                },
            },
        }
    }
});

const mainTag = document.querySelector('main');
const saveButton = document.createElement('button');
saveButton.innerText = 'Сохранить график';
mainTag.appendChild(saveButton);

saveButton.addEventListener('click', () => {
    const image = ctx.canvas.toDataURL('image/png');
    const link = document.createElement('a');
    link.href = image;
    link.download = 'chart.png';
    link.click();
});
