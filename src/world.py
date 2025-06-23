import pygame as pg
from constants import TITLE_FONT, SUBTITLE_FONT

class Tile:

    OUTLINER_THICKNESS = 2
    def __init__(self, grid_x, grid_y, world, colour):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.world = world
        self.size = world.tile_size
        self.pixel_x = self.world.x + self.grid_x*self.size
        self.pixel_y = self.world.y + self.grid_y*self.size
        self.background_colour = colour
        self.outliner = None
        self.active_colour = None

        raw_surface = pg.image.load("res/tetris_block.png").convert()
        self.transformed_surface = pg.transform.smoothscale(raw_surface, (self.size, self.size))
        self.colour_image = pg.Surface(self.transformed_surface.get_size()).convert()
    
    def set_active(self, colour = None):
        self.active_colour = colour
        if colour == None:
            return
        
        self.colour_image.fill(self.active_colour)
        self.final_surf = self.transformed_surface.copy()
        self.final_surf.blit(self.colour_image, (0, 0), special_flags=pg.BLEND_MULT)

    def render(self, screen : pg.Surface):
        if self.active_colour == None:
            pg.draw.rect(screen, self.background_colour, pg.Rect(self.pixel_x, self.pixel_y, self.size, self.size))
            if self.outliner != None:
                bt = Tile.OUTLINER_THICKNESS
                offset = bt//2
                pg.draw.line(screen, self.outliner, (self.pixel_x, self.pixel_y+offset), (self.pixel_x+self.size, self.pixel_y+offset), bt)
                pg.draw.line(screen, self.outliner, (self.pixel_x+offset, self.pixel_y), (self.pixel_x+offset, self.pixel_y+self.size), bt)
                pg.draw.line(screen, self.outliner, (self.pixel_x, self.pixel_y+self.size-offset), (self.pixel_x+self.size, self.pixel_y+self.size-offset), bt)
                pg.draw.line(screen, self.outliner, (self.pixel_x+self.size-offset, self.pixel_y+self.size), (self.pixel_x+self.size-offset, self.pixel_y), bt)
        else:
            screen.blit(self.final_surf, (self.pixel_x, self.pixel_y))

class World:

    def __init__(self):
        window_width = pg.display.get_window_size()[0]
        window_height = pg.display.get_window_size()[1]
        self.update_dimensions(window_width, window_height)
        self.tiles = []
        self.compute_grid()
        self.spawn_pos = (self.grid_width//2, 0)
        
    def update_dimensions(self, window_width : int, window_height : int):
        self.grid_width = 10
        self.grid_height = 20

        self.tile_size = window_height//self.grid_height
        self.width = self.tile_size*self.grid_width
        self.height = self.tile_size*self.grid_height
        self.x = (window_width - self.width)//2
        self.y = (window_height - self.height)//2

    def render_grid_lines(self, screen : pg.Surface):
        LINE_COLOUR = (0, 60, 60)
        for row in range(self.grid_height+1):
            pg.draw.line(screen, LINE_COLOUR, (self.x, self.y+self.tile_size*row), (self.width+self.x, self.y+self.tile_size*row))

        for column in range(self.grid_width+1):
            pg.draw.line(screen, LINE_COLOUR, (self.x+self.tile_size*column, self.y), (self.x+self.tile_size*column, self.height+self.y))

    def compute_grid(self):
        for row in range(self.grid_height):
            self.tiles.append([])
            for column in range(self.grid_width):
                
                if (row+column) % 2 == 0:
                    colour = (7, 0, 56)
                else:
                    colour = (10, 1, 71)

                tile = Tile(column, row, self, colour)
                self.tiles[row].append(tile)

    def render(self, screen : pg.Surface):

        
        

        for row in self.tiles:
            for tile in row:
                tile.render(screen)
        self.render_grid_lines(screen)
