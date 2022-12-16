import pyxel 
from objects import Bullet
from random import randint
from math import sin, cos

# The first class is the parent class from which all other subclasses inherit
# This class is used to define the basic attributes of the enemy craft
# and the methods that are common to all enemy craft

# All enemy craft have a position, a velocity, a size, a health, a score value, and a sprite
# All the following enemy craft take their basic attributes from this class and add their own unique attributes
# Which differentiates them from the other enemy craft such as their health, score value, sprite and shooting pattern


class Enemy:
    # Parent class for all the enemy plane classes
    def find_player(self, plane): 
        # This function is used to find the unit vector which is in the direction of the player
        # This is used to calculate the direction of the bullet fired by the enemy craft

        diff_x = self.x - plane.x  # Difference in x coordinates
        diff_y = self.y - plane.y  # Difference in y coordinates

        if diff_x != 0:
            # If the difference in x coordinates is not 0
            # Calculate the angle between the enemy craft and the player
            # This is done by dividing the difference in y coordinates by the difference in x coordinates
            x = int(diff_x/abs(diff_x))
        else:
            # If the difference in x coordinates is 0
            # Set the x value to 0
            x = 0
        if diff_y != 0:
            # If the difference in y coordinates is not 0
            # Calculate the angle between the enemy craft and the player
            # This is done the exact same way as for the x coordinate above
            y = int(diff_y/abs(diff_y))
        else:
            # If the difference in y coordinates is 0
            # Set the y value to 0
            y = 0

        # x and y are reverse because we need to shoot in opposite direction (towards the player)
        # The unit vector is returned
        # This is used to calculate the direction of the bullet fired by the enemy craft
        self.player_direction = (-x, -y)

    def draw(self):
        # Draws the enemy craft
        # If the enemy craft is alive
        # If it isn't alive, it won't be drawn
        pyxel.blt(self.x, self.y, 0, self.u, self.v, self.width, self.height, 0)
        for bullet in self.bullet_list:
            # Draws all the bullets fired by the enemy craft
            # If the bullet is alive
            if bullet.alive:
                bullet.draw()


class RegularEnemy(Enemy):
    # This is the class that handles the regular enemy craft (the one that moves in a straight line)
    def __init__(self):
        self.u = 32
        self.v = 0

        # Name is used to filter out drawing during specific waves
        self.name = "RegularEnemy"

        # Points awarded when the enemy is destroyed (by a bullet)
        self.points = 5

        self.width = 24
        self.height = 24

        # List of all the bullets spawned by enemy
        self.bullet_list = []
        self.bullet_speed = 5

        self.x = 0
        self.y = 0

        # This determines how often the bullet is shot.
        # The bigger the number, lesser is the frequency (because it takes that much time to loop back to 0)
        self.shoot_speed = 20

        self.alive = True

        # Unit vector directing towards the player plane

        self.player_direction = (0, 0)

        # Direction of the plane itself
        self.direction = 1
        # Used to make some planes move in the forward direction
        self.direction_fixed = False

    def update(self):
        # Updates the enemy craft
        # Bullet firing mechanism
        if pyxel.frame_count % self.shoot_speed == 0:
            # If the frame count is a multiple of the shoot speed
            # Create a bullet object
            # Append it to the bullet list
            # Set the bullet's position to the enemy craft's position
            # Set the bullet's velocity to the unit vector pointing towards the player
            # Multiply the unit vector by the bullet speed to get the actual velocity
            self.bullet_list.append(Bullet(self.x, self.y, 69, 101, direction=self.player_direction, speed=self.bullet_speed))

        # Checks if the plane has reached midway through the screen
        # (vertically) and a has a chance of reversing direction
        # (chance determined by randint)

        if self.y > ((pyxel.height / 2) - self.height) and self.direction_fixed is False:
            # If the enemy craft has reached the halfway point
            # And the direction is not fixed
            # Set the direction to a random value
            # This is done to make some planes move in the forward direction
            # And some move in the reverse direction
            self.direction = [-1, 1][randint(0, 1)]
            self.direction_fixed = True

        if self.direction == 1:
            # If the direction is 1, the plane moves down
            self.x += 1
            self.y += 1
        else:
            # If the direction is -1, the plane moves up
            self.y -= 1
            self.x += 1

        # Alive is false if the plane goes out of bounds
        # The bounds are determined by the size of the plane or the size of the screen which ever is reached
        if self.x < 0 or self.y < 0 or self.x > (pyxel.width - self.width) or self.y > (pyxel.height - self.height):
            self.alive = False

        for bullet in self.bullet_list:
            # Updates all the bullets fired by the enemy craft
            # If the bullet is alive
            # Update the bullet
            # If the bullet is not alive
            # Remove the bullet from the list
            if bullet.alive:
                bullet.update()
            else:
                self.bullet_list.remove(bullet)


