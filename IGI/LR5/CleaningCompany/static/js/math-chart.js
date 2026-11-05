document.addEventListener('DOMContentLoaded', () => {
    const drawBtn = document.getElementById('draw-chart-btn');
    const canvas = document.getElementById('mathChart');
    
    if (!drawBtn || !canvas) return; 
    let myChart = null;

    function calculateSeries(x, terms) {
        let sum = 0;
        for (let n = 0; n < terms; n++) {
            sum += 2 * (1 / ((2 * n + 1) * Math.pow(x, 2 * n + 1)));
        }
        return sum;
    }

    function calculateMath(x) {
        return Math.log((x + 1) / (x - 1));
    }

    function drawChart() {
        const terms = parseInt(document.getElementById('terms-input').value);

        if (terms > 500) {
            alert("Too many terms. Please enter a number between 1 and 500. (The series converges very fast, 100 is already enough).");
            return; 
        }
        if (terms < 1) {
            alert("Number of terms must be at least 1.");
            return;
        }

        const xStart = parseFloat(document.getElementById('x-start').value);
        const xEnd = parseFloat(document.getElementById('x-end').value);
        
        if (xStart >= xEnd) {
            alert("Error: 'X Start' must be less than 'X End'.");
            return;
        }
        if ((xStart >= -1 && xStart <= 1) || (xEnd >= -1 && xEnd <= 1)) {
            alert("Error: X values must be greater than 1 or less than -1 (|x| > 1).");
            return;
        }
        if (xStart < -1 && xEnd > 1) {
            alert("Error: You cannot plot across the asymptotes. Choose a range entirely > 1 or entirely < -1.");
            return;
        }

        const labels = []; 
        const seriesData = []; 
        const mathData = []; 

        for (let x = xStart; x <= xEnd; x += 0.1) {
            const currentX = parseFloat(x.toFixed(2)); 
            labels.push(currentX);
            seriesData.push(calculateSeries(currentX, terms));
            mathData.push(calculateMath(currentX));
        }

        updateTable(labels, seriesData, mathData, terms);

        if (myChart) {
            myChart.destroy();
        }

        const ctx = canvas.getContext('2d');
        myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Taylor Series',
                        data: seriesData,
                        borderColor: '#e63946',
                        backgroundColor: 'rgba(230, 57, 70, 0.1)',
                        borderWidth: 2,
                        tension: 0.3,
                        fill: true
                    },
                    {
                        label: 'Math Module',
                        data: mathData,
                        borderColor: '#2196f3',
                        backgroundColor: 'transparent',
                        borderWidth: 2,
                        borderDash: [5, 5],
                        tension: 0.3
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 1500,       
                    easing: 'easeOutQuart',
                    delay: 0              
                },
                plugins: {
                    legend: { position: 'top' },
                    title: {
                        display: true,
                        text: `ln((x+1)/(x-1)) (Terms: ${terms})`,
                        font: { size: 16 }
                    }
                },
                scales: {
                    x: { title: { display: true, text: 'x (|x| > 1)' } },
                    y: { title: { display: true, text: 'F(x)' } }
                }
            }
        });
    }

    function updateTable(labels, series, math, terms) {
        const tbody = document.querySelector('#math-data-table tbody');
        tbody.innerHTML = ''; 

        for (let i = 0; i < labels.length; i++) {
            const diff = Math.abs(series[i] - math[i]).toFixed(4);
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${labels[i]}</td>
                <td>${terms}</td>
                <td>${series[i].toFixed(4)}</td>
                <td>${math[i].toFixed(4)}</td>
                <td>${diff}</td>
            `;
            tbody.appendChild(tr);
        }
    }

    drawBtn.addEventListener('click', drawChart);
    drawChart(); 
});