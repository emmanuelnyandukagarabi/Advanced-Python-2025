#!/usr/bin/env python3
# ASCII movement with randomized background + async 60s countdown
# Adds inventory toggle with 'I' (open/close)
# Minimal imports: random, threading, time

import random
import threading
import time

W, H = 10, 6
player_x, player_y = 2, 2
remaining = 60  # seconds

# Inventory (mockup)
inventory_open = False
inventory_items = ["Sword", "Shield", "Leather Armor", "Health Potion", "Torch", "Rope"]

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
        # Map
        for y in range(H):
            row = []
            for x in range(W):
                row.append('@' if (x == player_x and y == player_y) else grid[y][x])
            print(''.join(row))
        # Help
        print("W/A/S/D = move, I = inventory, Q = quit")
        # Inventory panel
        if inventory_open:
            print("-" * W)
            print("Inventory:")
            for i, item in enumerate(inventory_items, 1):
                print(f"  {i}. {item}")
            print("(Press I again to close)")

def move(dx, dy):
    global player_x, player_y
    nx, ny = player_x + dx, player_y + dy
    if 0 <= nx < W and 0 <= ny < H:
        player_x, player_y = nx, ny

def countdown():
    global remaining
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
    global inventory_open
    t = threading.Thread(target=countdown, daemon=True)
    t.start()

    while not stop_event.is_set():
        draw()
        key = input("Action: ").strip().lower()[:1]
        if key == 'q':
            stop_event.set()
            break
        elif key == 'i':
            inventory_open = not inventory_open
        elif not inventory_open:  # ignore movement while inventory open
            if key == 'w': move(0, -1)
            elif key == 's': move(0,  1)
            elif key == 'a': move(-1, 0)
            elif key == 'd': move(1,  0)

    t.join(timeout=0.5)
    with print_lock:
        print("\n👋 Bye!")

if __name__ == "__main__":
    main()
