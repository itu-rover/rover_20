import math
import numpy as np
from random import randint
import serial

    # angle between vectors.
def angle(v1, v2, acute = True):
    angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    if (acute == True):
        return angle
    else:
        return 2 * np.pi - angle

def lengths(vector):
    a=math.sqrt((vector[0] ** 2) + (vector[1] ** 2) + (vector[2] ** 2))
    return a
def make_unit(vector):
    len_v = length(vector)
    return [vector[0] / len_v, vector[1] / len_v, vector[2] / len_v]
def scalar_of_vector(vector, scalar):
    return [vector[0] * scalar, vector[1] * scalar, vector[2] * scalar]
def subtract(vector1, vector2):
    return [vector1[0] - vector2[0], vector1[1] - vector2[1], vector1[2] - vector2[2]]

# Triangle Calculations
def cosine_rule(a, b, c):
    cos_theta = (-1 * ((a ** 2) - (b ** 2) - (c ** 2)) / (2 * b * c))
    return math.acos(cos_theta)
def get_triangle_angles(a, b, c):
    return [cosine_rule(a, b, c), cosine_rule(b, a, c), cosine_rule(c, a, b)]
def get_length_from_cos(a, b, theta_in_degrees):
    theta_rad = math.radians(theta_in_degrees)
    return math.sqrt(a * a + b * b - 2 * a * b * math.cos(theta_rad))
