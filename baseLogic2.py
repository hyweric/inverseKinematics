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
        
        return (x3, y3, z3)

    def inverse_kinematics(self, x, y, z):
        L = x**2 + y**2 + z**2
        cos_t3 = (L - self.l1**2 - self.l2**2) / (2 * self.l1 * self.l2)
        t3 = math.acos(cos_t3)
        k1 = self.l1 + self.l2 * cos_t3
        k2 = self.l2 * math.sin(t3)
        t2 = math.atan2(z, math.sqrt(x**2 + y**2)) - math.atan2(k2, k1)
        t1 = math.atan2(y, x)
        return math.degrees(t1), math.degrees(t2), math.degrees(t3)

    def plot_kinematics(self, t_abd, t_hip, t_knee, ax):
        t_abd = math.radians(t_abd)
        t_hip = math.radians(t_hip)
        t_knee = math.radians(t_knee)
        
        x1 = self.l1 * math.cos(t_abd)
        z1 = self.l1 * math.sin(t_abd)
        y1 = 0
        
        x2 = x1 + self.l2 * math.cos(t_abd) * math.cos(t_hip)
        z2 = z1 + self.l2 * math.sin(t_abd) * math.cos(t_hip)
        y2 = self.l2 * math.sin(t_hip)
        
        x3 = x2 + self.l3 * math.cos(t_abd) * math.cos(t_hip + t_knee)
        z3 = z2 + self.l3 * math.sin(t_abd) * math.cos(t_hip + t_knee)
        y3 = y2 + self.l3 * math.sin(t_hip + t_knee)
        
        ax.clear()
        ax.plot([0, x1, x2, x3], [0, y1, y2, y3], [0, z1, z2, z3], 'ro-')
        ax.set_xlim([-self.l1 - self.l2 - self.l3, self.l1 + self.l2 + self.l3])
        ax.set_ylim([-self.l1 - self.l2 - self.l3, self.l1 + self.l2 + self.l3])
        ax.set_zlim([-self.l1 - self.l2 - self.l3, self.l1 + self.l2 + self.l3])

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_aspect('auto')
        plt.draw()

def update(val):
    x = slider_x.val
    y = slider_y.val
    z = slider_z.val
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
