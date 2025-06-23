class Tetromino:

    def __init__(self, colour, default_index, rotations):
        self.colour = colour
        self.default_index = default_index
        self.rotations = rotations

I_VERTICAL = [[1],
              [1],
              [1],
              [1]]
I_HORIZONTAL = [[1,1,1,1]]

L_VERTICAL_BOTTOM = [[0,1],
                     [0,1],
                     [1,1]]
L_VERTICAL_TOP = [[1,1],
                  [1,0],
                  [1,0]]
L_HORIZONTAL_BOTTOM = [[1,1,1],
                       [0,0,1]]
L_HORIZONTAL_TOP = [[1,0,0],
                    [1,1,1]]
L_VFLIP_VERTICAL_BOTTOM = [[1,1],
                           [0,1],
                           [0,1]]
L_VFLIP_VERTICAL_TOP = [[1,0],
                        [1,0],
                        [1,1]]
L_VFLIP_HORIZONTAL_BOTTOM = [[0,0,1],
                             [1,1,1]]
L_VFLIP_HORIZONTAL_TOP = [[1,1,1],
                          [1,0,0]]
L_ROTATIONS = [L_VERTICAL_BOTTOM, L_HORIZONTAL_TOP, L_VERTICAL_TOP, L_HORIZONTAL_BOTTOM]
L_ROTATIONS_VFLIP = [L_VFLIP_VERTICAL_BOTTOM, L_VFLIP_HORIZONTAL_TOP, L_VFLIP_VERTICAL_TOP, L_VFLIP_HORIZONTAL_BOTTOM]

T_VERTICAL_TOP = [[0,1,0],
                  [1,1,1]]
T_VERTICAL_BOTTOM = [[1,1,1],
                     [0,1,0]]
T_HORIZONTAL_LEFT = [[1,0],
                     [1,1],
                     [1,0]]
T_HORIZONTAL_RIGHT = [[0,1],
                      [1,1],
                      [0,1]]
T_ROTATIONS = [T_VERTICAL_BOTTOM, T_HORIZONTAL_LEFT, T_VERTICAL_TOP, T_HORIZONTAL_RIGHT]


S_HORIZONTAL_RIGHT = [[0,1,1],
                      [1,1,0]]
S_HORIZONTAL_LEFT = [[1,1,0],
                     [0,1,1]]
S_VERTICAL_TOP = [[0,1],
                  [1,1],
                  [1,0]]
S_VERTICAL_BOTTOM = [[1,0],
                     [1,1],
                     [0,1]]

SKEWED_ROTATIONS = [S_HORIZONTAL_LEFT, S_VERTICAL_TOP, S_HORIZONTAL_RIGHT, S_VERTICAL_BOTTOM]

SQUARE = [[1,1],
          [1,1]]

TETRO_SQUARE = Tetromino(colour=(255, 255, 0), default_index=0, rotations=[SQUARE])
TETRO_I = Tetromino(colour=(0, 255, 255), default_index=0, rotations=[I_HORIZONTAL,I_VERTICAL])
TETRO_L_LEFT = Tetromino(colour=(13, 0, 255), default_index=0, rotations=L_ROTATIONS)
TETRO_L_RIGHT = Tetromino(colour=(255, 170, 0), default_index=2, rotations=L_ROTATIONS_VFLIP)
TETRO_T = Tetromino(colour=(195, 0, 217), default_index=0, rotations=T_ROTATIONS)
TETRO_SKEWED_LEFT = Tetromino(colour=(8, 255, 20), default_index=0, rotations=SKEWED_ROTATIONS)
TETRO_SKEWED_RIGHT = Tetromino(colour=(200, 0, 0), default_index=2, rotations=SKEWED_ROTATIONS)

BASE_TETROMINOES = [TETRO_SQUARE, TETRO_I, TETRO_L_LEFT, TETRO_L_RIGHT, TETRO_T, TETRO_SKEWED_LEFT, TETRO_SKEWED_RIGHT]
