#!/usr/bin/env python3
import random
# THE IMPORTANT BIT:
from functions import draw, move

W, H = 10, 6
player_x, player_y = 2, 2 # THIS IS NOT A GLOBAL ANYMORE!

BG_CHARS = ['.', ',', '`', '-', '_', ':', ';', '~', '*', '#', '+', '=', '^']
grid = [[random.choice(BG_CHARS) for _ in range(W)] for _ in range(H)]

while True:
    print("\033c", end='')
    draw(grid, W, H, player_x, player_y) # WE PASS A LOT OF PARAMETER

    key = input("Move: ").lower()
    if key == 'q':
        break
    elif key in ['w', 'a', 's', 'd']:
        dx, dy = 0, 0
        if key == 'w': dy = -1
        elif key == 's': dy = 1
        elif key == 'a': dx = -1
        elif key == 'd': dx = 1
        player_x, player_y = move(dx, dy, player_x, player_y, W, H) # ALSO HERE