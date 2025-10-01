# ---------- Braille rendering ----------
# map local (dr,dc) to dot mask
BRAILLE_MAP = [
    (0,0,0x01),  # dot1
    (1,0,0x02),  # dot2
    (2,0,0x04),  # dot3
    (0,1,0x08),  # dot4
    (1,1,0x10),  # dot5
    (2,1,0x20),  # dot6
    (3,0,0x40),  # dot7
    (3,1,0x80),  # dot8
]

def pad_board(board):
    rows, cols = len(board), len(board[0])
    # pad rows to multiple of 4 and cols to multiple of 2
    pad_r = (4 - (rows % 4)) % 4
    pad_c = (2 - (cols % 2)) % 2
    if pad_r:
        for _ in range(pad_r):
            board.append([0]*cols)
        rows += pad_r
    if pad_c:
        for r in range(rows):
            board[r].extend([0]*pad_c)
        cols += pad_c
    return board

def board_to_braille(board):
    board = pad_board([row[:] for row in board])
    rows, cols = len(board), len(board[0])
    br_rows = rows // 4
    br_cols = cols // 2
    out_lines = []
    for br in range(br_rows):
        line_chars = []
        base_r = br*4
        for bc in range(br_cols):
            base_c = bc*2
            bits = 0
            for dr, dc, mask in BRAILLE_MAP:
                r = base_r + dr
                c = base_c + dc
                if 0 <= r < rows and 0 <= c < cols and board[r][c]:
                    bits |= mask
            ch = chr(0x2800 + bits)
            line_chars.append(ch)
        out_lines.append("".join(line_chars))
    return "\n".join(out_lines)

def render_ansi(board):
    # \x1b[H = cursor home, \x1b[2J = clear screen
    return "\x1b[H\x1b[2J" + board_to_braille(board) + "\n"