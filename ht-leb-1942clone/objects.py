import pyxel

# This is the player class, it handles the player's movement and shooting
# It also handles the player's health and score
# It also handles the player's death

class Plane:
    # Defines the player plane class
    def __init__(self):
        # u, v indicate the starting coordinates of the sprite
        self.u = 0
        self.v = 0

        # chunk of distance which will be covered by plane during motion
        self.speed = 8

        # dimensions of the sprite
        self.width = 32 
        self.height = 32

        # distance the plane will maintain from bottom edge initially
        bottom_margin = -70
        self.x = pyxel.width/2 - self.width/2
        self.y = pyxel.height - self.height + bottom_margin

        # Indicates status of double bullet bonus
        self.double_bullet = False
        self.double_bullet_timeout_default = 10
        self.double_bullet_timeout = self.double_bullet_timeout_default

        # Coordinates indicating the head of the plane (for bullet)
        self.head_x = 15
        self.head_y = 15

        self.alive = True

        # Indicates if the plane is currently flipping
        self.flipping = 0
        # Total number of flips a player has
        self.total_flips = 6
        # Current flips available
        self.flips = self.total_flips

        # Fallback value
        self.flipping_time_default = 100
        self.flip_frame_rate = 20
        # Total number of frames for flipping (should be a multiple of flip frame rate)
        self.flipping_time = self.flipping_time_default

    def update(self):
        # All ifs instead of elif's to allow diagonal movements
        # Allows movement only if within window dimensions and when plane is not flipping
        if self.flipping == 0:
            # Move left
            if pyxel.btn(pyxel.KEY_LEFT) and (self.x - self.speed) >= 0:
                self.x -= self.speed

            # Move right
            if pyxel.btn(pyxel.KEY_RIGHT) and (self.x + self.speed) <= (pyxel.width - self.width):
                self.x += self.speed

            # Not 0 to prevent upper margin and allow plane to reach top end
            # Move up
            if pyxel.btn(pyxel.KEY_UP) and (self.y - self.speed) >= -self.height + self.speed:
                self.y -= self.speed

            # Move down
            if pyxel.btn(pyxel.KEY_DOWN) and (self.y + self.speed) <= (pyxel.height - self.height):
                self.y += self.speed
        else:
            # Reduce flipping time if plane is flipping
            if self.flipping_time > 0:
                self.flipping_time -= 1

    def draw(self):
        # Draws the plane
        # If the plane is flipping, the plane is drawn with the flipping animation
        if self.flipping == 0:
            # This condition checks whether the plane is flipping and just draws the plane as is if it's not
            pyxel.blt(self.x, self.y, 0, self.u, self.v, self.width, self.height, 0)

        elif self.flipping == 1:
            # This condition checks whether the plane is flipping
            # and draws the plane with the flipping animation if it is
            # The flipping animation is drawn by drawing the plane with different u and v values
            # There are 4 frames in the flipping animation
            # the left flip animation is drawn if the flipping time is greater than 75% of the total flipping time
            # which is the flipping time integer divided by the flip frame rate result
            if (self.flipping_time // self.flip_frame_rate) ==  4:
                u = 8
                v = 34
                w = 16
                h = 32
                pyxel.blt(self.x, self.y, 0, u, v, w, h, 0)

            # The bottom flip if the flipping time is greater than 50% of the total flipping time
            elif (self.flipping_time // self.flip_frame_rate) ==  3:
                u = 0
                v = 96
                w = 32
                h = 32
                pyxel.blt(self.x, self.y, 0, u, v, w, h, 0)

            # The right flip if the flipping time is greater than 25% of the total flipping time
            elif (self.flipping_time // self.flip_frame_rate) ==  2:
                u = 8
                v = 64
                w = 16
                h = 32
                pyxel.blt(self.x, self.y, 0, u, v, w, h, 0)

            # Flip back to normal position if the flipping time is equal to 1
            # This is the last frame of the flipping animation
            # The flipping time is reset to the default value
            elif (self.flipping_time // self.flip_frame_rate) ==  1:
                pyxel.blt(self.x, self.y, 0, self.u, self.v, self.width, self.height, 0)
                self.flipping = 0
                self.flipping_time = self.flipping_time_default
                # We have 6 flips in total and this decrements it by 1 each time the plane flips
                self.flips -= 1

class Bullet:
    # Defines the bullet class which will be used by all of the planes
    def __init__(self, plane_head_x, plane_head_y, u=69, v=85, direction=(0, -1), speed=10):
        self.x = plane_head_x
        self.y = plane_head_y

        self.u = u
        self.v = v

        self.width = 6
        self.height = 6

        # Velocity of bullet
        self.speed = speed

        self.alive = True

        # Damage the bullet will impact 
        self.damage = 10

        # Direction of bullet, default is upwards
        # Note: All directions throughout this code work somewhat like unit vectors.
        # (-1, 0) meaning left, (1, 0) right, etc
        # Available directions are 8. left, right, up, down and 4 diagonals
        self.direction = direction
    
    def update(self):
        # Multiply the speeds in the direction vector to get the actual speed
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

        # Check if bullet is out of boundary
        if (
            # Left boundary check
            self.y < 0 or
            self.y > pyxel.height - self.height or
            self.x < 0 or 
            self.x > pyxel.width - self.width and 
            self.alive
            ):
            # If out of boundary, kill the bullet which will not be drawn in the next function
            self.alive = False

    def draw(self):
        # Draws the bullet fired by the player plane
        # If the bullet is alive
        # If the bullet is not alive, it will not be drawn
        pyxel.blt(self.x, self.y, 0, self.u, self.v, self.width, self.height, 0)

