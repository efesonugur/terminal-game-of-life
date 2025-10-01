import random
from transforms import random_oriented
from core import stamp, stamp_wrap
from ships import *
from still_lives import *
from oscillators import *

SHIP_PATTERNS = {
    "glider": GLIDER,
    "lwss": LWSS,
    "mwss": MWSS,
    "hwss": HWSS
}
STILL_LIFE_PATTERNS = {
    "block": BLOCK,
    "beehive": BEEHIVE,
    "loaf": LOAF,
    "boat": BOAT,
    "tub": TUB
}
OSCILLATOR_PATTERNS = {
    "blinker": BLINKER,
    "toad": TOAD,
    "beacon": BEACON,
    "pulsar": PULSAR,
    "pentadecathlon": PENTADECATHLON
}

#CAN_PLACE = False

def can_place(board, pattern, top, left):
    rows, cols = len(board), len(board[0])
    for r,c in pattern:
        rr, cc = top + r, left + c
        if not (0 <= rr < rows and 0 <= cc < cols):
            return False
        if board[rr][cc]:
            return False
    return True

def can_place_wrap(board, pattern, top, left):
    rows, cols = len(board), len(board[0])
    for r, c in pattern:
        rr = (top + r) % rows
        cc = (left + c) % cols
        if board[rr][cc]:
            return False
    return True

def place_random_ships(board, count, ship_choices, max_tries=30, wrap=False):
    rows, cols = len(board), len(board[0])
    for _ in range(count):
        kind = random.choice(ship_choices)
        pat = random_oriented(SHIP_PATTERNS[kind])
        placed = False

        if wrap:
            for _t in range(max_tries):
                top = random.randint(0, rows - 1)
                left = random.randint(0, cols - 1)
                if can_place_wrap(board, pat, top, left):
                    stamp_wrap(board, pat, top, left)
                    placed = True
                    break
            if not placed:
                stamp_wrap(board, pat, random.randint(0, rows - 1), random.randint(0, cols - 1))
        else:
            for _t in range(max_tries):
                max_r = rows - max(r for r, c in pat) - 1
                max_c = cols - max(c for r, c in pat) - 1
                if max_r <= 0 or max_c <= 0:
                    break
                top = random.randint(0, max(0, max_r))
                left = random.randint(0, max(0, max_c))
                if can_place(board, pat, top, left):
                    stamp(board, pat, top, left)
                    placed = True
                    break
            if not placed:
                stamp(board, pat, random.randint(0, max(0, rows - 1)),
                      random.randint(0, max(0, cols - 1)))

def place_random_still_lives(board, count, still_life_choices, max_tries=30, wrap=False):
    rows, cols = len(board), len(board[0])
    for _ in range(count):
        kind = random.choice(still_life_choices)
        pat = random_oriented(STILL_LIFE_PATTERNS[kind])
        placed = False
        
        if wrap:
            for _t in range(max_tries):
                top = random.randint(0, rows - 1)
                left = random.randint(0, cols - 1)
                if can_place_wrap(board, pat, top, left):
                    stamp_wrap(board, pat, top, left)
                    placed = True
                    break
            if not placed:
                stamp_wrap(board, pat, random.randint(0, rows - 1), random.randint(0, cols - 1))
        else:
            for _t in range(max_tries):
                max_r = rows - max(r for r, c in pat) - 1
                max_c = cols - max(c for r, c in pat) - 1
                if max_r <= 0 or max_c <= 0:
                    break
                top = random.randint(0, max(0, max_r))
                left = random.randint(0, max(0, max_c))
                if can_place(board, pat, top, left):
                    stamp(board, pat, top, left)
                    placed = True
                    break
            if not placed:
                stamp(board, pat, random.randint(0, max(0, rows - 1)),
                      random.randint(0, max(0, cols - 1)))

def place_random_oscillators(board, count, oscillator_choices, max_tries=30, wrap=False):
    rows, cols = len(board), len(board[0])
    for _ in range(count):
        kind = random.choice(oscillator_choices)
        pat = random_oriented(OSCILLATOR_PATTERNS[kind])
        placed = False

        if wrap:
            for _t in range(max_tries):
                top = random.randint(0, rows - 1)
                left = random.randint(0, cols - 1)
                if can_place_wrap(board, pat, top, left):
                    stamp_wrap(board, pat, top, left)
                    placed = True
                    break
            if not placed:
                stamp_wrap(board, pat, random.randint(0, rows - 1), random.randint(0, cols - 1))
        else:
            for _t in range(max_tries):
                max_r = rows - max(r for r, c in pat) - 1
                max_c = cols - max(c for r, c in pat) - 1
                if max_r <= 0 or max_c <= 0:
                    break
                top = random.randint(0, max(0, max_r))
                left = random.randint(0, max(0, max_c))
                if can_place(board, pat, top, left):
                    stamp(board, pat, top, left)
                    placed = True
                    break
            if not placed:
                stamp(board, pat, random.randint(0, max(0, rows - 1)),
                      random.randint(0, max(0, cols - 1)))

