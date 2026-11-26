from math import *

def forward_kinematic(t1,t2,t3):
   
    L1 = 114
    L2 = 162
    L3 = 150
    d1 = 250
    t1 = radians(t1)
    t2 = radians(t2)
    t3 = radians(t3)
    Px = cos(t1)*(L1 +L2*cos(t2)+L3*cos(t2+t3))
    Py = sin(t1)*(L1 +L2*cos(t2)+L3*cos(t2+t3))
    Pz = L2*sin(t2)+L3*sin(t2+t3) +d1
    Px = round(Px,3)
    Py = round(Py,3)
    Pz = round(Pz,3)
    return Px,Py,Pz

def inverse_kinematic(Px,Py,Pz):
    L1 = 114
    L2 = 162
    L3 = 150
    d1 = 250
    t1 = atan2(Py,Px)
    Z = Pz - d1
    R = sqrt(Px*Px + Py*Py) -L1
    D = (Z*Z+R*R-L2*L2-L3*L3)/(2*L2*L3)
    if D < -1 or D > 1:
        print("Ngoai vung lam viec")
        return None
    t3_1 = atan2(-sqrt(1-D*D),D)
    A1 = L2 + L3*cos(t3_1)
    B1 = L3 * sin(t3_1)
    t2_1 = atan2((A1*Z - B1*R),(B1*Z+A1*R))

    t3_2 = atan2(sqrt(1-D*D),D)
    A2 = L2 + L3*cos(t3_2)
    B2 = L3 * sin(t3_2)
    t2_2 = atan2((A2*Z - B2*R),(B2*Z+A2*R))
    t1 = round(degrees(t1),3)
    t2_1 = round(degrees(t2_1),3)
    t3_1 = round(degrees(t3_1),3)
    t2_2 = round(degrees(t2_2),3)
    t3_2 = round(degrees(t3_2),3)
    return t1,t2_1,t3_1,t2_2,t3_2


