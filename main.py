import pygame, sys
from audio_util import *
from settings import *
from snake import Snake
from score import *
from menu import *
from wall import *
from random import randint

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
        self.font = pygame.font.Font(font_file, 70)


        self.original_logo_surface = self.font.render('Snake-Fight', False, (251, 250, 245))
        self.original_logo_rect = self.original_logo_surface.get_rect(center=(SCREEN_WIDTH / 2, 100))

        self.logo_surface = self.original_logo_surface
        self.logo_rect = self.original_logo_rect
        self.logo_rotation = 0
        self.logo_rotation_speed = 0.1
        self.logo_rotation_direction = 1

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
        self.options_buttons = (
            Button(self.screen, self.options, (85, 65), 'back', font_file, 35),
        )

        # text
        self.paused_text = self.font.render('paused', False, (251, 250, 245))
        self.paused_text_rect = self.paused_text.get_rect(center=(SCREEN_WIDTH / 2, 100))

        # fight starting
        self.fight_start = None
        self.fight_start_timer = 0
        self.fight_start_time = FIGHT_START_TIME
        self.fight_start_time_over = False

    def initialize_game_entities(self):
        self.snakes = []
        self.snakes.append(Snake(self, (0, SCREEN_HEIGHT / 4 - TILE_SIZE), (0, 255, 0), (TILE_SIZE, 0), fade=20))
        self.snakes.append(Snake(self, (SCREEN_WIDTH - TILE_SIZE, (SCREEN_HEIGHT / 4) * 3), (255, 0, 0), (-TILE_SIZE, 0), keybinds={'Up': pygame.K_i, 'Down': pygame.K_k, 'Left': pygame.K_j, 'Right': pygame.K_l}, fade=20))

        self.walls = []

        i = 0
        while i < OBSTACLE_AMOUNT:
            v = add_wall_combination(self)
            if v == True:
                i += 1

        self.score_points = [ScorePoint(self) for _ in range(25)]

        self.entities = self.snakes + self.score_points + self.walls
    
    def play(self):
        self.in_menu = False
        self.initialize_game_entities()

        self.fight_start = pygame.time.get_ticks()
        self.fight_start_time = FIGHT_START_TIME
    
    def restart(self):
        self.paused = False
        set_song('audio/ingameSong.mp3', force=True)
        self.initialize_game_entities()

        self.fight_start = pygame.time.get_ticks()
        self.fight_start_time = FIGHT_START_TIME

    def quit(self):
        self.running = False
    
    def options(self):
        self.in_options = not self.in_options
    
    def menu(self):
        self.in_menu = True
        self.paused = False

        self.fight_start = None
    
    def resume(self):
        for entity in self.entities:
            entity.transparency = None
        self.paused = False
        unpause_song()


    def run(self):

        if self.in_menu:
            set_song('audio/menuSong.mp3')

            
            self.logo_surface = pygame.transform.rotate(self.original_logo_surface, self.logo_rotation)

            self.logo_rect = self.logo_surface.get_rect(center=self.original_logo_rect.center)
            self.logo_rotation += self.logo_rotation_direction * self.logo_rotation_speed

            if abs(self.logo_rotation) > 7:
                if self.logo_rotation_direction == -1:
                    self.logo_rotation_direction = 1
                else:
                    self.logo_rotation_direction = -1


            set_song('audio/menuSong.mp3')
            for msp in self.menu_score_points:
                msp.update()
            if self.in_options:
                for button in self.options_buttons:
                    button.update()
            else:
                self.screen.blit(self.logo_surface, self.logo_rect)
                for button in self.menu_buttons:
                    button.update()
        else:
            keys = pygame.key.get_pressed()

            if self.fight_start_time - (pygame.time.get_ticks() - self.fight_start) > 0:
                pause_song()
                time_text_surface = self.font.render(f'{int(((self.fight_start_time - (pygame.time.get_ticks() - self.fight_start)) + 1000) / 1000)}', False, (251, 250, 245))
                time_text_rect = time_text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
                self.screen.blit(time_text_surface, time_text_rect)

                for entity in self.entities:
                    if entity.transparency != 50:
                        entity.transparency = 50
                    entity.draw()

                self.fight_start_time_over = True

                return
            
            elif self.fight_start_time_over:
                unpause_song()
                for entity in self.entities:
                    entity.transparency = None
                self.fight_start_time_over = False
            
            set_song('audio/ingameSong.mp3')
                
            if len(self.snakes) < 2:
                end_song()

                color_text_by_rgb_value = {
                    (255, 0, 0): 'red',
                    (0, 0, 255): 'blue',
                    (0, 255, 0): 'green'
                }

                self.paused_buttons[1].update()
                self.paused_buttons[2].update()

                if self.snakes != []:
                    winning_snake: Snake = self.snakes[0]

                    text_surface = self.font.render(f'{color_text_by_rgb_value[winning_snake.color]} won', False, winning_snake.color)
                    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, 100))
                else:
                    text_surface = self.font.render(f'draw', False, (251, 250, 245))
                    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, 100))

                self.screen.blit(text_surface, text_rect)

                return

            if keys[pygame.K_ESCAPE]:
                self.pressed_esc = True
            else:
                if self.pressed_esc:
                    self.pressed_esc = False
                    self.paused = not self.paused
                    if self.paused:
                        pause_song()
                        for entity in self.entities:
                            entity.transparency = 50
                    
                    else:
                        unpause_song()
                        for entity in self.entities:
                            entity.transparency = None

            if not self.paused:
                for entity in self.entities:
                    entity.update()
            else:
                for entity in self.entities:
                    entity.draw()
                self.screen.blit(self.paused_text, self.paused_text_rect)
                for button in self.paused_buttons:
                    button.update()
                
def main():

    pygame.init()
    mixer.init()

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

