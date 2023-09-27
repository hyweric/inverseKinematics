# inverseKinematics
Basic Inverse Kinematics website which gives you one solution after inputting the length of 2 segments and target position on a 2D cartesian coordinate system - 9/27/23 One Day Project 

Relaunched site: [https://inverse-kinematics.onrender.com](https://inverse-kinematics.onrender.com)

Domain Website : http://2dkinematics.mechsim.tech (**EXPIRED**)


<img width="800" alt="image" src="https://github.com/yeetric/inverseKinematics/assets/82407170/b95418ab-782e-4091-ab94-32eccfed3017">


## Usage

#### Inputs
1. Input coordinates (x,y) and length of segments
2. Click update to generate graph and angles
3. Use Zoom In and Zoom Out to scale the graph
4. Click update to apply changes

#### Outputs
- Angle 1: Angle of Line 1 rotation based on 0 degrees (Positive Side of X Axis) -> Counterclockwise as positive
- Angle 2: Angle of Line 2 rotation based on the Angle of Line 1 -> Clockwise as positive
  
  - Note: There may be more than one configuration of the two segments to reach a given point.

## Math
Derivation of Formulas within code
![image](https://github.com/yeetric/inverseKinematics/assets/82407170/ead3f8ba-21d1-44b0-a082-fd9eedcf1ff5)

