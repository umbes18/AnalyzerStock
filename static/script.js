document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.container');
    container.classList.add('fade-in');
    if (window.priceData) {
        const ctx = document.getElementById('priceChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: priceData.dates,
                datasets: [{
                    label: 'Prezzo di chiusura',
                    data: priceData.prices,
                    borderColor: '#2196f3',
                    backgroundColor: 'rgba(33,150,243,0.1)',
                    tension: 0.1
                }]
            },
            options: {
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: { display: true },
                    y: { display: true }
                }
            }
        });
    }
});
