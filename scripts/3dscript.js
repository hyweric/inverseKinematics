function degreesToRadians(degrees) {
    return degrees * (Math.PI / 180);
}

function drawAnimation(forward) {
    var x = forward[0];
    var y = forward[1];
    var z = forward[2];
        
    Plotly.newPlot('myDiv', [{
        type: 'scatter3d',
        mode: 'lines+markers',
        x: x,
        y: y,
        z: z,
        line: {
            width: 6,
            color: 'blue',
            colorscale: "Viridis"
        },
        marker: {
            size: 3.5,
            color: 'green',
            colorscale: "Greens",
            cmin: -20,
            cmax: 50
        }
    }]);
}

document.getElementById('parameter-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(this);

    fetch('/calculate3d', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(result => {
        if (result.hasOwnProperty('message')) {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = result.message;
            resultDiv.style.display = 'block';
            resultDiv.style.backgroundColor = 'tomato';
        } else {
            const len1 = parseFloat(formData.get('len1'));
            const len2 = parseFloat(formData.get('len2'));
            const len3 = parseFloat(formData.get('len3'));
            
            const t1 = result.t_abad;
            const t2 = result.t_hip;
            const t3 = result.t_knee;
            
            const x1 = result.point1[0];
            const y1 = result.point1[1];
            const z1 = result.point1[2];
            const x2 = result.point2[0];
            const y2 = result.point2[1];
            const z2 = result.point2[2];
            const x3 = result.point3[0];
            const y3 = result.point3[1];
            const z3 = result.point3[2];
            
            const forward = [[0, x1, x2, x3], [0, y1, y2, y3], [0, z1, z2, z3]];

            drawAnimation(forward);
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = `Coordinates: (${x1.toFixed(2)}, ${y1.toFixed(2)}, ${z1.toFixed(2)}), (${x2.toFixed(2)}, ${y2.toFixed(2)}, ${z2.toFixed(2)}), (${x3.toFixed(2)}, ${y3.toFixed(2)}, ${z3.toFixed(2)})<br>
                                   Angles: ${t1.toFixed(2)}°, ${t2.toFixed(2)}°, ${t3.toFixed(2)}°`;
            resultDiv.style.display = 'block';
            resultDiv.style.backgroundColor = '';
        }
    });
});
