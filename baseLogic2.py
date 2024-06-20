import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

class ThreeDOFKinematics:
    def __init__(self, l1, l2, l3):
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3

    def forward_kinematics(self, t_abd, t_hip, t_knee):
        t_abd = math.radians(t_abd)
        t_hip = math.radians(t_hip)
        t_knee = math.radians(t_knee)

        # First joint position
        x1 = 0
        y1 = self.l1 * math.sin(t_abd)
        z1 = self.l1 * math.cos(t_abd)

        # Second joint position
        x2 = x1 + self.l2 * math.cos(t_hip)
        y2 = y1
        z2 = z1 + self.l2 * math.sin(t_hip)

        # End effector position
        x3 = x2 + self.l3 * math.cos(t_hip + t_knee)
        y3 = y2
        z3 = z2 + self.l3 * math.sin(t_hip + t_knee)

        print("OUTPUT - X3: ", x3, "Y3: ", y3, "Z3: ", z3)
        return (x1, y1, z1), (x2, y2, z2), (x3, y3, z3)

    def inverse_kinematics(self, x, y, z):
        # Inverse kinematics calculations
        t_abd = math.atan2(y, z)

        r = math.sqrt(x**2 + (z - self.l1 * math.cos(t_abd))**2)
        D = (r**2 - self.l2**2 - self.l3**2) / (2 * self.l2 * self.l3)
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
        plt.draw()

def update(val):
    x = slider_x.val - 1 
    y = slider_y.val
    z = slider_z.val
    print("SLIDER X: ", x, "Y: ", y, "Z: ", z)
    t_abd, t_hip, t_knee = kinematics.inverse_kinematics(x, y, z)
    kinematics.plot_kinematics(t_abd, t_hip, t_knee, ax)

kinematics = ThreeDOFKinematics(l1=1, l2=1, l3=1)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax_slider_x = plt.axes([0.25, 0.1, 0.65, 0.03])
ax_slider_y = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_slider_z = plt.axes([0.25, 0.2, 0.65, 0.03])

slider_x = Slider(ax_slider_x, 'X', -2, 2, valinit=0)
slider_y = Slider(ax_slider_y, 'Y', -2, 2, valinit=0)
slider_z = Slider(ax_slider_z, 'Z', -2, 2, valinit=0)

slider_x.on_changed(update)
slider_y.on_changed(update)
slider_z.on_changed(update)

plt.show()
