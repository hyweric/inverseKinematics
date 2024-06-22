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

        x1 = 0
        y1 = self.l1 * math.sin(t_abd)
        z1 = self.l1 * math.cos(t_abd)

        x2 = x1 + self.l2 * math.cos(t_hip)
        y2 = y1
        z2 = z1 + self.l2 * math.sin(t_hip)

        x3 = x2 + self.l3 * math.cos(t_hip + t_knee)
        y3 = y2
        z3 = z2 + self.l3 * math.sin(t_hip + t_knee)

        return (x1, y1, z1), (x2, y2, z2), (x3, y3, z3)

    def inverse_kinematics(self, x, y, z):
        # Inverse kinematics calculations
        t_abd = math.atan2(y, z)

        r = math.sqrt(x**2 + (z - self.l1 * math.cos(t_abd))**2)
        D = (r**2 - self.l2**2 - self.l3**2) / (2 * self.l2 * self.l3)
        if D < -1 or D > 1:
            raise ValueError("No valid solutions for the given coordinates")

        t_knee = math.atan2(-math.sqrt(1 - D**2), D)
        t_hip = math.atan2(z - self.l1 * math.cos(t_abd), x) - math.atan2(self.l3 * math.sin(t_knee), self.l2 + self.l3 * math.cos(t_knee))

        # Convert radians to degrees
        t_abd = math.degrees(t_abd)
        t_hip = math.degrees(t_hip)
        t_knee = math.degrees(t_knee)

        return t_abd, t_hip, t_knee

    def plot_kinematics(self, t_abd, t_hip, t_knee, ax):
        points = self.forward_kinematics(t_abd, t_hip, t_knee)

        x_vals = [0, points[0][0], points[1][0], points[2][0]]
        y_vals = [0, points[0][1], points[1][1], points[2][1]]
        z_vals = [0, points[0][2], points[1][2], points[2][2]]

        ax.cla()
        ax.plot(x_vals, y_vals, z_vals, marker='o')
        ax.set_xlim([-2, 2])
        ax.set_ylim([-2, 2])
        ax.set_zlim([-2, 2])

    def combined_kinematics(self, x, y, z): # returns all points and angles
        t_abd, t_hip, t_knee = self.inverse_kinematics(x, y, z)
        points = self.forward_kinematics(t_abd, t_hip, t_knee)
        point1 = points[0]
        point2 = points[1]
        point3 = points[2]
        return {'t_abd': t_abd, 't_hip': t_hip, 't_knee': t_knee, 'point1': point1, 'point2': point2, 'point3': point3}


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