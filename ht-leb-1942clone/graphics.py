import pyxel
from random import randint


class Background:
    # Defines the background class which will be used by all the planes
    # The background is a 256x256 image
    def __init__(self):
        # Sets the stars to be drawn, also used code from the shooter game example in the docs
        self.stars = []
        self.create_objects()

        for i in range(100):
            # Creates 100 stars with random x,y coordinates and random speeds
            # The speed is used to determine the color of the star
            # The speed is also used to determine how fast the star moves(self-explanatory)
            self.stars.append(
                (
                    pyxel.rndi(0, pyxel.width - 1),
                    pyxel.rndi(0, pyxel.height - 1),
                    pyxel.rndf(1, 2.5),
                )
            )

    def create_objects(self):
        # Creates the objects for the background
        # The objects are the moon, planet with asteroid belt and little far away galaxies
        moon = [randint(0, int(pyxel.width / 3)), 0]
        planet = [randint(moon[0] + 20, 2 * int(pyxel.width / 3)), 0]
        galaxy = [randint(planet[0] + 20, pyxel.width), 0]

        self.moon_speed = randint(1, 3)
        self.planet_speed = randint(1, 3)
        self.galaxy_speed = randint(1, 3)

        self.objects = [moon, planet, galaxy]

    def update(self):
        # Updates the stars
        for i, (x, y, speed) in enumerate(self.stars):
            # Moves the stars, also taken from the shooter game example, but modified
            y += speed
            # If the star goes off the screen, it is reset to the top
            if y >= pyxel.height:
                y -= pyxel.height
            self.stars[i] = (x, y, speed)

        self.objects[0][1] += self.moon_speed
        self.objects[1][1] += self.galaxy_speed
        self.objects[2][1] += self.planet_speed

        if self.objects[0][1] > pyxel.height and self.objects[1][1] > pyxel.height and self.objects[2][1] > pyxel.height:
            # Resets the objects if they are off the screen
            self.objects.clear()
            self.create_objects()

    def draw(self):
        # Draws the stars
        for (x, y, speed) in self.stars:
            # Draws the stars set as pixels on the screen, with the color depending on speed of the pixel
            # Also taken from the shooter game example
            pyxel.pset(x, y, 12 if speed > 1.8 else 5)

        pyxel.blt(self.objects[0][0], self.objects[0][1], 1, 24, 0, 20, 20)
        pyxel.blt(self.objects[1][0], self.objects[1][1], 1, 48, 0, 20, 20)
        pyxel.blt(self.objects[2][0], self.objects[2][1], 1, 0, 24, 20, 20)


class Blast:
    # This class is used to create the blast effect when the player shoots
    # It is also used to create the blast effect when the player is hit
    def __init__(self, x, y):
        # Sets the blast to be drawn at the given x and y coordinates
        # with the given radius
        self.x = x
        self.y = y

        self.u = 0
        self.v = 0

        self.width = 8
        self.height = 8

        self.alive = True

        self.radius = 4
        self.max_radius = 10

    def update(self):
        # Updates the blast
        # If the blast is at the max radius, it is set to be dead
        if self.radius < self.max_radius:
            self.radius += 1
        else:
            self.alive = False

    def draw(self):
        # Draws the blast
        # which is a circle that gets bigger
        # It is drawn with the pyxel.circ function
        # The pyxel.circb function is used to draw the border of the circle
        if self.radius == self.max_radius:
            # If the blast is at the max radius, it is drawn with a different colour
            pyxel.blt(self.x, self.y, 1, self.u, self.v, self.width, self.height, 0)
        else:
            # If the blast is not at the max radius, it is drawn with a different colour
            pyxel.circ(self.x, self.y, self.radius, 7)
            pyxel.circb(self.x, self.y, self.radius, 10)
