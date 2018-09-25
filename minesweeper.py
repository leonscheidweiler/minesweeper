import pygame

import random

class Board:
    pixel_width            = 0
    pixel_height           = 0
    x_pixel_location       = 0
    y_pixel_location       = 0
    cell_pixel_size        = 0
    gap_pixel_width        = 0
    horizontal_cell_amount = 0
    vertical_cell_amount   = 0
    mine_amount            = 0
    revealed_amount        = 0
    mine_locations         = []
    entries                = []
    
    def __init__(self, horizontal_cell_amount, vertical_cell_amount,
            mine_amount):
        self.horizontal_cell_amount  = horizontal_cell_amount
        self.vertical_cell_amount    = vertical_cell_amount
        self.mine_amount             = mine_amount
        self.revealed_amount         = 0
        self.mine_locations          = [[0, 0] for i in range(mine_amount)]

    def initialize(self):
        self.entries = [[0]*self.vertical_cell_amount\
                for i in range(self.horizontal_cell_amount)]
        for i in range(self.horizontal_cell_amount):
            for j in range(self.vertical_cell_amount):
                self.entries[i][j] = Cell(self, i, j)

    def generate_mines(self):
        self.mine_locations = []
        for mine_id in range(self.mine_amount):
            while True:
                mine_x_location = random.randint(0, self.horizontal_cell_amount-1)
                mine_y_location = random.randint(0, self.vertical_cell_amount-1)
                if [mine_x_location, mine_y_location] not in self.mine_locations:
                    break
            self.mine_locations.append([mine_x_location, mine_y_location])
    
    def set_pixel_geometry(self, x_pixel_location, y_pixel_location,
            cell_size):
        self.x_pixel_location = x_pixel_location
        self.y_pixel_location = y_pixel_location
        self.cell_pixel_size = cell_size
        self.gap_pixel_width = int(0.1*cell_size)
        self.pixel_width = int(self.horizontal_cell_amount*self.cell_pixel_size\
                + self.horizontal_cell_amount*self.gap_pixel_width)
        self.pixel_height = int(self.vertical_cell_amount*self.cell_pixel_size\
                + self.vertical_cell_amount*self.gap_pixel_width)

    def print_entries_to_console(self):
        for j in range(self.horizontal_cell_amount):
            for i in range(self.vertical_cell_amount):
                print(str(playing_board.entries[i][j].value), end=' ')
            print('\n')

    def print_revealed_to_console(self):
        for j in range(self.horizontal_cell_amount):
            for i in range(self.vertical_cell_amount):
                print(str(playing_board.entries[i][j].revealed), end=' ')
            print('\n')

class Cell:
    x_id          = 0
    y_id          = 0
    x_pixel_location = 0
    y_pixel_location = 0
    pixel_size    = 0
    playing_board = 0
    revealed      = False
    flagged       = False
    value         = 0
    neighbors     = []

    def __init__(self, playing_board, x, y):
        self.x_id = x
        self.y_id = y
        self.playing_board = playing_board
        self.revealed = False
        self.flagged  = False
        self.value = 0

    def set_pixel_geometry(self):
        self.pixel_size = playing_board.cell_pixel_size
        self.x_pixel_location = int(
                self.playing_board.x_pixel_location
                + self.x_id * self.pixel_size
                + self.x_id * self.playing_board.gap_pixel_width
                + 0.5 * self.playing_board.gap_pixel_width)
        self.y_pixel_location = int(self.playing_board.y_pixel_location
                + self.y_id * self.pixel_size
                + self.y_id * self.playing_board.gap_pixel_width
                + 0.5 * self.playing_board.gap_pixel_width)

    def reveal(self):
        if not self.flagged:
            self.revealed = True
            self.playing_board.revealed_amount += 1
            if self.value == 0:
                for neighbor in self.neighbors:
                    if not neighbor.revealed:
                        neighbor.reveal()
    
    def toggle_flag(self):
        if not self.revealed:
            self.flagged = not self.flagged
    
    def get_x_pixel_range(self):
        return range(self.x_pixel_location, self.x_pixel_location + self.pixel_size)

    def get_y_pixel_range(self):
        return range(self.y_pixel_location, self.y_pixel_location + self.pixel_size)

    def get_neighbors(self):
        self.neighbors = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                if not self.x_id+i in range(
                        0, playing_board.horizontal_cell_amount):
                    continue
                if not self.y_id+j in range(
                        0, playing_board.vertical_cell_amount):
                    continue
                self.neighbors.append(
                        self.playing_board.entries[self.x_id+i][self.y_id+j])

    def increase_neighbors(self):
        '''This method should be called on all mines exactly once'''
        for neighbor in self.neighbors:
            if neighbor.value != 'm':
                neighbor.value += 1

