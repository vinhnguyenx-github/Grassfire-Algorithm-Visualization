import pygame
import numpy
import sys
from queue import Queue

pygame.init()
pygame.display.set_caption('Grassfire Algorithm Visualization')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (34, 255, 0)
BLUE = (0, 42, 255)
YELLOW = (255, 255, 0)

class Node:
    def __init__(self, value, row, col, total_rows, total_cols):
        self.value = value
        self.row = row
        self.col = col
        self.total_rows = total_rows
        self.total_cols = total_cols
        self.gap = 30
        self.color = WHITE

    def draw(self, screen):
        if self.value == -5:
            self.color = GREEN
        elif self.value == -2:
            self.color = BLACK
        elif self.value == -8:
            self.color = BLUE
        elif self.value == 0:
            self.color = RED
        elif self.value > 0 :
            self.color = YELLOW
        pygame.draw.rect(screen, self.color, (self.col * self.gap, self.row * self.gap, self.gap, self.gap))


class Map:
    def __init__(self, screen, rows, cols):
        self.screen = screen
        self.rows = rows
        self.cols = cols
        self.gap = 30
        self.width = self.cols * self.gap
        self.height = self.rows * self.gap
        self.map = []
        for i in range (self.rows):
            self.map.append([])
            for j in range (self.cols):
                self.map[i].append(-1)
        self.nodes = [[Node(self.map[i][j], i, j, self.rows, self.cols) for j in range(cols)] for i in range(rows)]

    def create_start_node(self, pos):
        self.nodes[0][pos].value = -5

    def create_destination_node(self, pos_y, pos_x):
        self.nodes[pos_y][pos_x].value = 0

    def create_obstacles(self, percent, start_pos, end_pos):
        obstacles = []
        total_nodes = self.cols * self.rows
        total_obstacles = (total_nodes / 100) * percent
        total_obstacles = int(total_obstacles)
        while len(obstacles) <= total_obstacles + 2:
            pos_x = numpy.random.randint(0, self.cols)
            pos_y = numpy.random.randint(0, self.rows)
            position = (pos_x, pos_y)
            if position not in obstacles and pos_x != start_pos and position != end_pos:
                obstacles.append(position)
                self.nodes[pos_y][pos_x].value = -2

    def draw(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.nodes[i][j].draw(self.screen)
        for i in range(self.rows):
            pygame.draw.line(self.screen, BLACK, (0, i * self.gap), (self.width, i * self.gap), 2)
        for j in range(self.cols):
            pygame.draw.line(self.screen, BLACK, (j * self.gap, 0), (j * self.gap, self.height), 2)


def draw(screen, map):
    screen.fill(WHITE)
    map.draw()
    pygame.display.flip()


def grassfire_algorithm(map, start_pos, end_pos):
    queue = Queue()
    queue.put(end_pos)
    visited = set()
    visited.add(end_pos)  
    final_destination_value = []
    clock = pygame.time.Clock()

    while not queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = queue.get()
        neighbors = find_neighbors(map, current)
        value = map.nodes[current[0]][current[1]].value

        for neighbor in neighbors:
            row, col = neighbor
            node = map.nodes[row][col]

            if node.value == -1 and (row, col) not in visited:
                visited.add((row, col))
                queue.put((row, col))
                node.value = value + 1 
                draw(map.screen, map)
                clock.tick(30)

            if (row,col) == start_pos:
                final_destination_value.append(value+1)

    if len(final_destination_value) != 0:
        paths = find_shortest_path(map,start_pos,end_pos,final_destination_value)
        for path in paths:
            map.nodes[path[0]][path[1]].value = -8
            draw(map.screen, map)
            clock.tick(30)
        print(paths)
        return True
    return False

def find_shortest_path(map, start_pos, end_pos, final_destination_value):
    value = min(final_destination_value)
    current = start_pos
    path = []

    while current != end_pos:
        neighbors = find_neighbors(map, current)

        for neighbor in neighbors:
            row, col = neighbor
            if map.nodes[row][col].value == value-1:
                path.append((row, col))
                value -=1
                current = (row, col)
    path.pop()
    return path


def find_neighbors(map, current):
    row, col = current
    neighbors = []

    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_row, new_col = row + dr, col + dc

        if 0 <= new_row < map.rows and 0 <= new_col < map.cols:
            neighbors.append((new_row, new_col))

    return neighbors


def main():
    print("Enter number of rows (>=8)")
    rows = int(input())
    print("Enter number of cols (>=8)")
    cols = int(input())
    print("Enter starting position:")
    start = int(input())
    print("Enter destination's row index")
    pos_y = int(input())
    print("Enter destination's column index")
    pos_x = int(input())
    print("Enter percentage of obstacle cell: ")
    percentage = float(input())
    percentage = int(percentage)
    gap = 30
    screen = pygame.display.set_mode((cols * gap, rows * gap))
    clock = pygame.time.Clock()
    map = Map(screen, rows, cols)
    map.create_start_node(start)
    map.create_destination_node(pos_y, pos_x)
    map.create_obstacles(percentage, start, (pos_y, pos_x))

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    find_path=grassfire_algorithm(map, (0, start), (pos_y, pos_x))
                    if not find_path:
                        print("No path found")

        draw(screen, map)
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
