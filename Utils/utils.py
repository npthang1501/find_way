import geopy.distance
import numpy as np
import math

def read_data(path_data):
    f = open(path_data, "r")
    ans = []
    N = f.read().split('\n')
    if '\t' in N[0]:
        split_type = '\t'
    else:
        split_type = ' '
    for i in N:
        a = []
        for j in i.split(split_type):
            if '.' in j:
                a.append(float(j))
            else:
                a.append(int(j))
        ans.append(a)
    ans.insert(0, ans[0])
    return ans

# transfer str to long,lat
def str2point(a):
    if ',' in a:
        res = a.split(',')
    else:
        res = a.split(' ')
    return [float(res[0].strip()), float(res[1].strip())]

def distance(u,v):
    return geopy.distance.geodesic(u, v).m

def make_vector(A,B):
    v = []
    for i in range(len(A)):
        v.append(B[i]-A[i])
    return v

def S(p,q,r):
    A = make_vector(p,q)
    B = make_vector(p,r)
    return A[0]*B[1] - A[1]*B[0]

# Returns the unit vector of the vector
def unit_vector(vector):
    return vector / np.linalg.norm(vector)

# Returns the angle between 2 vector
def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))/math.pi*180
