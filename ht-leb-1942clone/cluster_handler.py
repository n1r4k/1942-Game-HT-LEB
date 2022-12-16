import pyxel
from random import randint

# This is the class to handle cluster formations of the enemy planes(regular and red)
# The first plane in the list is the leader of the formation
# The leader is the only plane that can move, the rest of the planes follow the leader


class ClusterHandler:
    # Creates cluster formations
    def __init__(self):
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        # The cluster formation is a list of lists, each list is a plane in the formation
        self.cluster_w = 24
        self.cluster_h = 24

        # Generate random x,y coordinates 
        self.cluster_x = randint(0, int(pyxel.width / 2) - self.cluster_w)
        self.cluster_y = randint(0, int(pyxel.height / 2) - self.cluster_h)

        # Determines the cluster size
        self.cluster_size = randint(2, 7)
        self.cluster_list = []

    def generate_cluster(self, Enemy):
        # This is where the cluster formation takes place,
        # it assigns random neighbouring locations relative to the previous coordinates
        # Can create a duplicate and modified method for specific formations
        previous = 0
        for i in range(self.cluster_size):
            # Randomly select a direction from the list
            # The direction is relative to the previous plane in the formation
            if previous == 0:
                # If there is no previous plane, select a random direction as this plane is the leader
                previous = [self.cluster_x, self.cluster_y]
                enemy = Enemy()
                enemy.x, enemy.y = previous
                self.cluster_list.append(enemy)
            else:
                # Select a random direction from the list
                direction = self.directions[randint(0, len(self.directions) - 1)]
                # Add the direction to the previous plane's coordinates
                cluster_x = (direction[0] * previous[0]) + self.cluster_w
                cluster_y = (direction[1] * previous[1]) + self.cluster_h
                # Create a new plane and add it to the formation
                previous = [cluster_x, cluster_y]

                previous = [max(cluster_x, 0), max(cluster_y, 0)]
                previous = [min(previous[0], pyxel.width - self.cluster_w), min(previous[1], (pyxel.height / 2) - self.cluster_h)]
                #
                if previous not in self.cluster_list:
                    enemy = Enemy()
                    enemy.x, enemy.y = previous
                    self.cluster_list.append(enemy)

    # Filter update calls based on wave and enemy type compatibility
    def update(self, wave):
        # Updates the cluster formation based on the wave we are on
        for object in self.cluster_list:
            # This is for the regular enemy plane cluster formation, that moves in a random direction
            if wave == 0 and object.name == "RegularEnemy":
                if object.alive:
                    object.update()
                else:
                    # If plane is dead, remove it from the list
                    self.cluster_list.remove(object)
            #
            elif wave == 1 and object.name == "RedEnemy":
                # This is for the red enemy plane cluster formation,  that moves in a random direction(in circles)
                if object.alive:
                    object.update()
                else:
                    # If plane is dead, remove it from the list
                    self.cluster_list.remove(object)

    def draw(self, wave):
        # Filter draw calls based on wave and enemy type compatibility
        # Draws planes in the cluster formation based on the wave we are on
        # There are two waves, wave 0 is for the regular enemy plane cluster formation
        # wave 1 is for the red enemy plane cluster formation
        # There are other waves, but they are for the bombardier and super bombardier planes
        # These planes are not in a cluster formation, as such we do not implement them here
        for object in self.cluster_list:
            if wave == 0 and object.name == "RegularEnemy":
                if object.alive:
                    # Draws the regular enemies if they are alive
                    object.draw()
            elif wave == 1 and object.name == "RedEnemy":
                if object.alive:
                    # Draws the red enemies if they are alive
                    object.draw()

# Testing
# currently useless
if __name__ == "__main__":
    cluster_handler = ClusterHandler()
    cluster_handler.generate_cluster()
