from game_manager import GameManager

# This is the main file that runs the game
# it consists of the game manager class which handles the game logic
# all tied up in a neat little package that can be run from the command line
# or from the IDE, all it needs to run is the App() command at the bottom and it's dependencies

class App:
    # This class is the main class that runs the game
    def __init__(self, width=256, height=256):
        # Initializes the game
        self.width = width
        self.height = height
        # Creates the game manager object which was imported from the game_manager.py file
        self.game_manager = GameManager(self.width, self.height)

    def update(self):
        # Updates the game manager
        self.game_manager.update()

    def draw(self):
        # Draws the game manager
        self.game_manager.draw()

App()
