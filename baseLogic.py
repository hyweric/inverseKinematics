import math

class baseLogic:
    def __init__(self, x, y, len1, len2, angle1, angle2):
        self.xcoord = x 
        self.ycoord = y 
        self.len1 = len1
        self.len2 = len2
        self.angle1 = math.radians(angle1)
        self.angle2 = math.radians(angle2)

    def distFromOrigin(self):
        return math.sqrt(self.xcoord**2 + self.ycoord**2)
    
    def forwardKinematics(self):
        self.xcoord = self.len1 * math.cos(self.angle1) + self.len2 * math.cos(self.angle1 + self.angle2)
        self.ycoord = self.len1 * math.sin(self.angle1) + self.len2 * math.sin(self.angle1 + self.angle2)
    
    def inverseKinematics(self):
        temp = (self.xcoord**2 + self.ycoord**2 - self.len1**2 - self.len2**2) / (2 * self.len1 * self.len2)

        if -1 <= temp <= 1:
            a = math.acos(temp)
            self.angle2 = math.pi - a
            b = math.acos((self.len1**2 + self.xcoord**2 + self.ycoord**2 - self.len2**2) / (2 * self.len1 * math.sqrt(self.xcoord**2 + self.ycoord**2)))
            self.angle1 = math.atan2(self.ycoord, self.xcoord) - b
        else:
            raise ValueError("")
    


if __name__ == "__main__":
    judy = baseLogic(x=70, y=60, len1=100, len2=30, angle1=0, angle2=0)
    judy.inverseKinematics()
    print(math.degrees(judy.angle1), math.degrees(judy.angle2))

