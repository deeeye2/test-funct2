document.getElementById('k8s-calculator').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);

    const response = await fetch('/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    document.getElementById('instanceType').innerText = result.instanceType;
    document.getElementById('totalCost').innerText = result.totalCost;
    document.getElementById('provider').innerText = result.provider;

    const ctx = document.getElementById('costChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Total Cost'],
            datasets: [{
                label: result.provider,
                data: [result.totalCost],
                backgroundColor: ['rgba(75, 192, 192, 0.2)'],
                borderColor: ['rgba(75, 192, 192, 1)'],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
});
