function degreesToRadians(degrees) {
    return degrees * (Math.PI / 180);
}

function drawAnimation(x, y, len1, len2, angle1, angle2) {
    const canvas = document.getElementById('animation-canvas');
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw axes
    ctx.strokeStyle = '#ccc';
    ctx.beginPath();
    ctx.moveTo(0, canvas.height / 2);
    ctx.lineTo(canvas.width, canvas.height / 2);
    ctx.moveTo(canvas.width / 2, 0);
    ctx.lineTo(canvas.width / 2, canvas.height);
    ctx.stroke();

    // Drawing origin
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    ctx.fillStyle = 'green';
    ctx.beginPath();
    ctx.arc(centerX, centerY, 5, 0, Math.PI * 2);
    ctx.fill();

    angle1 = degreesToRadians(angle1);
    angle2 = degreesToRadians(180 - angle2);

    // Calculate positions based on lengths and angles
    const scale = 1.5;
    const x1 = len1 * Math.cos(angle1) * scale;
    const y1 = len1 * Math.sin(angle1) * scale;
    const x2 = x1 + len2 * Math.cos(angle1 + angle2) * scale;
    const y2 = y1 + len2 * Math.sin(angle1 + angle2) * scale;

    // Draw links
    ctx.strokeStyle = 'blue';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(centerX + x1, centerY - y1);
    ctx.stroke();

    ctx.strokeStyle = 'red';
    ctx.beginPath();
    ctx.moveTo(centerX + x1, centerY - y1);
    ctx.lineTo(centerX + x2, centerY - y2);
    ctx.stroke();

    // Draw points
    ctx.fillStyle = 'blue';
    ctx.beginPath();
    ctx.arc(centerX + x1, centerY - y1, 5, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = 'red';
    ctx.beginPath();
    ctx.arc(centerX + x2, centerY - y2, 5, 0, Math.PI * 2);
    ctx.fill();
}

function updateGraph() {
    const formData = new FormData(document.getElementById('parameter-form'));

    fetch('/calculate2d', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(result => {
            const resultDiv = document.getElementById('result');
            if (result.hasOwnProperty('message')) {
                resultDiv.innerHTML = result.message;
                resultDiv.style.display = 'block';
                resultDiv.style.backgroundColor = 'tomato';
            } else {
                const x = parseFloat(formData.get('x'));
                const y = parseFloat(formData.get('y'));
                const len1 = parseFloat(formData.get('len1'));
                const len2 = parseFloat(formData.get('len2'));
                const angle1 = result.angle1;
                const angle2 = result.angle2;

                drawAnimation(x, y, len1, len2, angle1, angle2);
    
                resultDiv.innerHTML = `
                    <h3><strong>Input:</strong></h3>
                    <p><strong> len1:</strong> ${len1.toFixed(2)}</p>
                    <p><strong> len2:</strong> ${len2.toFixed(2)}</p>
                    <p><strong>x:</strong> ${x.toFixed(2)}</p>
                    <p><strong>y:</strong> ${y.toFixed(2)}</p>
                    <h3><strong>Result:</strong></h3>
                    <p><strong>Angle 1:</strong> ${angle1.toFixed(2)} degrees</p>
                    <p><strong>Angle 2:</strong> ${angle2.toFixed(2)} degrees</p>
                `;
                resultDiv.style.display = 'block';
                resultDiv.style.backgroundColor = '';
            }
        })
        .catch(error => console.error('Error:', error));
}