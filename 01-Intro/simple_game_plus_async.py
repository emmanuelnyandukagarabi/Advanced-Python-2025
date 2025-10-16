#!/usr/bin/env python3
# ASCII movement with randomized background + async 60s countdown
# Uses only: random, threading, time

import random
import threading
import time

W, H = 10, 6
player_x, player_y = 2, 2
remaining = 60  # seconds

# Allowed background characters (non-alphanumeric)
BG_CHARS = [',', '`', '-', '_', ':', ';', '~', '*', '#', '+', '=', '^', '.']

# Generate random background
grid = [[random.choice(BG_CHARS) for _ in range(W)] for _ in range(H)]

# Sync drawing from multiple threads
print_lock = threading.Lock()
stop_event = threading.Event()

def draw():
    with print_lock:
        print("\033c", end='')  # clear screen
        print(f"⏳ Time left: {remaining:2d}s")
        for y in range(H):
            row = []
            for x in range(W):
                row.append('@' if (x == player_x and y == player_y) else grid[y][x])
            print(''.join(row))
        print("Use W/A/S/D to move, Q to quit")

def move(dx, dy):
    global player_x, player_y
    nx, ny = player_x + dx, player_y + dy
    if 0 <= nx < W and 0 <= ny < H:
        player_x, player_y = nx, ny

def countdown():
    global remaining
    # tick every second until 0 or stop
    while not stop_event.is_set() and remaining > 0:
        time.sleep(1)
        remaining -= 1
        draw()
    if remaining == 0:
        stop_event.set()
        draw()
        with print_lock:
            print("\n⏰ Time's up!")

def main():
    # start timer thread
    t = threading.Thread(target=countdown, daemon=True)
    t.start()

    # input-driven movement
    while not stop_event.is_set():
        draw()
        key = input("Move: ").strip().lower()[:1]  # take first char
        if key == 'q':
            stop_event.set()
            break
        elif key == 'w': move(0, -1)
        elif key == 's': move(0,  1)
        elif key == 'a': move(-1, 0)
        elif key == 'd': move(1,  0)

    t.join(timeout=0.5)
    with print_lock:
        print("\n👋 Bye!")

if __name__ == "__main__":
    main()
