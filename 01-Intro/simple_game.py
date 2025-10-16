#!/usr/bin/env python3
# Minimal ASCII movement using only input()
# Move with W/A/S/D, quit with Q

W, H = 10, 6
player_x, player_y = 2, 2

def draw():
    for y in range(H):
        for x in range(W):
            if x == player_x and y == player_y:
                print('@', end='')
            else:
                print('.', end='')
        print()
    print("Use W/A/S/D to move, Q to quit")

def move(dx, dy):
    global player_x, player_y
    nx, ny = player_x + dx, player_y + dy
    if 0 <= nx < W and 0 <= ny < H:
        player_x, player_y = nx, ny

while True:
    draw()
    key = input("Move: ").lower()
    if key == 'q':
        break
    elif key == 'w': move(0, -1)
    elif key == 's': move(0, 1)
    elif key == 'a': move(-1, 0)
    elif key == 'd': move(1, 0)
    print("\033c", end='')  # clear screen
