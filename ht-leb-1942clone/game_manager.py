import pyxel
from objects import Plane, Bullet
from enemy import RegularEnemy, RedEnemy, Bombardier, SuperBombardier
from graphics import Blast, Background
from cluster_handler import ClusterHandler

# This class literally acts like a manager and manages the interconnections between all the objects
# This class is the brain of the game while all the other classes are the body
# It merges all the objects together and makes sure they all work together which naturally means
# it has to be the most complex class and the messiest class.


class GameManager:
    # GamaManger class which handles all game objects and their mechanics (update and draw methods)
    def __init__(self, parent_w, parent_h):
        # List of bullets fired by player
        self.player_bullet_list = []
        # Max amount of bullet which can be fired
        self.player_bullet_limit = 5

        # List of blasts to be rendered
        self.blast_list = []

        # List containing red enemy planes destroyed by player
        self.bonus = False

        # Indicates the current scene
        self.scene = "TITLE"

        # Current enemy wave, 0 for regular enemy, 1 for red, 2 for bombardier, 3 for super bombardier
        self.wave = 0

        # Score of the player
        self.score = 0

        # Lives of the player
        self.lives = 3
        # Total lives of the player
        self.total_lives = 3

        #
        pyxel.init(parent_w, parent_h, title="Galaxy King")
        pyxel.load("Assets/asset.pyxres")
            
        # Initalizes the background (stars, planets, etc) object
        self.background = Background()

        # Initalizes the plane object
        self.plane = Plane()

        # Creates the cluster handler
        self.cluster = ClusterHandler()
        # Initalizes the regular enemy object
        self.cluster.generate_cluster(RegularEnemy)
        pyxel.run(self.update, self.draw)

    def update(self):
        # print(len(self.player_bullet_list), len(self.cluster.cluster_list), len(self.blast_list))
        self.background.update()
        # Updates the background object
        if self.scene == "TITLE":
            # If the player presses enter, the game starts
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.scene = "PLAY"

        # All values which were initialized are reset here
        elif self.scene == "GAME_OVER" or self.scene == "WIN":
            # If the player presses enter after dying or winning, the game restarts
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.scene = "PLAY"
                # Resets the plane object
                # The following handles the errors we get when we restart the game and deletes the old plane object
                # and enemies, bullets and blasts
                try:
                    del self.cluster
                except AttributeError:
                    pass
                try: 
                    del self.super_bombardier
                except AttributeError:
                    pass
                try: 
                    del self.cluster
                except AttributeError:
                    pass

                del self.plane

                self.wave = 0
                self.bonus = False
                self.lives = self.total_lives

                self.player_bullet_list.clear()
                self.blast_list.clear()

                self.plane = Plane()
                self.cluster = ClusterHandler()
                self.cluster.generate_cluster(RegularEnemy)

        elif self.scene == "PLAY":
            # Checks if the player is alive
            # If the player is alive, the game continues
            # If the player is dead, the game ends
            if not self.plane.alive:
                self.scene = "GAME_OVER"
                pyxel.cls(0)

            # If the player is alive, it creates the waves of enemies
            # Since the regular enemies always get created, we only need to check for the other waves
            # If the player has destroyed all the enemies in the current wave, the next wave is created
            # If the player has destroyed all the enemies in the last wave, the player wins
            # 0 for regular enemy, 1 for red, 2 for bombardier
            # Create wave 1
            if len(self.cluster.cluster_list) == 0 and self.wave == 0:
                self.wave = 1
                self.cluster.cluster_list.clear()
                self.cluster.generate_cluster(RedEnemy)

            # Create wave 2
            # Since the bombardier is a special enemy, we need to create it separately
            # We also need to check if the player has destroyed all the red enemies
            # But since the bombardier isn't clustered, we don't need to check if the cluster list is empty or
            # generate a new one
            elif len(self.cluster.cluster_list) == 0 and self.wave == 1:
                self.wave = 2
                self.cluster.cluster_list.clear()
                self.bombardier = Bombardier()

            # Updates the player plane motions
            self.plane.update()

            # Bullet shooting mechanism
            if self.plane.flipping == 0:
                # If the player presses space, a bullet is fired
                if self.plane.double_bullet and self.plane.double_bullet_timeout > 0:
                    # If the player has the double bullet powerup, two bullets are fired
                    # The double bullet powerup is only active for a certain amount of time
                    # After that, the powerup is deactivated
                    if pyxel.btnp(pyxel.KEY_X) and len(self.player_bullet_list) < self.player_bullet_limit:
                        self.player_bullet_list.append(Bullet(self.plane.x + self.plane.head_x + 5, self.plane.y + self.plane.head_y))
                        self.player_bullet_list.append(Bullet(self.plane.x + self.plane.head_x - 5, self.plane.y + self.plane.head_y))
                        self.plane.double_bullet_timeout -= 1

                elif self.plane.double_bullet and self.plane.double_bullet_timeout <= 0:
                    # If the player has the double bullet powerup, but the powerup has expired, only one bullet is fired
                    self.plane.double_bullet = False
                    self.plane.double_bullet_timeout = self.plane.double_bullet_timeout_default
                    self.bonus = False

                else:
                    # If the player doesn't have the double bullet powerup, only one bullet is fired
                    if pyxel.btnp(pyxel.KEY_X) and len(self.player_bullet_list) < self.player_bullet_limit:
                        self.player_bullet_list.append(Bullet(self.plane.x + self.plane.head_x, self.plane.y + self.plane.head_y))
                        print(self.bonus)

            # Key for flipping

            if pyxel.btnp(pyxel.KEY_Z) and self.plane.flipping == 0 and self.plane.flips > 0:
                self.plane.flipping = 1

            # Check if enemy has collided with bullet
            for enemy in self.cluster.cluster_list:
                for bullet in self.player_bullet_list:
                    if (
                        # Checks if the bullet is within the enemy's x and y coordinates
                        # If it is, the enemy is destroyed
                        enemy.x + enemy.width > bullet.x
                        and bullet.x + bullet.width > enemy.x
                        and enemy.y + enemy.height > bullet.y
                        and bullet.y + bullet.height > enemy.y
                    ):
                        # If the enemy is destroyed, the bullet is deleted
                        # The enemy is also deleted
                        bullet.alive = False
                        enemy.alive = False

                        #
                        self.score += enemy.points

                        self.blast_list.append(Blast(bullet.x, bullet.y))

                        self.player_bullet_list.remove(bullet)
                        self.cluster.cluster_list.remove(enemy)
                        # If the enemy is a red enemy, the player gets the double bullet powerup
                        if enemy.name == "RedEnemy" and len(self.cluster.cluster_list) == 0 and self.bonus is False:
                            self.bonus = True
                            self.plane.double_bullet = True

            # Blast animations
            for blast in self.blast_list:
                # If the blast animation is over, the blast is deleted
                if blast.alive:
                    blast.update()
                else:
                    self.blast_list.remove(blast)

            # Bullet updater
            for bullet in self.player_bullet_list:
                # If the bullet is still alive, it updates
                # If the bullet is dead, it is deleted
                if bullet.alive:
                    bullet.update()
                else:
                    self.player_bullet_list.remove(bullet)

            # Find player direction and check for bullet collision
            for enemy in self.cluster.cluster_list:
                # If the enemy is still alive, it updates
                enemy.find_player(self.plane)
                for bullet in enemy.bullet_list:
                    if (
                        # Checks if the bullet is within the enemy's x and y coordinates
                        self.plane.x + self.plane.width > bullet.x
                        and bullet.x + bullet.width > self.plane.x
                        and self.plane.y + self.plane.height > bullet.y
                        and bullet.y + bullet.height > self.plane.y
                    ):
                        # If the enemy is destroyed as the bullet is in the enemy's x and y coordinates,
                        # the bullet is deleted
                        bullet.alive = False

                        if self.plane.flipping == 0:
                            # If the player is not flipping, the player is destroyed when hit by a bullet
                            # if he is flipping, the player is invincible in that time
                            if self.lives > 0:
                                self.lives -= 1
                            else:
                                self.plane.alive = False

                        self.blast_list.append(Blast(self.plane.x, self.plane.y))

                    # Plane and enemy collision
                    if (
                        # Checks if the enemy is within the player's x and y coordinates
                        self.plane.x + self.plane.width > enemy.x
                        and enemy.x + enemy.width > self.plane.x
                        and self.plane.y + self.plane.height > enemy.y
                        and enemy.y + enemy.height > self.plane.y
                    ):
                        # If the enemy is destroyed as the player is in the enemy's x and y coordinates,
                        # the enemy is deleted
                        # The player is also destroyed or loses a life
                        enemy.alive = False
                        if self.lives > 0:
                            self.lives -= 1
                        else:
                            self.plane.alive = False
                        # If the player is not flipping, the player is destroyed when hit by an enemy
                        self.blast_list.append(Blast(self.plane.x, self.plane.y))

            # Enemy plane updater
            self.cluster.update(self.wave)

            # Check if player bullet has hit bombardier
            # The following does the same as the above, just modified for the bombardier
            if self.wave == 2:
                for bullet in self.player_bullet_list:
                    if (
                        self.bombardier.x + self.bombardier.width > bullet.x
                        and bullet.x + bullet.width > self.bombardier.x
                        and self.bombardier.y + self.bombardier.height > bullet.y
                        and bullet.y + bullet.height > self.bombardier.y
                    ):
                        # As the bombardier's health is 2, it takes 2 hits to destroy it
                        if self.bombardier.health > 0:
                            self.bombardier.health -= bullet.damage

                        else:
                            # If the bombardier is destroyed, the player gets a bonus
                            self.bombardier.alive = False
                            self.score += self.bombardier.points

                        bullet.alive = False
                        # If the bullet hits the bombardier, the bullet is deleted and the blast list is updated
                        self.blast_list.append(Blast(self.bombardier.x + self.bombardier.width/2, self.bombardier.y + self.bombardier.height/2))

            # Check if player bullet has hit super_bombardier
            if self.wave == 3:
                # The following does the same as the above, just modified for the super bombardier
                for bullet in self.player_bullet_list:
                    if (
                        self.super_bombardier.x + self.super_bombardier.width > bullet.x
                        and bullet.x + bullet.width > self.super_bombardier.x
                        and self.super_bombardier.y + self.super_bombardier.height > bullet.y
                        and bullet.y + bullet.height > self.super_bombardier.y
                    ):
                        # As the super Bombardier's health is 3, it takes 3 hits to destroy it
                        if self.super_bombardier.health > 0:
                            self.super_bombardier.health -= bullet.damage

                        else:
                            self.super_bombardier.alive = False
                            self.score += self.super_bombardier.points

                        bullet.alive = False
                        # If the bullet hits the super bombardier, the bullet is deleted and the blast list is updated
                        # Same as above for bombardier
                        self.blast_list.append(Blast(self.super_bombardier.x + self.super_bombardier.width/2, self.super_bombardier.y + self.super_bombardier.height/2))


            # Check for bombardier bullet collision with player
            if self.wave == 2:
                self.bombardier.find_player(self.plane)
                for bullet in self.bombardier.bullet_list:
                    if (
                        # Checks if the bombardier bullet is within the player's x and y coordinates
                        self.plane.x + self.plane.width > bullet.x
                        and bullet.x + bullet.width > self.plane.x
                        and self.plane.y + self.plane.height > bullet.y
                        and bullet.y + bullet.height > self.plane.y
                    ):
                        # If the player is destroyed as the bullet is in the player's x and y coordinates,
                        # the bullet is deleted
                        # The player is also destroyed or loses a life
                        bullet.alive = False

                        if self.plane.flipping == 0:
                            # If the player is not flipping, the player is destroyed when hit by a bullet
                            if self.lives > 0:
                                self.lives -= 1
                            else:
                                self.plane.alive = False

                        self.blast_list.append(Blast(self.plane.x, self.plane.y))

            # Check for super bombardier bullet collision with player
            if self.wave == 3:
                for bullet in self.super_bombardier.bullet_list:
                    if (
                        self.plane.x + self.plane.width > bullet.x
                        and bullet.x + bullet.width > self.plane.x
                        and self.plane.y + self.plane.height > bullet.y
                        and bullet.y + bullet.height > self.plane.y
                    ):
                        bullet.alive = False

                        if self.plane.flipping == 0:
                            if self.lives > 0:
                                self.lives -= 1
                            else:
                                self.plane.alive = False

                        self.blast_list.append(Blast(self.plane.x, self.plane.y))


            # Player and bombardier collision
            if self.wave == 2:
                if (
                    self.plane.x + self.plane.width > self.bombardier.x
                    and self.bombardier.x + self.bombardier.width > self.plane.x
                    and self.plane.y + self.plane.height > self.bombardier.y
                    and self.bombardier.y + self.bombardier.height > self.plane.y
                ):
                    self.bombardier.alive = False
                    if self.lives > 0:
                        self.lives -= 1
                    else:
                        self.plane.alive = False

                    self.blast_list.append(Blast(self.plane.x, self.plane.y))

            # Player and super bombardier collision
            if self.wave == 3:
                if (
                    self.plane.x + self.plane.width > self.super_bombardier.x
                    and self.super_bombardier.x + self.super_bombardier.width > self.plane.x
                    and self.plane.y + self.plane.height > self.super_bombardier.y
                    and self.super_bombardier.y + self.super_bombardier.height > self.plane.y
                ):
                    self.super_bombardier.alive = False
                    if self.lives > 0:
                        self.lives -= 1
                    else:
                        self.plane.alive = False

                    self.blast_list.append(Blast(self.plane.x, self.plane.y))


            if self.wave == 2:
                if self.bombardier.alive:
                    self.bombardier.update()
                else:
                    del self.bombardier

                    if self.wave == 2:
                        self.wave = 3

                    self.super_bombardier = SuperBombardier()

            if self.wave == 3:
                if self.super_bombardier.alive:
                    self.super_bombardier.update()
                else:
                    del self.super_bombardier

                    if self.wave == 3:
                        self.wave = 0
                        self.cluster.generate_cluster(RegularEnemy)

            if self.plane.y <= 0:
                self.scene = "WIN"

    def draw(self):
        # This function draws all the objects on the screen
        # It also draws the score, lives and flips on the screen
        pyxel.cls(0)

        self.background.draw()

        pyxel.text(0, 0, f"SCORE: {self.score}", 7)
        pyxel.text(pyxel.width - 40, 0, f"LIVES: {self.lives}/{self.total_lives}", 7)
        pyxel.text(0, pyxel.height - 10, f"FLIPS: {self.plane.flips}/{self.plane.total_flips}", 7)

        # The following code checks for the scene and draws the appropriate objects
        if self.scene == "TITLE":
            self.draw_title()
            self.plane.draw()

        elif self.scene == "PLAY":
            if self.plane.alive:
                self.plane.draw()

            for blast in self.blast_list:
                blast.draw()

            for bullet in self.player_bullet_list:
                if bullet.alive:
                    bullet.draw()

            if self.wave == 2:
                if self.bombardier.alive:
                    self.bombardier.draw()

            if self.wave == 3:
                if self.super_bombardier.alive:
                    self.super_bombardier.draw()

            self.cluster.draw(self.wave)

        elif self.scene == "GAME_OVER":
            self.draw_game_over()

        elif self.scene == "WIN":
            self.draw_win()

    # The following functions draw the title, game over and win screens
    def draw_title(self):
        pyxel.text(pyxel.width / 2 - 15, pyxel.height / 2 - 10, "WELCOME", pyxel.frame_count % 16)
        pyxel.text(pyxel.width - 150, pyxel.height - 50, "PRESS ENTER", 13)

    def draw_game_over(self):
        pyxel.text(pyxel.width / 2 - 18, pyxel.height / 2 - 10, "GAME OVER", 7)
        pyxel.text(pyxel.width - 150, pyxel.height - 50, "PRESS ENTER", 13)

    def draw_win(self):
        pyxel.text(pyxel.width / 2 - 50, pyxel.height / 2 - 10, "CONGRATULATIONS! YOU HAVE WON", pyxel.frame_count % 16)
        pyxel.text(pyxel.width - 150, pyxel.height - 50, "PRESS ENTER", 13)

