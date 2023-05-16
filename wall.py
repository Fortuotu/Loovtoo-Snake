import pygame
from settings import *
from snake import Snake
from audio_util import *
from main import Game
from score import positions
from random import choice, randint

class Wall:

    def __init__(self, game, pos):
        self.game = game
        self.snakes: list[Snake] = game.snakes
        self.screen = game.screen


        self.rect = pygame.rect.Rect(
            pos[0], pos[1], TILE_SIZE, TILE_SIZE
        )

        
        self.color = (251, 250, 245)

        self.surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.surf.fill(self.color)

        self.transparency = None
    
    def draw(self):
        self.surf.set_alpha(self.transparency)
        self.screen.blit(self.surf, (self.rect.x, self.rect.y))

    def check_collisions(self):
        for snake in self.snakes:
            if snake.rect.topleft == self.rect.topleft:
                self.snakes.remove(snake)
                play_sound_effect('audio/snakeDie.wav')


    def update(self):
        self.check_collisions()
        self.draw()

wall_combinations = (
    ((0, 0), (0, TILE_SIZE), (0, TILE_SIZE * 2), (TILE_SIZE, 0), (TILE_SIZE * 2, 0)),
    ((0, 0), (0, TILE_SIZE), (0, TILE_SIZE * 2), (0, TILE_SIZE * 3), (TILE_SIZE, 0), (TILE_SIZE * 2, 0), (TILE_SIZE * 3, 0)),

    ((0, 0), (0, -TILE_SIZE), (0, -TILE_SIZE * 2), (-TILE_SIZE, 0), (-TILE_SIZE * 2, 0)),
    ((0, 0), (0, -TILE_SIZE), (0, -TILE_SIZE * 2), (0, -TILE_SIZE * 3), (-TILE_SIZE, 0), (-TILE_SIZE * 2, 0), (-TILE_SIZE * 3, 0)),


    ((0, 0), (0, TILE_SIZE), (0, TILE_SIZE * 2)),
    ((0, 0), (0, TILE_SIZE), (0, TILE_SIZE * 2), (0, TILE_SIZE * 3)),

    ((0, 0), (TILE_SIZE, 0), (TILE_SIZE * 2, 0)),
    ((0, 0), (TILE_SIZE, 0), (TILE_SIZE * 2, 0), (TILE_SIZE * 3, 0)),


    ((0, 0), (TILE_SIZE, 0), (TILE_SIZE * 2, 0), (TILE_SIZE * 2, TILE_SIZE), (TILE_SIZE * 2, TILE_SIZE * 2)),
    ((0, 0), (TILE_SIZE, 0), (TILE_SIZE * 2, 0), (TILE_SIZE * 3, 0), (TILE_SIZE * 3, TILE_SIZE), (TILE_SIZE * 3, TILE_SIZE * 2), (TILE_SIZE * 3, TILE_SIZE * 3)),

    ((0, 0), (0, TILE_SIZE), (0, TILE_SIZE * 2), (TILE_SIZE, TILE_SIZE * 2), (TILE_SIZE * 2, TILE_SIZE * 2)),
    ((0, 0), (0, TILE_SIZE), (0, TILE_SIZE * 2), (0, TILE_SIZE * 3), (TILE_SIZE, TILE_SIZE * 3), (TILE_SIZE * 2, TILE_SIZE * 3), (TILE_SIZE * 3, TILE_SIZE * 3)),
)

def add_wall_combination(game: Game):
    while True:
        x, y = choice(positions[0]), choice(positions[1])
        index = randint(0, len(wall_combinations) - 1)

        wall_combination = [(pos[0] + x, pos[1] + y)
                            for pos in wall_combinations[index]]

        for wall_pos in wall_combination:
            for wall in game.walls:
                if wall_pos == wall.rect.topleft:
                    return False

        for wall_pos in wall_combination:
            game.walls.append(Wall(game, (wall_pos[0], wall_pos[1])))
        return True
