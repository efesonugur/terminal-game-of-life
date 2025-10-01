import random
from copy import deepcopy

def rotate90(coords):
    # (r,c) -> (-c,r)
    return [(-c, r) for (r, c) in coords]

def mirror_x(coords):
    # mirror vertically
    return [(-r, c) for (r, c) in coords]

def normalize(coords):
    minr = min(r for r,c in coords)
    minc = min(c for r,c in coords)
    return [(r-minr, c-minc) for r,c in coords]

def random_oriented(pattern):
    coords = deepcopy(pattern)
    # 0..3 rotations
    k = random.randint(0,3)
    for _ in range(k):
        coords = rotate90(coords)
    # optional mirror
    if random.choice([True, False]):
        coords = mirror_x(coords)
    coords = normalize(coords)
    return coords