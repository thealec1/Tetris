import pygame as pg
from constants import *
from world import World
from game import Game

class Main:

    def __init__(self):
        self.screen = pg.display.set_mode((1024, 850), flags=pg.SCALED, vsync=1)
        pg.display.set_caption(WINDOW_TITLE)

        self.clock = pg.time.Clock()
        self.running = True
        self.world = World()
        self.game = Game(self.world)

        self.loop()

    def render_ui(self):
        # self.screen.blit(Main.SCORE_TITLE, (100, 75))
        
        highscore_title = TITLE_FONT.render("High Score", True, (255, 255, 255))
        highscore_value = SUBTITLE_FONT.render(str(self.game.highscore), True, (255, 255, 255))

        score_title = TITLE_FONT.render("Score", True, (255, 255, 255))
        score_value = SUBTITLE_FONT.render(str(self.game.score), True, (255, 255, 255))

        self.screen.blit(highscore_title, (10, 75))
        self.screen.blit(highscore_value, (10, 120))

        self.screen.blit(score_title, (10, 170))
        self.screen.blit(score_value, (10, 205))


        # score_text = SUBTITLE_FONT.render(str(self.game.score), True, (255, 255, 255))
        # self.screen.blit(score_text, (140, 120))
    
    def loop(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        self.game.rotate()
                    if event.key == pg.K_LEFT:
                        self.game.translate(-1)
                    if event.key == pg.K_RIGHT:
                        self.game.translate(1)
                    if event.key == pg.K_SPACE:
                        self.game.snap()

            keys = pg.key.get_pressed()
            if keys[pg.K_DOWN]:
                self.game.deccelerate()
                self.game.update()
            
            self.clock.tick(FPS)

            self.game.update()

            self.screen.fill((0, 0, 0))
            self.world.render(self.screen)
            self.render_ui()
            pg.display.update()

        self.quit()

    def quit(self):
        # Serialize data
        f = open(DATA_FILE_PATH, "r+")
        hs = self.game.highscore
        file_score = int(f.read())
        if hs != file_score:
            f.seek(0)
            f.write(str(hs))
            f.truncate()
        
        # Terminate media library
        pg.quit()

if __name__ == "__main__":
    Main()
