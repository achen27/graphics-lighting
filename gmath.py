import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    normalize(normal)
    normalize(light[0])
    normalize(view)
    Ia = calculate_ambient(ambient, areflect)
    Id = calculate_diffuse(light, dreflect, normal)
    Is = calculate_specular(light, sreflect, view, normal)
    # print(Ia)
    # print(Id)
    # print(Is)
    r = Ia[0] + Id[0] + Is[0]
    g = Ia[1] + Id[1] + Is[1]
    b = Ia[2] + Id[2] + Is[2]
    # print([int(r), int(g), int(b)])
    return [int(r), int(g), int(b)]

def calculate_ambient(alight, areflect):
    r = alight[0] * areflect[0]
    g = alight[1] * areflect[1]
    b = alight[2] * areflect[2]
    return limit_color([r,g,b])

def calculate_diffuse(light, dreflect, normal):
    dp = dot_product(normal,light[0])
    if dp < 0:
        dp = 0
    r = light[1][0] * dreflect[0] * dp
    g = light[1][1] * dreflect[1] * dp
    b = light[1][2] * dreflect[2] * dp
    return limit_color([r,g,b])

def calculate_specular(light, sreflect, view, normal):
    dp1 = dot_product(normal,light[0])
    if dp1 < 0:
        dp1 = 0
    rr = 2 * normal[0] * dp1 - light[0][0]
    rg = 2 * normal[1] * dp1 - light[0][1]
    rb = 2 * normal[2] * dp1 - light[0][2]
    reflect = [rr,rg,rb]
    normalize(reflect)
    dp2 = dot_product(reflect,view)
    if dp2 < 0:
        dp2 = 0
    r = light[1][0] * sreflect[0] * (dp2 ** 4)
    g = light[1][1] * sreflect[1] * (dp2 ** 4)
    b = light[1][2] * sreflect[2] * (dp2 ** 4)
    return limit_color([r,g,b])

def limit_color(color):
    # print(color)
    if color[0] > 255:
        color[0] = 255
    if color[0] < 0:
        color[0] = 0
    if color[1] > 255:
        color[1] = 255
    if color[1] < 0:
        color[1] = 0
    if color[2] > 255:
        color[2] = 255
    if color[2] < 0:
        color[2] = 0
    return color

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    # print(vector)
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude
    # print(vector)

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
