from tetromino import *
from constants import FPS
import random
from constants import DATA_FILE_PATH


class Game:
    def __init__(self, world):
        self.rotation_index = 0
        self.world = world
        self.ticks = 0
        self.speed = FPS*1
        self.score = 0
        self.ghost_tiles = []
        self.highscore = self.get_highscore()
        self.new_tetromino()
        self.draw_tetromino()
    
    def get_highscore(self):
        f = open(DATA_FILE_PATH)
        return int(f.read())

    def add_score(self, value):
        self.score += value

        if self.score > self.highscore:
            self.highscore = self.score
    
    def new_tetromino(self):
        self.base_tetromino = random.choice(BASE_TETROMINOES)
        self.rotation_index = self.base_tetromino.default_index
        self.tetro_x, self.tetro_y = self.world.spawn_pos
        self.tetromino_geometry = self.base_tetromino.rotations[self.rotation_index]
        for row in enumerate(self.tetromino_geometry):
            for tile in enumerate(row[1]):
                x, y = tile[0], row[0]
                if self.world.tiles[self.tetro_y+y][self.tetro_x+x].active_colour != None:
                    self.game_over()
                    return

        self.compute_exposed_tile_list()
        rows_cleared = self.compute_score()
        self.add_score(rows_cleared*10)
        self.score_calculation(rows_cleared)
        self.compute_ghost_tiles()

    def score_calculation(self, score):
        match score:
            case 1:
                return "Single"
            case 2:
                return "Double"
            case 3:
                return "Triple"
            case 4:
                return "Tetris"

    def compute_score(self):
        row_counter = 0
        for row in enumerate(self.world.tiles):
            populated = True
            for tile in row[1]:
                if tile.active_colour == None:
                    populated = False
                    break
            if populated:
                for tile in row[1]:
                    tile.active_colour = None

                row_counter += 1

                for i in range(row[0]-1,0,-1):
                    for tile in enumerate(self.world.tiles[i]):
                        self.world.tiles[i+1][tile[0]].set_active(tile[1].active_colour)

        return row_counter

    def game_over(self):
        for tile in self.ghost_tiles:
            tile.set_active(self.base_tetromino.colour)
            tile.outliner = None
        self.ghost_tiles = []
        for row in self.world.tiles:
            for tile in row:
                tile.set_active(None)
        self.clear_tetromino()
        self.new_tetromino()
        self.score = 0

    def compute_exposed_tile_list(self):

        self.exposed_tile_coords = []

        for row in enumerate(self.tetromino_geometry):
            for tile in enumerate(row[1]):
                x = tile[0]
                y = row[0]
                geometry_node = tile[1]
                coords = [x,y]
                if y < len(self.tetromino_geometry)-1:
                    if self.tetromino_geometry[y+1][x] == 0 and geometry_node == 1:
                        self.exposed_tile_coords.append(coords)
                else:
                    if geometry_node == 1:
                        self.exposed_tile_coords.append(coords)
    
    def snap(self):
        for tile in self.ghost_tiles:
            tile.set_active(self.base_tetromino.colour)
            tile.outliner = None
        self.clear_tetromino()
        self.ghost_tiles = []
        self.new_tetromino()

    def rotate(self):
        self.clear_tetromino()
        if self.rotation_index+1 > len(self.base_tetromino.rotations)-1:
            self.rotation_index = 0
        else:
            self.rotation_index += 1

        delta_tetromino = self.base_tetromino.rotations[self.rotation_index]
        delta_tetromino_right_edge = self.tetro_x + len(delta_tetromino[0])
        if delta_tetromino_right_edge > self.world.grid_width:
            self.tetro_x -= (delta_tetromino_right_edge - self.world.grid_width)
        for row in enumerate(delta_tetromino):
            for tile in enumerate(row[1]):
                x, y = tile[0], row[0]
                if self.world.tiles[self.tetro_y+y][self.tetro_x+x].active_colour != None:
                    return

        self.tetromino_geometry = self.base_tetromino.rotations[self.rotation_index]
        self.compute_exposed_tile_list()
        self.compute_ghost_tiles()
    
    def deccelerate(self):

        for coord in self.exposed_tile_coords:
            x, y = coord[0], coord[1]
            if self.tetro_y+y < self.world.grid_height-1:
                tile_below = self.world.tiles[self.tetro_y+y+1][self.tetro_x+x]
                if (tile_below.active_colour != None):
                    self.new_tetromino()
                    return

            else:
                self.new_tetromino()
                return
            
        self.clear_tetromino()
        
        self.tetro_y += 1

    def compute_ghost_tiles(self):
        for tile in self.ghost_tiles:
            tile.outliner = None
        self.ghost_tiles = []
        found_collision = False
        end = (self.world.grid_height-1)-(self.tetro_y+len(self.tetromino_geometry)-1)
        for i in range(1, end+1):
            for x, y in self.exposed_tile_coords:
                if self.tetro_y+y+i < self.world.grid_height-1:
                    tile_below = self.world.tiles[self.tetro_y+y+i+1][self.tetro_x+x]
                    if (tile_below.active_colour != None):
                        found_collision = True
                        break
                else:
                    found_collision = True
                    break
            if found_collision:
                break
        if found_collision:
            for row in enumerate(self.tetromino_geometry):
                for tile in enumerate(row[1]):
                    if tile[1] == 1:
                        x, y = tile[0], row[0]
                        world_tile = self.world.tiles[self.tetro_y+y+i][self.tetro_x+x]
                        world_tile.outliner = self.base_tetromino.colour
                        self.ghost_tiles.append(world_tile)

    def update(self):
        if self.ticks % self.speed == 0:
            self.deccelerate()

        self.draw_tetromino()
        
        self.ticks += 1

    def translate(self, direction : int):
        dx = self.tetro_x + direction

        if dx + len(self.tetromino_geometry[0]) <= self.world.grid_width and dx >= 0:

            found_collision = False

            for row in enumerate(self.tetromino_geometry):
                for tile in enumerate(row[1]):
                    if tile[1] == 1:
                        x = tile[0]
                        y = row[0]
                        if ((x+direction < 0 or x+direction >= len(self.tetromino_geometry[0]) or self.tetromino_geometry[y][x+direction] != 1) 
                        and (self.world.tiles[self.tetro_y+y][self.tetro_x+x+direction].active_colour != None)):
                            found_collision = True

            if not found_collision:
                self.clear_tetromino()
                self.tetro_x = dx
                self.compute_ghost_tiles()

    def clear_tetromino(self):
        self.modify_tetromino(None)

    def draw_tetromino(self):
        self.modify_tetromino(self.base_tetromino.colour)

    def modify_tetromino(self, state):
        for row in enumerate(self.tetromino_geometry):
            for tile in enumerate(row[1]):
                if tile[1] == 1:
                    x = tile[0]
                    y = row[0]
                    self.world.tiles[self.tetro_y+y][self.tetro_x+x].set_active(state)
