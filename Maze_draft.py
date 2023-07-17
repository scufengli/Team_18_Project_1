import pygame
import random

# Initialize pygame
pygame.init()

# Set the dimensions of the window
screen_width = 800
screen_height = 800
cell_size = 20

# Set the number of rows and columns in the maze
maze_rows = 20
maze_cols = 20

# Set the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Create the maze grid
maze = [[0] * maze_cols for _ in range(maze_rows)]

# Create a stack to store the visited cells
stack = []

# Set the starting cell
start_row, start_col = 0, 0
maze[start_row][start_col] = 1

# Set the current cell
current_row, current_col = start_row, start_col

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze")

# Generate the maze using recursive backtracking
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                done = True

    screen.fill(BLACK)

    # Mark the current cell as visited
    maze[current_row][current_col] = 1

    # Find unvisited neighbors
    neighbors = []
    if current_row > 1 and maze[current_row - 2][current_col] == 0:
        neighbors.append((-2, 0))
    if current_row < maze_rows - 2 and maze[current_row + 2][current_col] == 0:
        neighbors.append((2, 0))
    if current_col > 1 and maze[current_row][current_col - 2] == 0:
        neighbors.append((0, -2))
    if current_col < maze_cols - 2 and maze[current_row][current_col + 2] == 0:
        neighbors.append((0, 2))

    if len(neighbors) > 0:
        # Choose a random neighbor
        move_row, move_col = random.choice(neighbors)

        # Carve a path to the neighbor
        maze[current_row + move_row // 2][current_col + move_col // 2] = 1

        # Push the current cell to the stack
        stack.append((current_row, current_col))

        # Move to the neighbor cell
        current_row += move_row
        current_col += move_col
    elif len(stack) > 0:
        # Backtrack if there are no unvisited neighbors
        current_row, current_col = stack.pop()

    # Draw the maze
    for row in range(maze_rows):
        for col in range(maze_cols):
            if maze[row][col] == 0:
                pygame.draw.rect(screen, WHITE, (col * cell_size, row * cell_size, cell_size, cell_size))

    # Draw the current cell
    pygame.draw.rect(screen, GREEN, (current_col * cell_size, current_row * cell_size, cell_size, cell_size))

    pygame.display.flip()

# Player character variables
player_row, player_col = start_row, start_col

# Game loop for player movement
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Handle keypress events
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        if player_row > 0 and maze[player_row - 1][player_col] == 1:
            player_row -= 1
    elif keys[pygame.K_DOWN]:
        if player_row < maze_rows - 1 and maze[player_row + 1][player_col] == 1:
            player_row += 1
    elif keys[pygame.K_LEFT]:
        if player_col > 0 and maze[player_row][player_col - 1] == 1:
            player_col -= 1
    elif keys[pygame.K_RIGHT]:
        if player_col < maze_cols - 1 and maze[player_row][player_col + 1] == 1:
            player_col += 1

    screen.fill(BLACK)

    # Draw the maze
    for row in range(maze_rows):
        for col in range(maze_cols):
            if maze[row][col] == 0:
                pygame.draw.rect(screen, WHITE, (col * cell_size, row * cell_size, cell_size, cell_size))

    # Draw the current cell
    pygame.draw.rect(screen, GREEN, (current_col * cell_size, current_row * cell_size, cell_size, cell_size))

    # Draw the player character
    pygame.draw.rect(screen, (255, 0, 0), (player_col * cell_size, player_row * cell_size, cell_size, cell_size))

    pygame.display.flip()
