from math import sqrt
from math import hypot
from scipy.spatial import distance as dist
import numpy as np
def midpoint(p1, p2):
    return  int((p1.x+p2.x)/2), int((p1.y+p2.y)/2)

def distance_btw_points(p1, p2):
    return hypot( (p2[0] - p1[0]), (p2[1] - p1[1]) )