def find_cell_id(mouse_location):
    clicked_x_id = -1
    clicked_y_id = -1
    for x_id in range(playing_board.horizontal_cell_amount):
        for y_id in range(playing_board.vertical_cell_amount):
            cell = playing_board.entries[x_id][y_id]
            if int(mouse_location[0]) in cell.get_x_pixel_range():
                clicked_x_id = x_id
            if int(mouse_location[1]) in cell.get_y_pixel_range():
                clicked_y_id = y_id
    return [clicked_x_id, clicked_y_id]

################################################################################

playing_board = Board(10, 10, 20)
if playing_board.mine_amount\
        > playing_board.horizontal_cell_amount*playing_board.vertical_cell_amount:
    print('too many mines')
playing_board.initialize()
playing_board.set_pixel_geometry(0, 0, 50)

playing_board.generate_mines()

for i in range(playing_board.horizontal_cell_amount):
    for j in range(playing_board.vertical_cell_amount):
        cell = playing_board.entries[i][j]
        cell.get_neighbors()
        cell.set_pixel_geometry()

for mine in playing_board.mine_locations:
    cell = playing_board.entries[mine[0]][mine[1]]
    cell.value = 'm'
    cell.increase_neighbors()

#playing_board.print_entries_to_console()
#playing_board.print_revealed_to_console()

done = False

WIDTH = playing_board.pixel_width
HEIGHT = playing_board.pixel_height
screen = pygame.display.set_mode([WIDTH, HEIGHT])

pygame.init()
pygame.display.set_caption('Minesweeper')

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, cell.pixel_size)

while not done:
    # EVENT LOOP
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_button = pygame.mouse.get_pressed()
            mouse_location = pygame.mouse.get_pos()
            if mouse_button[0]:
                cell_id = find_cell_id(mouse_location)
                if cell_id[0] != -1 and cell_id[1] != -1:
                    clicked_cell = playing_board.entries[cell_id[0]][cell_id[1]]
                    if not clicked_cell.flagged:
                        clicked_cell.reveal()
                        if clicked_cell.value == 'm':
                            print('You lose!')
                            done = True
                        if playing_board.revealed_amount\
                                == playing_board.horizontal_cell_amount\
                                *playing_board.vertical_cell_amount\
                                - playing_board.mine_amount:
                            print('You win!')
            if mouse_button[2]:
                cell_id = find_cell_id(mouse_location)
                if cell_id[0] != -1 and cell_id[1] != -1:
                    clicked_cell = playing_board.entries[cell_id[0]][cell_id[1]]
                    clicked_cell.toggle_flag()
    
    # GAME LOOP

    # DRAW LOOP
    BLACK = 3*[50]
    DARK  = 3*[150]
    LIGHT = 3*[200]
    RED   = [200, 140, 140]

    screen.fill(BLACK)

    pygame.draw.rect(screen, BLACK, [
        playing_board.x_pixel_location, playing_board.y_pixel_location,
        playing_board.pixel_width, playing_board.pixel_height],
        0)


    for x_id in range(playing_board.horizontal_cell_amount):
        for y_id in range(playing_board.vertical_cell_amount):
            cell = playing_board.entries[x_id][y_id]
            if cell.revealed:
                pygame.draw.rect(screen, DARK, [
                    cell.x_pixel_location, cell.y_pixel_location,
                    cell.pixel_size, cell.pixel_size], 0)
            if not cell.revealed:
                pygame.draw.rect(screen, LIGHT, [
                    cell.x_pixel_location, cell.y_pixel_location,
                    cell.pixel_size, cell.pixel_size], 0)
            if cell.flagged:
                pygame.draw.rect(screen, RED, [
                    cell.x_pixel_location, cell.y_pixel_location,
                    cell.pixel_size, cell.pixel_size], 0)
            if cell.revealed and cell.value != 0:
                text = font.render(str(cell.value), True, BLACK)
                screen.blit(text, [cell.x_pixel_location, cell.y_pixel_location])

    pygame.display.flip()
    clock.tick(100)

#pygame.quit()
