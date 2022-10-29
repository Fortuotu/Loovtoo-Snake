import pygame
from settings import *
from random import choice, randint

positions = (
    [i for i in range(0, SCREEN_WIDTH, TILE_SIZE)],
    [i for i in range(0, SCREEN_HEIGHT, TILE_SIZE)],
)

colors = (
    (255, 0, 0),
    (255, 165, 0),
    (255, 255, 0),
    (0, 128, 0),
    (0, 0, 255),
    (75, 0, 130),
    (238, 130, 238)
)

class ScorePoint:

    def __init__(self, game):
        self.screen = game.screen
        self.snakes = game.snakes
        self.color = choice(colors)
        
        # powerup stuff
        self.big = False
        self.power_up_target = None
        self.powerup_ticks = 0
        self.powerup_duration = SNAKE_POWERUP_DURATION
        self.last_rainbow_change = 0


        self.transparency = None
        self.surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = pygame.rect.Rect(
            0, 0, 
            TILE_SIZE, TILE_SIZE
        )
        self.reposition()

        self.repositioning_speed = TILE_SIZE

    def check_powerup_timeout(self):
        if self.power_up_target is not None:
            
            self.power_up_target.rainbow_pallete[
                randint(0, len(self.power_up_target.rainbow_pallete) - 1)
            ] = [randint(0, 255) for _ in range(3)]
            self.last_rainbow_change = pygame.time.get_ticks()

            if pygame.time.get_ticks() - self.powerup_ticks >= self.powerup_duration:
                self.power_up_target.speed = SNAKE_SPEED
                self.power_up_target.rainbow_pallete = None
                self.power_up_target.powerup_rainbow = False
                self.power_up_target.powerup_score_entity = None
                self.power_up_target = None
                self.powerup_ticks = 0
                self.powerup_duration = SNAKE_POWERUP_DURATION

    def reposition(self):
        if not randint(0, POWERUP_SPAWNRATE) and self.power_up_target is None:
            self.big = True
        else:
            self.big = False
        self.rect.topleft = (choice(positions[0]),
                            choice(positions[1]))
        self.repositioning_speed = TILE_SIZE
        self.color = choice(colors)

    def check_collision(self):
        for snake in self.snakes:
            if snake.rect.topleft == self.rect.topleft:
                if self.big:
                    if snake.powerup_rainbow:
                        snake.powerup_score_entity.powerup_duration += SNAKE_POWERUP_DURATION
                    else:
                        self.power_up_target = snake
                        self.power_up_target.powerup_score_entity = self
                        self.power_up_target.speed = round(SNAKE_SPEED / 3)
                        self.powerup_ticks = pygame.time.get_ticks()
                        snake.rainbow_pallete = [
                            [randint(0, 255) for _ in range(3)] for _ in range(snake.bodyparts + 1)
                        ]
                        self.last_rainbow_change = pygame.time.get_ticks()
                        self.power_up_target.powerup_rainbow = True
                if snake.fade:
                    snake.one_fade_index *= snake.bodyparts / (snake.bodyparts + 1)
                if snake.powerup_rainbow:
                    snake.rainbow_pallete.append(
                        [randint(0, 255) for _ in range(3)]
                    )
                snake.bodyparts += 1
                self.reposition()

    def draw(self):
        if not self.big:
            surf = pygame.Surface((
                round(TILE_SIZE / 2) + round(self.repositioning_speed / 2), 
                round(TILE_SIZE / 2) + round(self.repositioning_speed / 2)
            ))
        else:
            surf = pygame.Surface((
                round(TILE_SIZE) + round(self.repositioning_speed), 
                round(TILE_SIZE) + round(self.repositioning_speed)
            ))
        surf.set_alpha(self.transparency)
        surf.fill(self.color)
        rect = surf.get_rect()
        rect.center = self.rect.center


        self.screen.blit(surf, rect.topleft)

        if self.repositioning_speed > 0:
            self.repositioning_speed -= TILE_SIZE / 15
        else:
            self.repositioning_speed = 0


    def update(self):
        self.check_collision()
        self.check_powerup_timeout()
        self.draw()



