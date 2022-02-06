from pygame.math import Vector2
from pygame.transform import rotozoom
from utils import get_random_velocity, load_sound, load_sprite, wrap_position


UP = Vector2(0, -1)

class GameObject:

    def __init__(self, position, sprite, velocity):

        self.position = Vector2(position)

        self.sprite = sprite

        self.radius = sprite.get_width() / 2

        self.velocity = Vector2(velocity)



    def draw(self, surface):

        blit_position = self.position - Vector2(self.radius)

        surface.blit(self.sprite, blit_position)


    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)



    def collides_with(self, other_obj):

        distance = self.position.distance_to(other_obj.position)

        return distance < self.radius + other_obj.radius
        
class Spaceship(GameObject):

    def __init__(self, position, create_bullet_callback, level_characteristics):
        global asteroid_no
        asteroid_no=level_characteristics
        self.MAX_SPEED = 100
        ship_no=1
        if level_characteristics==0:
            self.MANEUVERABILITY = 2.5
            self.ACCELERATION = 0.1
            self.BULLET_SPEED = 2.0
            ship_no=1
        if level_characteristics==1:
            self.MANEUVERABILITY = 2.75
            self.ACCELERATION = 0.125
            self.BULLET_SPEED = 2.5
            ship_no=2
        if level_characteristics==2:
            self.MANEUVERABILITY = 3.0
            self.ACCELERATION = 0.15
            self.BULLET_SPEED = 3.0
            ship_no=3
        if level_characteristics==3:
            self.MANEUVERABILITY = 3.25
            self.ACCELERATION = 0.175
            self.BULLET_SPEED = 3.5
            ship_no=4
        if level_characteristics==4:
            self.MANEUVERABILITY = 3.5
            self.ACCELERATION = 0.2
            self.BULLET_SPEED = 4.0
            ship_no=5

        if level_characteristics==5:
            self.MANEUVERABILITY = 3.75
            self.ACCELERATION = 0.225
            self.BULLET_SPEED = 4.5
            ship_no=6

        if level_characteristics==6:
            self.MANEUVERABILITY = 4.0
            self.ACCELERATION = 0.25
            self.BULLET_SPEED = 5.0
            ship_no=7
        if level_characteristics==7:
            self.MANEUVERABILITY = 4.25
            self.ACCELERATION = 0.275
            self.BULLET_SPEED = 5.5
            ship_no=8

        
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("laser")

        # Make a copy of the original UP vector
        self.direction = Vector2(UP)

        #changing name of ship imported
        shipname= 'spaceship'+str(ship_no)

        #reducing size of ship and loading sprite from load_sprite(utils)
        ship = rotozoom(load_sprite(shipname), 0, 0.125)
        super().__init__(position, ship, Vector2(0))
        
    

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def draw(self, surface):

        angle = self.direction.angle_to(UP)

        rotated_surface = rotozoom(self.sprite, angle, 1.0)

        rotated_surface_size = Vector2(rotated_surface.get_size())

        blit_position = self.position - rotated_surface_size * 0.5

        surface.blit(rotated_surface, blit_position)

    def accelerate(self):
        #maximum speed

        self.velocity += self.direction * self.ACCELERATION

    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)
        self.laser_sound.play()


class Asteroid(GameObject):
    def __init__(self, position, create_asteroid_callback, size=3):
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size

        #sizes of asteroid
        size_to_scale = {
            3: 0.3,
            2: 0.2,
            1: 0.1,
        }
        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite("asteroid"), 0, scale)

        super().__init__(position, sprite, get_random_velocity(1, 3))

    def split(self):
        if self.size > 1:
            #2 to 6
            if asteroid_no==0:
                for _ in range(2): #number of asteroids a single asteroid splits into
                    asteroid = Asteroid(
                        self.position, self.create_asteroid_callback, self.size - 1
                    )
                    self.create_asteroid_callback(asteroid)
            if asteroid_no==1:
                for _ in range(2):
                    asteroid = Asteroid(
                        self.position, self.create_asteroid_callback, self.size - 1
                    )
                    self.create_asteroid_callback(asteroid)
            if asteroid_no==2:
                for _ in range(3):
                    asteroid = Asteroid(
                        self.position, self.create_asteroid_callback, self.size - 1
                    )
                    self.create_asteroid_callback(asteroid)
            if asteroid_no==3:
                for _ in range(3):
                    asteroid = Asteroid(
                        self.position, self.create_asteroid_callback, self.size - 1
                    )
                    self.create_asteroid_callback(asteroid)
            if asteroid_no==4:
                for _ in range(4):
                    asteroid = Asteroid(
                        self.position, self.create_asteroid_callback, self.size - 1
                    )
                    self.create_asteroid_callback(asteroid)
            if asteroid_no==5:
                for _ in range(4):
                    asteroid = Asteroid(
                        self.position, self.create_asteroid_callback, self.size - 1
                    )
                    self.create_asteroid_callback(asteroid)
            if asteroid_no==6:
                for _ in range(5):
                    asteroid = Asteroid(
                        self.position, self.create_asteroid_callback, self.size - 1
                    )
                    self.create_asteroid_callback(asteroid)
            if asteroid_no==7:
                for _ in range(5):
                    asteroid = Asteroid(
                        self.position, self.create_asteroid_callback, self.size - 1
                    )
                    self.create_asteroid_callback(asteroid)
                

class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("bullet"), velocity)
    
    def move(self, surface):
        self.position = self.position + self.velocity

