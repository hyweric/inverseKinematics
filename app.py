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
    def inverseKinematics3d(self, x, y, z, len1, len2, len3):
        L = x**2 + y**2 + z**2
        cos_t3 = (L - len1**2 - len2**2 - len3**2) / (2 * len1 * len2)
        t3 = math.acos(cos_t3)
        k1 = len1 + len2 * cos_t3
        k2 = len2 * math.sin(t3)
        t2 = math.atan2(z, math.sqrt(x**2 + y**2)) - math.atan2(k2, k1)
        t1 = math.atan2(y, x)
        return math.degrees(t1), math.degrees(t2), math.degrees(t3)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    x = float(request.form.get('x'))
    y = float(request.form.get('y'))
    len1 = float(request.form.get('len1'))
    len2 = float(request.form.get('len2'))

    kin1 = Kinematics()
    result = kin1.inverseKinematics(x, y, len1, len2)

    return jsonify(result)


@app.route('/calculate3d', methods=['POST'])
def calculate3d():
    x = float(request.form.get('x'))
    y = float(request.form.get('y'))
    z = float(request.form.get('z'))
    len1 = float(request.form.get('len1'))
    len2 = float(request.form.get('len2'))
    len3 = float(request.form.get('len3'))

    kin1 = Kinematics()
    result = kin1.inverseKinematics3d(x, y, z, len1, len2, len3)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)