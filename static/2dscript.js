function degreesToRadians(degrees) {
    return degrees * (Math.PI / 180);
}

function drawAnimation(x, y, len1, len2, angle1, angle2) {
    let scale = 100 * 1/(len1 + len2);
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

    // calc of len1 end 
    const x1 = len1 * Math.cos(angle1) * scale;
    const y1 = len1 * Math.sin(angle1) * scale;

    // calc len2 based on len1 end 
    const x2 = x1 + len2 * Math.cos(angle1 + angle2) * scale;
    const y2 = y1 + len2 * Math.sin(angle1 + angle2) * scale;

    // draw len1
    ctx.strokeStyle = 'blue';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(centerX + x1, centerY - y1);
    ctx.stroke();

    // draw len2 from the end of len1
    ctx.strokeStyle = 'red';
    ctx.beginPath();
    ctx.moveTo(centerX + x1, centerY - y1);
    ctx.lineTo(centerX + x2, centerY - y2);
    ctx.stroke();
}

document.getElementById('parameter-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(this);

    fetch('/calculate2d', {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json())
        .then(result => {
            if (result.hasOwnProperty('message')) { // Error handling message
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = result.message;
                resultDiv.style.display = 'block';
                resultDiv.style.backgroundColor = 'tomato'; // Background color changed
            } else {
                const x = parseFloat(formData.get('x'));
                const y = parseFloat(formData.get('y'));
                const len1 = parseFloat(formData.get('len1'));
                const len2 = parseFloat(formData.get('len2'));
                const angle1 = result.angle1;
                const angle2 = result.angle2;

                drawAnimation(x, y, len1, len2, angle1, angle2);

                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = `Angle 1: ${angle1.toFixed(2)} degrees<br>Angle 2: ${angle2.toFixed(2)} degrees`;
                resultDiv.style.display = 'block';
                resultDiv.style.backgroundColor = ''; // Reset background color
            }
        });
});