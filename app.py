from flask import Flask, request, jsonify, render_template
import math

app = Flask(__name__)

class Kinematics:
    def inverseKinematics(self, x, y, len1, len2):
        temp = (x ** 2 + y ** 2 - len1 ** 2 - len2 ** 2) / (2 * len1 * len2)

        if -1 <= temp <= 1:
            a = math.acos(temp)
            angle2 = math.pi - a
            b = math.acos((len1 ** 2 + x ** 2 + y ** 2 - len2 ** 2) / (2 * len1 * math.sqrt(x ** 2 + y ** 2)))
            angle1 = math.atan2(y, x) - b
            return {'angle1': math.degrees(angle1), 'angle2': math.degrees(angle2)}
        else:
            return {'message': 'Cannot Calculate Angles - Please modify inputs'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
@app.route('/calculate', methods=['POST'])
def calculate():
    x = float(request.form.get('x'))
    y = float(request.form.get('y'))
    len1 = float(request.form.get('len1'))
    len2 = float(request.form.get('len2'))

    kin1 = Kinematics()
    result = kin1.inverseKinematics(x, y, len1, len2)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)