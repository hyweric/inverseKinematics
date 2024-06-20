from flask import Flask, request, jsonify, render_template
import math

app = Flask(__name__)

class kin2d:
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

class kin3d:
    def __init__(self, l1, l2, l3):
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3

    def forward_kinematics(self, t_abd, t_hip, t_knee):

        t_abd = math.radians(t_abd)
        t_hip = math.radians(t_hip)
        t_knee = math.radians(t_knee)
        
        # Calculating the positions in 3D space
        x1 = self.l1 * math.cos(t_abd)
        z1 = self.l1 * math.sin(t_abd)
        y1 = 0
        
        x2 = x1 + self.l2 * math.cos(t_abd) * math.cos(t_hip)
        z2 = z1 + self.l2 * math.sin(t_abd) * math.cos(t_hip)
        y2 = self.l2 * math.sin(t_hip)
        
        x3 = x2 + self.l3 * math.cos(t_abd) * math.cos(t_hip + t_knee)
        z3 = z2 + self.l3 * math.sin(t_abd) * math.cos(t_hip + t_knee)
        y3 = y2 + self.l3 * math.sin(t_hip + t_knee)

        return ([x1, x2, x3], [y1, y2, y3], [z1, z2, z3])

    def inverse_kinematics(self, x, y, z):
        L = x**2 + y**2 + z**2
        cos_t3 = (L - self.l1**2 - self.l2**2) / (2 * self.l1 * self.l2)
        t3 = math.acos(cos_t3)
        k1 = self.l1 + self.l2 * cos_t3
        k2 = self.l2 * math.sin(t3)
        t2 = math.atan2(z, math.sqrt(x**2 + y**2)) - math.atan2(k2, k1)
        t1 = math.atan2(y, x)
        return [math.degrees(t1), math.degrees(t2), math.degrees(t3)]

    def combined_kinematics(self, x, y, z):
        inverse = self.inverse_kinematics(x, y, z)
        forward = self.forward_kinematics(inverse[0], inverse[1], inverse[2])
        return {'x1': forward[0][0], 'x2': forward[0][1], 'x3': forward[0][2], 'y1': forward[1][0], 'y2': forward[1][1], 'y3': forward[1][2], 'z1': forward[2][0], 'z2': forward[2][1], 'z3': forward[2][2], 't1': inverse[0], 't2': inverse[1], 't3': inverse[2]}
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate2d', methods=['POST'])
def calculate2d():
    x = float(request.form.get('x'))
    y = float(request.form.get('y'))
    len1 = float(request.form.get('len1'))
    len2 = float(request.form.get('len2'))

    kin1 = kin2d()
    result = kin1.inverseKinematics(x, y, len1, len2)

    return jsonify(result)


@app.route('/calculate3d', methods=['POST'])
def calculate3d():
    x = float(request.form.get('x'))
    y = float(request.form.get('y'))
    z = float(request.form.get('z'))
    l1 = float(request.form.get('len1'))
    l2 = float(request.form.get('len2'))
    l3 = float(request.form.get('len3'))

    kin2 = kin3d(l1, l2, l3)
    result = kin2.combined_kinematics(x, y, z)
    return jsonify(result)

@app.route('/index3dof')
def index3dof():
    return render_template('index3dof.html')

if __name__ == "__main__":
    app.run(debug=True)