class RedEnemy(Enemy):
    # This is the class that handles the red enemy craft (the one that moves in a cluster)
    # This is the same as the regular enemy craft except for the name and the points
    # The name is used to filter out drawing during specific waves
    # The points are used to determine the score
    # The points are also used to determine the number of bullets fired by the enemy craft
    def __init__(self, direction=(0, 1)):
        # Direction is the direction in which the enemy craft moves
        # It is a unit vector
        # It is used to calculate the velocity of the enemy craft
        # It is also used to calculate the direction of the bullet fired by the enemy craft
        self.u = 32
        self.v = 32

        self.name = "RedEnemy"

        self.points = 10
        # Points are used to determine the number of bullets fired by the enemy craft
        self.width = 32
        self.height = 24

        self.bullet_list = []
        # List of all the bullets spawned by enemy
        self.bullet_speed = 5

        self.x = 0
        self.y = 0

        self.radius = 25
        # Here the last element is used to store a constant
        self.direction = [0, 0, 0]
        # This is the direction in which the enemy craft moves
        self.direction_fixed = False
        # This is used to make some planes move in the forward direction
        # And some move in the reverse direction
        self.speed = 0.08
        # This is the speed at which the enemy craft moves
        self.shoot_speed = 60
        # This determines how often the bullet is shot.

        self.alive = True
        # This is used to determine if the enemy craft is alive or not

        self.player_direction = (0, 0)

    def update(self):
        # This is the bullet firing mechanism for red enemy planes, it fires a bullet in the direction of the player
        if pyxel.frame_count % self.shoot_speed == 0:
            # This is the exact same code as the regular enemy craft
            self.bullet_list.append(Bullet(self.x, self.y, 69, 101, direction=self.player_direction, speed=self.bullet_speed))

        # This is the movement mechanism for the red enemy planes
        t = (pyxel.frame_count % 240) * self.speed

        if not self.direction_fixed:
            # If the direction is not fixed
            # Set the direction to a random value
            # This is done to make some planes move in the forward direction
            # And some move in the reverse direction
            self.direction[2] = self.x
            self.direction[1] = self.y
            self.direction_fixed = True

        # This is the exact same code as the regular enemy craft
        self.direction[0] = (pyxel.frame_count % pyxel.width) + self.direction[2]

        # Function for circular motion, We used the equation of a circle to find the x and y coordinates
        # This is inspired by how the shooter game in the documentation works as the enemies moved along a sine wave
        # But to add and make the red enemy planes move more interestingly like the game, they move in a circle
        self.x = self.direction[0] + sin(t) * self.radius
        self.y = self.direction[1] + cos(t) * self.radius

        # Setting this to True causes a bug, as they don't appear after one iteration
        # if self.x < 0 or self.y < 0 or self.x > (pyxel.width - self.width) or self.y > (pyxel.height - self.height):
            # self.alive = False
            # pass

        for bullet in self.bullet_list:
            # This is the exact same code as the regular enemy craft
            if bullet.alive:
                bullet.update()
            else:
                self.bullet_list.remove(bullet)

class Bombardier(Enemy):
    # This is the class that handles the bombardier enemy craft
    # This is the same as the regular enemy craft except for the name and the points
    def __init__(self):
        # Most of the init function is the same as the rest of the planes, except for the name and the points
        # which determine the score and the number of bullets fired by the enemy craft
        self.u = 32
        self.v = 56

        self.points = 20

        self.width = 32
        self.height = 24

        self.bullet_list = []
        self.bullet_speed = 5

        # HP of the plane
        self.health = 30

        self.x = 0
        self.y = 0
        # This is the direction in which the bombardier craft moves
        self.direction_list = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        self.direction = self.direction_list[0]
        self.distance = 15
        self.count = 0

        self.speed = 2
        self.shoot_speed = 15

        self.alive = True

        self.player_direction = (0, 0)

    def update(self):
        # Same as the other ones conceptually
        # This is the bullet firing mechanism for the bombardier planes
        if pyxel.frame_count % self.shoot_speed == 0:
            self.bullet_list.append(Bullet(self.x, self.y, 69, 101, direction=self.player_direction, speed=self.bullet_speed))

        # Add motion here
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

        # Square motion
        if self.y >= (pyxel.height / 2 - self.height) and self.direction == [0, 1]:
            # If the plane is in the bottom half of the screen and is moving down
            self.direction = [1, 0]

        elif self.x >= (pyxel.width - self.width) and self.direction == [1, 0]:
            # If the plane is in the right half of the screen and is moving right
            self.direction = [0, -1]

        elif self.y <= 0 and self.direction == [0, -1]:
            # If the plane is in the top half of the screen and is moving up
            self.direction = [-1, 0]

        elif self.x <= 0 and self.direction == [-1, 0]:
            # If the plane is in the left half of the screen and is moving left
            self.direction = [0, 1]

        if self.x < 0 or self.y < 0 or self.x > (pyxel.width - self.width) or self.y > (pyxel.height - self.height):
            # If the plane is out of bounds
            # Kill the plane
            self.alive = False

        for bullet in self.bullet_list:
            # Same as the other ones
            if bullet.alive:
                bullet.update()
            else:
                self.bullet_list.remove(bullet)

