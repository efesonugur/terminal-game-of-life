#!/usr/bin/env python3
"""
braille_life.py

Run: python3 braille_life.py
Options: --rows --cols --ships --still_lives --oscillators --gens --delay --seed --bake --outfile
"""

import argparse
import random
import sys
import time
import shutil

from core import *
from render import render_ansi
from place_patterns import *


# ---------- Bake to file ----------
def bake_frames(board, gens, outfile, wrap=False):
    delim = "@@FRAME@@\n"

    with open(outfile, "w", encoding="utf-8") as f:
        for i in range(gens):
            f.write(delim)
            f.write(render_ansi(board))
            board = next_gen(board, wrap=wrap)

    print(f"Wrote {outfile} with {gens} frames.")

# ---------- Live runner ----------
def run_live(board, gens, delay, wrap=False):
    # Enter alternate screen buffer and hide cursor
    sys.stdout.write("\x1b[?1049h")  # switch to alternate buffer
    sys.stdout.write("\x1b[2J")      # clear alt buffer
    sys.stdout.write("\x1b[?25l")    # hide cursor
    sys.stdout.flush()

    try:
        for i in range(gens):
            sys.stdout.write(render_ansi(board))
            sys.stdout.flush()
            time.sleep(delay)
            board = next_gen(board, wrap=wrap)
    finally:
        # Restore cursor and return to normal buffer
        sys.stdout.write("\x1b[?25h")  # show cursor
        sys.stdout.write("\x1b[?1049l")  # back to normal buffer
        sys.stdout.flush()


# ---------- CLI & main ----------
def parse_args():
    p = argparse.ArgumentParser()
    term_cols, term_lines = shutil.get_terminal_size((80,24))
    # each braille char = 2 logical cols, 4 logical rows
    default_cols = term_cols * 2
    default_rows = term_lines * 4
    p.add_argument("--rows", type=int, default=default_rows, help="logical pixel rows (multiple of 4 preferred)")
    p.add_argument("--cols", type=int, default=default_cols, help="logical pixel cols (multiple of 2 preferred)")
    p.add_argument("--ships", type=int, default=30, help="how many random spaceships to place")
    p.add_argument("--still_lives", type=int, default=30, help="how many random still lives to place")
    p.add_argument("--oscillators", type=int, default=20, help="how many random oscillators to place")
    p.add_argument("--gens", type=int, default=1000, help="generations to run")
    p.add_argument("--delay", type=float, default=0.06, help="seconds between frames")
    p.add_argument("--seed", type=int, default=None, help="random seed (repeatable)")
    p.add_argument("--bake", action="store_true", help="write baked frames to a file (no live play)")
    p.add_argument("--outfile", type=str, default="braille_life.txt", help="outfile when --bake")
    p.add_argument("--wrap", action="store_true", help="enable toroidal (wrap-around) neighbor logic: edges connect so cells leaving one side reappear on the opposite side.")
    
    return p.parse_args()

def main():
    args = parse_args()
    if args.seed is not None:
        random.seed(args.seed)
    board = empty_board(args.rows, args.cols)

    # clamp counts based on area
    area = args.rows * args.cols
    max_entities = max(1, area // 200)  # heuristic: 1 entity per 200 logical pixels
    ships_count = min(args.ships, max_entities)
    still_count = min(args.still_lives, max_entities)
    osc_count = min(args.oscillators, max_entities)

    

    
    place_random_ships(board, ships_count, list(SHIP_PATTERNS.keys()), wrap=args.wrap)
    place_random_still_lives(board, still_count, list(STILL_LIFE_PATTERNS.keys()), wrap=args.wrap)
    place_random_oscillators(board, osc_count, list(OSCILLATOR_PATTERNS.keys()), wrap=args.wrap)

    if args.bake:
        bake_frames(board, args.gens, args.outfile, wrap=args.wrap)
        print(f"Play with: ./play.sh {args.outfile} {args.delay}")
    else:
        run_live(board, args.gens, args.delay, wrap=args.wrap)

if __name__ == "__main__":
    main()
