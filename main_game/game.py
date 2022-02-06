import pygame
from tkinter import *
from models import Asteroid, Spaceship
from utils import get_random_position, load_sprite, print_text


class Game:

    #minimum area to be left empty while creating asteroids
    MIN_ASTEROID_DISTANCE = 500
    name=None
    def __init__(self, level_characteristics):
        self._init_pygame()
        self.screen = pygame.display.set_mode((900,600))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('assets/fonts/impact.ttf', 64)
        self.message = ""

        self.asteroids = []
        self.bullets = []
        self.spaceship = Spaceship((400, 450), self.bullets.append, level_characteristics)

        #range decides number of asteroids being displayed #2 to 6
        for _ in range(2):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE
                ):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))

    def main_loop(self):

        while True:

            self._handle_input()

            self._process_game_logic()

            message = self._draw()
            if message:
                break
        
        return message


    def _init_pygame(self):

        pygame.init()

        pygame.display.set_caption("Astronomia")


    def _handle_input(self):
        for event in pygame.event.get():
                    if event.type == pygame.QUIT or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                    ):
                        quit()
                    elif (
                        self.spaceship
                        and event.type == pygame.KEYDOWN
                        and event.key == pygame.K_SPACE
                    ):
                        self.spaceship.shoot()

        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects


    def _process_game_logic(self):
        
        for game_object in self._get_game_objects():
            game_object.move(self.screen)
        
        #spaceship is destroyed
        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.spaceship = None
                    self.message = "YOU LOST!"
                    break

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break


        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)
        
        #all asteroids are destroyed
        if not self.asteroids and self.spaceship:
            self.message = "YOU WON!"
            

    def _draw(self):
        global win
        self.screen.blit(self.background, (0, 0))
        global flag
        flag=0
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        #displaying win or loss message on
        if self.message:
            print_text(self.screen, self.message, self.font)
            flag=1

        pygame.display.flip()
        self.clock.tick(60)
        if flag==1:
            pygame.quit()
            pygame.time.delay(4000)
            if self.message == "YOU WON!":
                return "won"
            elif self.message == "YOU LOST!":
                return "lost"
        return False



class Button(object):

    def __init__(self, position, size, color, text):

        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = pygame.Rect((0,0), size)

        font = pygame.font.SysFont(None, 32)
        text = font.render(text, True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = self.rect.center

        self.image.blit(text, text_rect)

        # set after centering text
        self.rect.topleft = position

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return self.rect.collidepoint(event.pos)