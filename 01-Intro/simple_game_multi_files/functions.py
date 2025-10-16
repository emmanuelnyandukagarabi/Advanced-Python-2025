def move(dx, dy, player_x, player_y, W, H):
    new_x = player_x + dx
    new_y = player_y + dy

    # Keep inside the grid
    new_x = max(0, min(W - 1, new_x))
    new_y = max(0, min(H - 1, new_y))

    return new_x, new_y


def draw(grid, W, H, player_x, player_y):
    for y in range(H):
        for x in range(W):
            if x == player_x and y == player_y:
                print('@', end='')
            else:
                print(grid[y][x], end='')
        print()