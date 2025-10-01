def empty_board(rows, cols):
    return [[0]*cols for _ in range(rows)]

def stamp(board, pattern, top, left):
    rows, cols = len(board), len(board[0])
    for r,c in pattern:
        rr = top + r
        cc = left + c
        if 0 <= rr < rows and 0 <= cc < cols:
            board[rr][cc] = 1

def stamp_wrap(board, pattern, top, left):
    rows, cols = len(board), len(board[0])
    for r, c in pattern:
        rr = (top + r) % rows
        cc = (left + c) % cols
        board[rr][cc] = 1


def next_gen(board, wrap=False):
    """
    Compute the next generation.
    If wrap==False: bounded grid (default).
    If wrap==True: toroidal grid (wrap-around edges).
    """
    rows, cols = len(board), len(board[0])
    new = [[0] * cols for _ in range(rows)]

    if wrap:
        for r in range(rows):
            for c in range(cols):
                cnt = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr = (r + dr) % rows
                        nc = (c + dc) % cols
                        cnt += 1 if board[nr][nc] else 0
                if board[r][c] == 1:
                    new[r][c] = 1 if cnt in (2, 3) else 0
                else:
                    new[r][c] = 1 if cnt == 3 else 0
    else:
        for r in range(rows):
            for c in range(cols):
                cnt = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            cnt += 1 if board[nr][nc] else 0
                if board[r][c] == 1:
                    new[r][c] = 1 if cnt in (2, 3) else 0
                else:
                    new[r][c] = 1 if cnt == 3 else 0

    return new
