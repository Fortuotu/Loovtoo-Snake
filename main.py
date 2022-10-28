import pygame, sys
from settings import *
from snake import Snake
from score import ScorePoint
from menu import *

class Game:

    def __init__(self, screen):
        # important setup
        self.screen = screen
        self.running = True
        self.initialize_game_entities()

        # menu
        self.in_menu = True
        self.in_options = False
        self.paused = False
        self.pressed_esc = False
        
        self.menu_score_points = [MenuScorePoint(self) for _ in range(50)]

        font_file = 'fonts/FFFFORWA.TTF'

        font = pygame.font.Font(font_file, 70)
        self.logo_surface = font.render('Snake-Fight', False, (251, 250, 245))
        self.logo_rect = self.logo_surface.get_rect(center=(SCREEN_WIDTH / 2, 100))
        self.menu_buttons = (
            Button(self.screen, self.play, (SCREEN_WIDTH / 2, 325), 'play', font_file, 50),
            Button(self.screen, self.options, (SCREEN_WIDTH / 2, 450), 'options', font_file, 50),
            Button(self.screen, self.quit, (SCREEN_WIDTH / 2, 575), 'quit', font_file, 50)
        )
        self.paused_buttons = (
            Button(self.screen, self.resume, (SCREEN_WIDTH / 2, 325), 'resume', font_file, 50),
            Button(self.screen, self.menu, (SCREEN_WIDTH / 2, 450), 'menu', font_file, 50),
            Button(self.screen, self.restart, (SCREEN_WIDTH / 2, 575), 'restart', font_file, 50)
        )

        # text
        self.paused_text = font.render('paused', False, (251, 250, 245))
        self.paused_text_rect = self.paused_text.get_rect(center=(SCREEN_WIDTH / 2, 100))

    def initialize_game_entities(self):
        self.snakes = []
        self.snakes.append(Snake(self, (0, SCREEN_HEIGHT / 4 - TILE_SIZE), (0, 255, 0), (TILE_SIZE, 0), fade=20))
        self.snakes.append(Snake(self, (SCREEN_WIDTH - TILE_SIZE, (SCREEN_HEIGHT / 4) * 3), (0, 0, 255), (-TILE_SIZE, 0), keybinds={'Up': pygame.K_i, 'Down': pygame.K_k, 'Left': pygame.K_j, 'Right': pygame.K_l}, fade=20))
        self.score_points = [ScorePoint(self) for _ in range(1)]
    
    def play(self):
        self.in_menu = False
        self.initialize_game_entities()
    
    def restart(self):
        self.paused = False
        self.initialize_game_entities()

    def quit(self):
        self.running = False
    
    def options(self):
        self.in_options = True
    
    def menu(self):
        self.in_menu = True
        self.paused = False
    
    def resume(self):
        for entity in self.snakes + self.score_points:
            entity.transparency = None
        self.paused = False


    def run(self):
        if self.in_menu:
            for msp in self.menu_score_points:
                msp.update()
            if self.in_options:
                pass
            else:
                self.screen.blit(self.logo_surface, self.logo_rect)
                for button in self.menu_buttons:
                    button.update()
        else:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]:
                self.pressed_esc = True
            else:
                if self.pressed_esc:
                    self.pressed_esc = False
                    self.paused = not self.paused
                    if self.paused:
                        for entity in self.snakes + self.score_points:
                            entity.transparency = 50
                    else:
                        for entity in self.snakes + self.score_points:
                            entity.transparency = None

            if not self.paused:
                for entity in self.snakes + self.score_points:
                    entity.update()
            else:
                for entity in self.snakes + self.score_points:
                    entity.draw()
                self.screen.blit(self.paused_text, self.paused_text_rect)
                for button in self.paused_buttons:
                    button.update()
                
def main():

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    game = Game(screen)
    
    while game.running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
        
        game.run()

        pygame.display.update()
        clock.tick(60)
        screen.fill((14, 14, 17))

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()

