document.addEventListener('DOMContentLoaded', function () {
    const sliders = document.querySelectorAll('input[type="range"]');
    const resultDiv = document.getElementById('result');
    // const xVal = document.getElementById('x-val');
    // const yVal = document.getElementById('y-val');
    // const zVal = document.getElementById('z-val');
    const len1Val = document.getElementById('len1-val');
    const len2Val = document.getElementById('len2-val');
    const len3Val = document.getElementById('len3-val');
    
    sliders.forEach(slider => {
        slider.addEventListener('input', updateValues);
        slider.addEventListener('change', updateResult);
    });
    updateResult();

    function updateValues() {
        xVal.textContent = document.getElementById('x').value;
        yVal.textContent = document.getElementById('y').value;
        zVal.textContent = document.getElementById('z').value;
        len1Val.textContent = document.getElementById('len1').value;
        len2Val.textContent = document.getElementById('len2').value;
        len3Val.textContent = document.getElementById('len3').value;
    }

    function updateResult() {
        const x = parseFloat(document.getElementById('x').value);
        const y = parseFloat(document.getElementById('y').value);
        const z = parseFloat(document.getElementById('z').value);
        const len1 = parseFloat(document.getElementById('len1').value);
        const len2 = parseFloat(document.getElementById('len2').value);
        const len3 = parseFloat(document.getElementById('len3').value);

        fetch('/calculate3d', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ x, y, z, len1, len2, len3 })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                resultDiv.style.display = 'block';
                resultDiv.classList.remove('alert-success');
                resultDiv.classList.add('alert-info');
                resultDiv.textContent = data.message;
            } else {
                resultDiv.style.display = 'block';
                resultDiv.classList.remove('alert-info');
                resultDiv.classList.add('alert-success');
                resultDiv.innerHTML = `
                    <h3><strong>Input:</strong></h3>
                    <p><strong> len1:</strong> ${len1}</p>
                    <p><strong> len2:</strong> ${len2}</p>
                    <p><strong> len3:</strong> ${len3}</p>
                    <h3><strong>Result:</strong></h3>
                    <p><strong>t_abd:</strong> ${data.t_abd.toFixed(2)}</p>
                    <p><strong>t_hip:</strong> ${data.t_hip.toFixed(2)}</p>
                    <p><strong>t_knee:</strong> ${data.t_knee.toFixed(2)}</p>
                    <p><strong>Point 1:</strong> (${data.point1[0].toFixed(2)}, ${data.point1[1].toFixed(2)}, ${data.point1[2].toFixed(2)})</p>
                    <p><strong>Point 2:</strong> (${data.point2[0].toFixed(2)}, ${data.point2[1].toFixed(2)}, ${data.point2[2].toFixed(2)})</p>
                    <p><strong>Point 3:</strong> (${data.point3[0].toFixed(2)}, ${data.point3[1].toFixed(2)}, ${data.point3[2].toFixed(2)})</p>
                `;

                const forward = [
                    [0, data.point1[0], data.point2[0], data.point3[0]],
                    [0, data.point1[1], data.point2[1], data.point3[1]],
                    [0, data.point1[2], data.point2[2], data.point3[2]]
                ];

                drawAnimation(forward);
            }
        })
        .catch(error => console.error('Error:', error));
    }

    function drawAnimation(forward) {
        const x = forward[0];
        const y = forward[1];
        const z = forward[2];

        Plotly.newPlot('myDiv', [{
            type: 'scatter3d',
            mode: 'lines+markers',
            x: x,
            y: y,
            z: z,
            line: {
            width: 6,
            color: ['blue', 'red', 'green'] 
            },
            marker: {
            size: 3.5,
            color: 'black'
            }
        }], {
            width: 800,
            height: 700,
            autosize: false,
            scene: {
            xaxis: { title: 'X', range : [-10, 10] },
            yaxis: { title: 'Y', range: [-10, 10] },
            zaxis: { title: 'Z', range: [-10, 10] },
            camera: {
                up: { x: 0, y: 0, z: 1 },
                center: { x: 0, y: 0, z: 0 },
                eye: { x: 1.25, y: 1.25, z: 1.25 }
            },
            aspectratio: { x: 1, y: 1, z: 0.7 },
            aspectmode: 'manual'
            }
        });
    }

    updateValues();
    updateResult();
});