class SuperBombardier(Enemy):
    # This is the class that handles the super bombardier enemy craft
    def __init__(self):
        self.u = 32
        self.v = 88

        self.points = 50

        self.width = 32
        self.height = 32

        self.bullet_list = []
        self.bullet_speed = 2

        self.health = 100

        self.x = 0
        self.y = 0

        # Direction matrix for the bullets
        self.direction_list = [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [-1, -1], [1, -1], [-1, 1]]
        self.direction = self.direction_list[0]

        self.speed = 1
        self.shoot_speed = 30

        self.alive = True

        # self.player_direction = (0, 0)

    # To override the inherited method, as we don't need player coordinate finder function here
    def find_player(self, plane):
        pass

    def update(self):
        # Bullets for 8 possible directions
        # It allows the bullets to be fired in all 8 directions at the same time
        # Which differentiates it from the other planes the most(other than the sprite)
        if pyxel.frame_count % self.shoot_speed == 0:
            self.bullet_list.append(Bullet(self.x + (self.width / 2), self.y + (self.height / 2), 69, 101, direction=self.direction_list[0], speed=self.bullet_speed))
            self.bullet_list.append(Bullet(self.x + (self.width / 2), self.y + (self.height / 2), 69, 101, direction=self.direction_list[1], speed=self.bullet_speed))
            self.bullet_list.append(Bullet(self.x + (self.width / 2), self.y + (self.height / 2), 69, 101, direction=self.direction_list[2], speed=self.bullet_speed))
            self.bullet_list.append(Bullet(self.x + (self.width / 2), self.y + (self.height / 2), 69, 101, direction=self.direction_list[3], speed=self.bullet_speed))
            self.bullet_list.append(Bullet(self.x + (self.width / 2), self.y + (self.height / 2), 69, 101, direction=self.direction_list[4], speed=self.bullet_speed))
            self.bullet_list.append(Bullet(self.x + (self.width / 2), self.y + (self.height / 2), 69, 101, direction=self.direction_list[5], speed=self.bullet_speed))
            self.bullet_list.append(Bullet(self.x + (self.width / 2), self.y + (self.height / 2), 69, 101, direction=self.direction_list[6], speed=self.bullet_speed))
            self.bullet_list.append(Bullet(self.x + (self.width / 2), self.y + (self.height / 2), 69, 101, direction=self.direction_list[7], speed=self.bullet_speed))

        # This is the motion of the super bombardier plane
        # It moves in a criss-cross pattern
        # The criss-cross motion is achieved by changing the direction of the plane
        # Every 15 frame
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

        # This is to make sure that the plane doesn't go out of bounds
        # It checks if the plane is out of bounds by checking if the plane is in the top left corner of the screen or
        # The bottom right corner of the screen
        # or if the plane is in the top right corner of the screen or the bottom left corner of the screen
        if self.y >= (pyxel.height / 2 - self.height) and self.direction in [[0, 1], [-1, 1], [-1, 0]]:
            self.direction = [[0, -1], [1, -1], [1, 0]][randint(0, 2)]

        elif self.x >= (pyxel.width - self.width) and self.direction in [[1, 0], [1, 1], [0, 1]]:
            self.direction = [[-1, 0], [-1, -1], [0, -1]][randint(0, 2)]

        elif self.y <= 0 and self.direction in [[0, -1], [1, -1], [1, 0]]:
            self.direction = [[0, 1], [-1, 1], [-1, 0]][randint(0, 2)]

        elif self.x <= 0 and self.direction in [[-1, 0], [-1, -1], [0, -1]]:
            self.direction = [[1, 0], [1, 1], [0, 1]][randint(0, 2)]


        self.x = max(0, self.x)
        self.y = max(0, self.y)
        self.x = min(pyxel.width - self.width, self.x)
        self.y = min(pyxel.height - self.height, self.y)

        # Again commented out because we don't ever want the bombardier to be destroyed unless its by bullets
        #if self.x < 0 or self.y < 0 or self.x > (pyxel.width - self.width) or self.y > (pyxel.height - self.height):
            # self.alive = False
            # pass

        # Same as always, I maybe could've made a method for this just once but I didn't design this well enough
        for bullet in self.bullet_list:
            if bullet.alive:
                bullet.update()
            else:
                self.bullet_list.remove(bullet)

