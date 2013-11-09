#24-3-2010

import pygame, math, sys, os , os.path
from random import randint, choice
from pygame.locals import *
import Pause_Menu, Level_Results, Highscores

screen = pygame.display.set_mode((1024, 768))
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
SCREENRECT = screen.get_rect()
background = pygame.Surface(SCREENRECT.size)


"""
    The following are game and player attributes and initial values
    that can be modified to alter game. Certain enemy atributes change as
    the game progresses
"""
#Game Constants
FRICTION               = 1
ACCELERATION           = 2
TURN_SPEED             = 6
BONUS_ROUND_POS        = ((1024/2)-165,(768/2)-50)
SPACE_START_POS        = ((1024/2)-75,(768/2)+200)
LEVEL_DISP_POS         = ((1024/2)-100,(768/2)-50)
BONUS_START_TIME       = 30
#Player Atributes
PLAYER_MAX_HEALTH      = 500
PLAYER_DAMAGE          = 10
PLAYER_SPEED           = 10
PLAYER_BULLET_SPEED    = 30
LIVES                  = 3
PLAYER_RELOAD          = 200 #in ms
#Saucer Enemy Atributes
SAUCER_START_HEALTH    = 30
SAUCER_SPEED           = 5
SAUCER_RELOAD_TIME     = 1500 #in ms
SAUCER_BULLET_SPEED    = 15
SAUCER_DAMAGE          = 5
SAUCER_POINTS          = 10
#Triangle Enemy Atributes
TRIANGLE_START_HEALTH  = 10
TRIANGLE_SPEED         = 3
TRIANGLE_RELOAD_TIME   = 1500 #in ms
TRIANGLE_BULLET_SPEED  = 10
TRIANGLE_DAMAGE        = 10
TRIANGLE_POINTS        = 20
#Tank Enemy Atributes
TANK_START_HEALTH      = 50
TANK_SPEED             = 1
TANK_RELOAD_TIME       = 5000 #in ms
TANK_BULLET_SPEED      = 30
TANK_DAMAGE            = 20
TANK_POINTS            = 50
TANK_TURN_SPEED        = 4
#Mine Enemy Atributes
MINE_START_HEALTH      = 40
MINE_SPEED             = 4
MINE_RELOAD_TIME       = 3000 #in ms
MINE_DAMAGE            = 50
MINE_POINTS            = 30
MINE_MAX_TURN_SPEED    = 1
MINE_DIRECTION_CHANGE  = 5000 #ms before maybe changing direction
#Trishot Enemy Atributes
TRISHOT_START_HEALTH   = 40
TRISHOT_SPEED          = 3
TRISHOT_RELOAD_TIME    = 2000 #in ms
TRISHOT_BULLET_SPEED   = 20
TRISHOT_DAMAGE         = 20
TRISHOT_POINTS         = 60
TRISHOT_TURN_SPEED     = 4
#Boss Atributes
BOSS_START_HEALTH      = 70
BOSS_SPEED             = 15
BOSS_RELOAD_TIME       = 1000 #in ms
BOSS_BULLET_SPEED      = 20
BOSS_DAMAGE            = 10
BOSS_POINTS            = 200
#Target Atributes
TARGET_POINTS          = 100

#Character Classes
class Player(pygame.sprite.Sprite):
    image = []
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.src_image = self.image[0]
        self.rect = self.src_image.get_rect()

        #start at center
        self.init_position = SCREENRECT.center
        self.rect.move_ip(self.init_position)
        self.position = self.init_position

        #initialize speed and direction variables
        self.speedv = self.speedh = self.direction = 0
        self.k_w = 0
        self.k_a = 0
        self.k_s = 0
        self.k_d = 0
        self.k_left = 0
        self.k_right = 0

        #initialize player variables
        self.health = PLAYER_MAX_HEALTH
        self.hit = False
        self.damage_type = None
        self.alive = True

    def update(self):
        """ Update the player position.
        """
        # Establish vertical speed relative to the Player and set boundries
        if self.speedv > 0:
            self.speedv += (self.k_w + self.k_s) - FRICTION
        elif self.speedv < 0:
            self.speedv += (self.k_w + self.k_s) + FRICTION
        else:
            self.speedv += (self.k_w + self.k_s)

        if self.speedv > PLAYER_SPEED:
            self.speedv = PLAYER_SPEED
        if self.speedv < PLAYER_SPEED * -1:
            self.speedv = PLAYER_SPEED * -1

        # Establish horizontal speed relative to the Player and set boundries
        if self.speedh > 0:
            self.speedh += (self.k_a + self.k_d) - FRICTION
        elif self.speedh < 0:
            self.speedh += (self.k_a + self.k_d) + FRICTION
        else:
            self.speedh += (self.k_a + self.k_d)
        
        if self.speedh > PLAYER_SPEED:
            self.speedh = PLAYER_SPEED
        if self.speedh < PLAYER_SPEED * -1:
            self.speedh = PLAYER_SPEED * -1

        # Establish rotation and movement direction
        self.direction += (self.k_right + self.k_left)
        x, y = self.position
        rad = self.direction * math.pi / 180
        x += (-self.speedv * math.sin(rad)) + (self.speedh * math.sin(rad -
                                                                (math.pi / 2)))
        y += (-self.speedv * math.cos(rad)) + (self.speedh * math.cos(rad -
                                                                (math.pi / 2)))

        # Make screen wrap-around
        if x > screen.get_width() + 50:
            x = -50
        elif x < -50:
            x = screen.get_width() + 50
        if y > screen.get_height() + 50:
            y = -50
        elif y < -50:
            y = screen.get_height() + 50

        # Move to new position
        self.position = (x, y)
        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

        #Check for damage
        if self.hit == True:
            if self.damage_type == 'saucer':
                self.health -= SAUCER_DAMAGE
            elif self.damage_type == 'triangle':
                self.health -= TRIANGLE_DAMAGE
            elif self.damage_type == 'tank':
                self.health -= TANK_DAMAGE
            elif self.damage_type == 'mine':
                self.health -= MINE_DAMAGE
            elif self.damage_type == 'trishot':
                self.health -= TRISHOT_DAMAGE
            elif self.damage_type == 'boss':
                self.health -= BOSS_DAMAGE
            self.damage_type = None
            self.hit = False

        #Cheack for death
        if self.health <= 0:
            self.alive = False
            self.kill()
        
    def gunrot(self):
        return self.direction * math.pi / 180

    def gunpos(self):
        return self.position

class SaucerEnemy(pygame.sprite.Sprite):
    image = []
    def __init__(self, player, level):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.src_image = self.image[0]

        #initialize position
        self.rect = self.src_image.get_rect()
        self.arenax = screen.get_width()
        self.arenay = screen.get_height()
        self.position = (randint(50, self.arenax - 50), randint(50,
                                                            self.arenay - 50))
        self.rect.move_ip(self.position)

        #initialize speed and direction variables
        self.speedv = self.speedh = self.direction = 0
        self.forward = 0
        self.backward = 0
        self.left = 0
        self.right = 0
        self.rleft = 0
        self.rright = 0
        self.angle = 0

        #initialize state variables
        self.health = SAUCER_START_HEALTH + ((int(level) - 1) * 5)
        self.max_health = self.health
        self.reload_time = 0

        #get player location/rotation
        self.player = player
        self.player_pos = (0,0)
        self.player_rot = (0,0)

    def update(self):
        right = (TURN_SPEED * -1)
        left = TURN_SPEED

        self.reload_time += 20
        
        # Get player location/rotation
        self.player_pos = Player.gunpos(self.player)
        self.player_rot = math.degrees(Player.gunrot(self.player))

        #set variables
        angle = 0
        sx,sy = self.position
        px,py = self.player_pos
        dirn = self.direction       
        difx = px - sx
        dify = py - sy
        hyp = math.sqrt((difx ** 2) + (dify ** 2))
        
        #keep player rot within 360
        while self.player_rot > 360:
            self.player_rot -= 360
        while self.player_rot < 0:
            self.player_rot += 360

        #figure out which direction to move
        if sx < px:
            if sy < py:
                if self.player_rot < 45:
                    self.right = -2
                    self.left = 0
                else:
                    self.right = 0
                    self.left = 2
            else:
                if self.player_rot > 90 and self.player_rot < 135:
                    self.right = -2
                    self.left = 0
                else:
                    self.right = 0
                    self.left = 2
        else:
            if sy < py:
                if self.player_rot < 315:
                    self.right = -2
                    self.left = 0
                else:
                    self.right = 0
                    self.left = 2
            else:
                if self.player_rot < 270 and self.player_rot > 225:
                    self.right = -2
                    self.left = 0
                else:
                    self.right = 0
                    self.left = 2
        if hyp < 300:
            self.backward = -2
        elif hyp > 400:
            self.forward = 2
        else:
            self.backward = 0
            self.forward = 0
                    
        
        # Establish vertical speed relative to self
        if self.speedv > 0:
            self.speedv += (self.forward + self.backward) - FRICTION
        elif self.speedv < 0:
            self.speedv += (self.forward + self.backward) + FRICTION
        else:
            self.speedv += (self.forward + self.backward)

        if self.speedv > SAUCER_SPEED:
            self.speedv = SAUCER_SPEED
        if self.speedv < SAUCER_SPEED * -1:
            self.speedv = SAUCER_SPEED * -1
        
        # Establish horizontal speed relative to self
        if self.speedh > 0:
            self.speedh += (self.left + self.right) - FRICTION
        elif self.speedh < 0:
            self.speedh += (self.left + self.right) + FRICTION
        else:
            self.speedh += (self.left + self.right)
        
        if self.speedh > SAUCER_SPEED:
            self.speedh = SAUCER_SPEED
        if self.speedh < SAUCER_SPEED * -1:
            self.speedh = SAUCER_SPEED * -1  

        # Keep angle within 360
        if dirn > 360:
            dirn = 0
        if dirn < 0:
            dirn = 360

        # Get angle to player
        if difx == 0:
            if dify <= 0:
                angle = 0
            else:
                angle = 180
        elif difx < 0:
            if dify <= 0:
                angle = math.degrees(math.asin(math.fabs(difx)/hyp))
            else:
                angle = 180-math.degrees(math.asin(math.fabs(difx)/hyp))
        else:
            if dify >= 0:
                angle = math.degrees(math.asin(math.fabs(difx)/hyp)) + 180
            else:
                angle = 360 - math.degrees(math.asin(math.fabs(difx)/hyp))

        # Decide which direction to turn
        if math.fabs(angle - dirn) >= 6 and math.fabs(angle - dirn) < 180:
            if angle > dirn:
                self.rright = 0
                self.rleft = left
            else:
                self.rright = right
                self.rleft = 0
        elif math.fabs(angle - dirn) >= 180:
            if angle > dirn:
                self.rright = right
                self.rleft = 0
            else:
                self.rright = 0
                self.rleft = left
        else:
            self.rright = 0
            self.rleft = 0
            if self.reload_time >= SAUCER_RELOAD_TIME:
                saucer_shot_sound.play()
                SaucerShot((self.direction * math.pi / 180), self.position)
                self.reload_time = 0

        self.direction = dirn
        
        # Establish rotation and movement direction
        rad = math.radians(self.direction)
        self.direction += (self.rright + self.rleft)
        x, y = self.position
        x += (-self.speedv * math.sin(rad)) + (self.speedh * math.sin(rad -
                                                                (math.pi / 2)))
        y += (-self.speedv * math.cos(rad)) + (self.speedh * math.cos(rad -
                                                                (math.pi / 2)))

        # Make screen wrap-around
        if x > screen.get_width() + 50:
            x = -50
        elif x < -50:
            x = screen.get_width() + 50
        if y > screen.get_height() + 50:
            y = -50
        elif y < -50:
            y = screen.get_height() + 50

        # Move
        self.position = (x, y)
        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

        # Draw health
        posx = x - 50
        posy = y - 60
        draw_rect((posx,posy), (50,5), (255,0,0))
        draw_rect((posx,posy), ((float(self.health)/self.max_health) * 50,
                            5), (0,255,0))

        # Cheack for death
        if self.health <= 0:
            self.kill()
        
    def gunrot(self):
        return self.direction * math.pi / 180

    def gunpos(self):
        return self.position

class TriangleEnemy(pygame.sprite.Sprite):
    image = []
    def __init__(self, player, level):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.src_image = self.image[0]

        #initialize position
        self.rect = self.src_image.get_rect()
        self.arenax = screen.get_width()
        self.arenay = screen.get_height()
        self.position = (randint(50, self.arenax - 50), randint(50,
                                                            self.arenay - 50))
        self.rect.move_ip(self.position)

        #initialize speed and direction variables
        self.speedv = self.direction = 0
        self.forward = 0
        self.backward = 0
        self.rleft = 0
        self.rright = 0
        self.angle = 0

        #initialize state variables
        self.health = TRIANGLE_START_HEALTH + ((int(level) - 2) * 5)
        self.max_health = self.health
        self.reload_time = 0

        #get player location/rotation
        self.player = player
        self.player_pos = (0,0)
        self.player_rot = (0,0)

    def update(self):
        right = (TURN_SPEED * -1)
        left = TURN_SPEED

        self.reload_time += 20
        
        # Get player location/rotation
        self.player_pos = Player.gunpos(self.player)
        self.player_rot = math.degrees(Player.gunrot(self.player))

        #set variables
        angle = 0
        sx,sy = self.position
        px,py = self.player_pos
        dirn = self.direction       
        difx = px - sx
        dify = py - sy
        hyp = math.sqrt((difx ** 2) + (dify ** 2))
        
        #keep player rot within 360
        while self.player_rot > 360:
            self.player_rot -= 360
        while self.player_rot < 0:
            self.player_rot += 360

        # Keep angle within 360
        if dirn > 360:
            dirn = 0
        if dirn < 0:
            dirn = 360

        # Get angle to player
        if difx == 0:
            if dify <= 0:
                angle = 0
            else:
                angle = 180
        elif difx < 0:
            if dify <= 0:
                angle = math.degrees(math.asin(math.fabs(difx)/hyp))
            else:
                angle = 180-math.degrees(math.asin(math.fabs(difx)/hyp))
        else:
            if dify >= 0:
                angle = math.degrees(math.asin(math.fabs(difx)/hyp)) + 180
            else:
                angle = 360 - math.degrees(math.asin(math.fabs(difx)/hyp))

        # Decide which direction to turn
        if math.fabs(angle - dirn) >= 6 and math.fabs(angle - dirn) < 180:
            if angle > dirn:
                self.rright = 0
                self.rleft = left
            else:
                self.rright = right
                self.rleft = 0
        elif math.fabs(angle - dirn) >= 180:
            if angle > dirn:
                self.rright = right
                self.rleft = 0
            else:
                self.rright = 0
                self.rleft = left
        else:
            self.rright = 0
            self.rleft = 0
            
            #figure out which direction to move
            if hyp < 100:
                self.backward = -2
            elif hyp > 200:
                self.forward = 2
            else:
                self.backward = 0
                self.forward = 0
                
            #dicide if time to shoot
            if self.reload_time >= TRIANGLE_RELOAD_TIME:
                triangle_shot_sound.play()
                TriangleShot((self.direction * math.pi / 180), self.position)
                self.reload_time = 0

        self.direction = dirn

        # Establish vertical speed relative to self
        if self.speedv > 0:
            self.speedv += (self.forward + self.backward) - FRICTION
        elif self.speedv < 0:
            self.speedv += (self.forward + self.backward) + FRICTION
        else:
            self.speedv += (self.forward + self.backward)

        if self.speedv > TRIANGLE_SPEED:
            self.speedv = TRIANGLE_SPEED
        if self.speedv < TRIANGLE_SPEED * -1:
            self.speedv = TRIANGLE_SPEED * -1

        # Establish rotation and movement direction
        rad = math.radians(self.direction)
        self.direction += (self.rright + self.rleft)
        x, y = self.position
        x += -self.speedv * math.sin(rad)
        y += -self.speedv * math.cos(rad)
        
        # Make screen wrap-around
        if x > screen.get_width() + 50:
            x = -50
        elif x < -50:
            x = screen.get_width() + 50
        if y > screen.get_height() + 50:
            y = -50
        elif y < -50:
            y = screen.get_height() + 50

        # Move
        self.position = (x, y)
        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

        # Draw health
        posx = x - 50
        posy = y - 70
        draw_rect((posx,posy), (50,5), (255,0,0))
        draw_rect((posx,posy), ((float(self.health)/self.max_health) * 50,
                            5), (0,255,0))

        # Cheack for death
        if self.health <= 0:
            self.kill()
        
    def gunrot(self):
        return self.direction * math.pi / 180

    def gunpos(self):
        return self.position

class TankEnemy(pygame.sprite.Sprite):
    image = []
    def __init__(self, player, level):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.src_image = self.image[0]

        #initialize position
        self.rect = self.src_image.get_rect()
        self.arenax = screen.get_width()
        self.arenay = screen.get_height()
        self.position = (randint(50, self.arenax - 50), randint(50,
                                                            self.arenay - 50))
        self.rect.move_ip(self.position)

        #initialize speed and direction variables
        self.speedv = self.direction = 0
        self.forward = 0
        self.backward = 0
        self.rleft = 0
        self.rright = 0
        self.angle = 0

        #initialize state variables
        self.health = TANK_START_HEALTH + ((int(level) - 3) * 5)
        self.max_health = self.health
        self.reload_time = 0

        #get player location/rotation
        self.player = player
        self.player_pos = (0,0)
        self.player_rot = (0,0)

    def update(self):
        right = (TANK_TURN_SPEED * -1)
        left = TANK_TURN_SPEED

        self.reload_time += 20
        
        # Get player location/rotation
        self.player_pos = Player.gunpos(self.player)
        self.player_rot = math.degrees(Player.gunrot(self.player))

        #set variables
        angle = 0
        sx,sy = self.position
        px,py = self.player_pos
        dirn = self.direction       
        difx = px - sx
        dify = py - sy
        hyp = math.sqrt((difx ** 2) + (dify ** 2))
        
        #keep player rot within 360
        while self.player_rot > 360:
            self.player_rot -= 360
        while self.player_rot < 0:
            self.player_rot += 360

        # Keep angle within 360
        if dirn > 360:
            dirn = 0
        if dirn < 0:
            dirn = 360

        # Get angle to player
        if difx == 0:
            if dify <= 0:
                angle = 0
            else:
                angle = 180
        elif difx < 0:
            if dify <= 0:
                angle = math.degrees(math.asin(math.fabs(difx)/hyp))
            else:
                angle = 180-math.degrees(math.asin(math.fabs(difx)/hyp))
        else:
            if dify >= 0:
                angle = math.degrees(math.asin(math.fabs(difx)/hyp)) + 180
            else:
                angle = 360 - math.degrees(math.asin(math.fabs(difx)/hyp))

        # Decide which direction to turn
        if math.fabs(angle - dirn) >= 6 and math.fabs(angle - dirn) < 180:
            if angle > dirn:
                self.rright = 0
                self.rleft = left
            else:
                self.rright = right
                self.rleft = 0
        elif math.fabs(angle - dirn) >= 180:
            if angle > dirn:
                self.rright = right
                self.rleft = 0
            else:
                self.rright = 0
                self.rleft = left
        else:
            self.rright = 0
            self.rleft = 0
            
            #figure out which direction to move
            if hyp < 400:
                self.backward = -2
            elif hyp > 500:
                self.forward = 2
            else:
                self.backward = 0
                self.forward = 0
                
            #dicide if time to shoot
            if self.reload_time >= TANK_RELOAD_TIME:
                tank_shot_sound.play()
                TankShot((self.direction * math.pi / 180), self.position)
                self.reload_time = 0

        self.direction = dirn

        # Establish vertical speed relative to self
        if self.speedv > 0:
            self.speedv += (self.forward + self.backward) - FRICTION
        elif self.speedv < 0:
            self.speedv += (self.forward + self.backward) + FRICTION
        else:
            self.speedv += (self.forward + self.backward)

        if self.speedv > TANK_SPEED:
            self.speedv = TANK_SPEED
        if self.speedv < TANK_SPEED * -1:
            self.speedv = TANK_SPEED * -1

        # Establish rotation and movement direction
        rad = math.radians(self.direction)
        self.direction += (self.rright + self.rleft)
        x, y = self.position
        x += -self.speedv * math.sin(rad)
        y += -self.speedv * math.cos(rad)
        
        # Make screen wrap-around
        if x > screen.get_width() + 50:
            x = -50
        elif x < -50:
            x = screen.get_width() + 50
        if y > screen.get_height() + 50:
            y = -50
        elif y < -50:
            y = screen.get_height() + 50

        # Move
        self.position = (x, y)
        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

        # Draw health
        posx = x - 50
        posy = y - 75
        draw_rect((posx,posy), (50,5), (255,0,0))
        draw_rect((posx,posy), ((float(self.health)/self.max_health) * 50,
                            5), (0,255,0))

        # Cheack for death
        if self.health <= 0:
            self.kill()
        
    def gunrot(self):
        return self.direction * math.pi / 180

    def gunpos(self):
        return self.position

class MineEnemy(pygame.sprite.Sprite):
    image = []
    def __init__(self, level):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.src_image = self.image[0]

        #initialize position
        self.rect = self.src_image.get_rect()
        self.arenax = screen.get_width()
        self.arenay = screen.get_height()
        self.position = (randint(50, self.arenax - 50), randint(50,
                                                            self.arenay - 50))
        self.rect.move_ip(self.position)

        #initialize speed and direction variables
        self.speedv = self.direction = 0
        self.forward = 2
        self.turn_speed = 0

        #initialize state variables
        self.health = MINE_START_HEALTH + ((int(level) - 4) * 5)
        self.max_health = self.health
        self.reload_time = 0
        self.change_direction = 0

    def update(self):
        self.reload_time += 20
        dirn = self.direction

        # Mabye change direction
        if self.change_direction == 0:
            rand = randint(1,2)
            if rand == 1:
                self.turn_speed = MINE_MAX_TURN_SPEED
            elif rand == 2:
                self.turn_speed = -MINE_MAX_TURN_SPEED
            self.change_direction = 0

        self.change_direction += 20

        if self.change_direction >= MINE_DIRECTION_CHANGE:
            self.change_direction = 0

        # Keep angle within 360
        if dirn > 360:
            dirn = 0
        if dirn < 0:
            dirn = 360

        # Decide if time to shoot
        if self.reload_time >= MINE_RELOAD_TIME:
            mine_drop_sound.play()
            MineShot((self.direction * math.pi / 180), self.position)
            self.reload_time = 0

        self.direction = dirn

        # Establish vertical speed relative to self
        if self.speedv > 0:
            self.speedv += self.forward - FRICTION
        elif self.speedv < 0:
            self.speedv += self.forward + FRICTION
        else:
            self.speedv += self.forward

        if self.speedv > MINE_SPEED:
            self.speedv = MINE_SPEED
        if self.speedv < MINE_SPEED * -1:
            self.speedv = MINE_SPEED * -1

        # Establish rotation and movement direction
        rad = math.radians(self.direction)
        self.direction += (self.turn_speed)
        x, y = self.position
        x += -self.speedv * math.sin(rad)
        y += -self.speedv * math.cos(rad)
        
        # Make screen wrap-around
        if x > screen.get_width() + 50:
            x = -50
        elif x < -50:
            x = screen.get_width() + 50
        if y > screen.get_height() + 50:
            y = -50
        elif y < -50:
            y = screen.get_height() + 50

        # Move
        self.position = (x, y)
        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

        # Draw health
        posx = x - 50
        posy = y - 75
        draw_rect((posx,posy), (50,5), (255,0,0))
        draw_rect((posx,posy), ((float(self.health)/self.max_health) * 50,
                            5), (0,255,0))

        # Cheack for death
        if self.health <= 0:
            self.kill()
        
    def gunrot(self):
        return self.direction * math.pi / 180

    def gunpos(self):
        return self.position

class TrishotEnemy(pygame.sprite.Sprite):
    image = []
    def __init__(self, player, level):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.src_image = self.image[0]

        #initialize position
        self.rect = self.src_image.get_rect()
        self.arenax = screen.get_width()
        self.arenay = screen.get_height()
        self.position = (randint(50, self.arenax - 50), randint(50,
                                                            self.arenay - 50))
        self.rect.move_ip(self.position)

        #initialize speed and direction variables
        self.speedv = self.direction = 0
        self.forward = 0
        self.backward = 0
        self.rleft = 0
        self.rright = 0
        self.angle = 0

        #initialize state variables
        self.health = TRISHOT_START_HEALTH + ((int(level) - 5) * 5)
        self.max_health = self.health
        self.reload_time = 0

        #get player location/rotation
        self.player = player
        self.player_pos = (0,0)
        self.player_rot = (0,0)

    def update(self):
        right = (TRISHOT_TURN_SPEED * -1)
        left = TRISHOT_TURN_SPEED

        self.reload_time += 20
        
        # Get player location/rotation
        self.player_pos = Player.gunpos(self.player)
        self.player_rot = math.degrees(Player.gunrot(self.player))

        #set variables
        angle = 0
        sx,sy = self.position
        px,py = self.player_pos
        dirn = self.direction       
        difx = px - sx
        dify = py - sy
        hyp = math.sqrt((difx ** 2) + (dify ** 2))
        
        #keep player rot within 360
        while self.player_rot > 360:
            self.player_rot -= 360
        while self.player_rot < 0:
            self.player_rot += 360

        # Keep angle within 360
        if dirn > 360:
            dirn = 0
        if dirn < 0:
            dirn = 360

        # Get angle to player
        if difx == 0:
            if dify <= 0:
                angle = 0
            else:
                angle = 180
        elif difx < 0:
            if dify <= 0:
                angle = math.degrees(math.asin(math.fabs(difx)/hyp))
            else:
                angle = 180-math.degrees(math.asin(math.fabs(difx)/hyp))
        else:
            if dify >= 0:
                angle = math.degrees(math.asin(math.fabs(difx)/hyp)) + 180
            else:
                angle = 360 - math.degrees(math.asin(math.fabs(difx)/hyp))

        # Decide which direction to turn
        if math.fabs(angle - dirn) >= 6 and math.fabs(angle - dirn) < 180:
            if angle > dirn:
                self.rright = 0
                self.rleft = left
            else:
                self.rright = right
                self.rleft = 0
        elif math.fabs(angle - dirn) >= 180:
            if angle > dirn:
                self.rright = right
                self.rleft = 0
            else:
                self.rright = 0
                self.rleft = left
        else:
            self.rright = 0
            self.rleft = 0
            
            #figure out which direction to move
            if hyp < 350:
                self.backward = -2
            elif hyp > 450:
                self.forward = 2
            else:
                self.backward = 0
                self.forward = 0
                
            #dicide if time to shoot
            if self.reload_time >= TRISHOT_RELOAD_TIME:
                trishot_sound.play()
                TriShot((self.direction*math.pi/180)+(math.pi/4), self.position)
                TriShot(self.direction * math.pi / 180, self.position)
                TriShot((self.direction*math.pi/180)-(math.pi/4), self.position)
                self.reload_time = 0

        self.direction = dirn

        # Establish vertical speed relative to self
        if self.speedv > 0:
            self.speedv += (self.forward + self.backward) - FRICTION
        elif self.speedv < 0:
            self.speedv += (self.forward + self.backward) + FRICTION
        else:
            self.speedv += (self.forward + self.backward)

        if self.speedv > TRISHOT_SPEED:
            self.speedv = TRISHOT_SPEED
        if self.speedv < TRISHOT_SPEED * -1:
            self.speedv = TRISHOT_SPEED * -1

        # Establish rotation and movement direction
        rad = math.radians(self.direction)
        self.direction += (self.rright + self.rleft)
        x, y = self.position
        x += -self.speedv * math.sin(rad)
        y += -self.speedv * math.cos(rad)
        
        # Make screen wrap-around
        if x > screen.get_width() + 50:
            x = -50
        elif x < -50:
            x = screen.get_width() + 50
        if y > screen.get_height() + 50:
            y = -50
        elif y < -50:
            y = screen.get_height() + 50

        # Move
        self.position = (x, y)
        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

        # Draw health
        posx = x - 50
        posy = y - 75
        draw_rect((posx,posy), (50,5), (255,0,0))
        draw_rect((posx,posy), ((float(self.health)/self.max_health) * 50,
                            5), (0,255,0))

        # Cheack for death
        if self.health <= 0:
            self.kill()
    
    def gunrot(self):
        return self.direction * math.pi / 180

    def gunpos(self):
        return self.position

class BossEnemy(pygame.sprite.Sprite):
    image = []
    def __init__(self, player, level):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.src_image = self.image[0]

        #initialize position
        self.rect = self.src_image.get_rect()
        self.arenax = screen.get_width()
        self.arenay = screen.get_height()
        self.position = (randint(50, self.arenax - 50), randint(50,
                                                            self.arenay - 50))
        self.rect.move_ip(self.position)

        #initialize speed and direction variables
        self.speedv = self.speedh = self.direction = 0
        self.forward = 0
        self.backward = 0
        self.left = 0
        self.right = 0
        self.rleft = 0
        self.rright = 0
        self.angle = 0

        #initialize state variables
        self.health = BOSS_START_HEALTH + ((int(level) - 1) * 5)
        self.max_health = self.health
        self.reload_time = 0

        #get player location/rotation
        self.player = player
        self.player_pos = (0,0)
        self.player_rot = (0,0)

    def update(self):
        right = (TURN_SPEED * -1)
        left = TURN_SPEED

        self.reload_time += 20
        
        # Get player location/rotation
        self.player_pos = Player.gunpos(self.player)
        self.player_rot = math.degrees(Player.gunrot(self.player))

        #set variables
        angle = 0
        sx,sy = self.position
        px,py = self.player_pos
        dirn = self.direction       
        difx = px - sx
        dify = py - sy
        hyp = math.sqrt((difx ** 2) + (dify ** 2))
        
        #keep player rot within 360
        while self.player_rot > 360:
            self.player_rot -= 360
        while self.player_rot < 0:
            self.player_rot += 360

        #figure out which direction to move
        if sx < px:
            if sy < py:
                if self.player_rot < 45:
                    self.right = -2
                    self.left = 0
                else:
                    self.right = 0
                    self.left = 2
            else:
                if self.player_rot > 90 and self.player_rot < 135:
                    self.right = -2
                    self.left = 0
                else:
                    self.right = 0
                    self.left = 2
        else:
            if sy < py:
                if self.player_rot < 315:
                    self.right = -2
                    self.left = 0
                else:
                    self.right = 0
                    self.left = 2
            else:
                if self.player_rot < 270 and self.player_rot > 225:
                    self.right = -2
                    self.left = 0
                else:
                    self.right = 0
                    self.left = 2
        if hyp < 300:
            self.backward = -2
        elif hyp > 400:
            self.forward = 2
        else:
            self.backward = 0
            self.forward = 0
                    
        
        # Establish vertical speed relative to self
        if self.speedv > 0:
            self.speedv += (self.forward + self.backward) - FRICTION
        elif self.speedv < 0:
            self.speedv += (self.forward + self.backward) + FRICTION
        else:
            self.speedv += (self.forward + self.backward)

        if self.speedv > BOSS_SPEED:
            self.speedv = BOSS_SPEED
        if self.speedv < BOSS_SPEED * -1:
            self.speedv = BOSS_SPEED * -1
        
        # Establish horizontal speed relative to self
        if self.speedh > 0:
            self.speedh += (self.left + self.right) - FRICTION
        elif self.speedh < 0:
            self.speedh += (self.left + self.right) + FRICTION
        else:
            self.speedh += (self.left + self.right)
        
        if self.speedh > BOSS_SPEED:
            self.speedh = BOSS_SPEED
        if self.speedh < BOSS_SPEED * -1:
            self.speedh = BOSS_SPEED * -1  

        # Keep angle within 360
        if dirn > 360:
            dirn = 0
        if dirn < 0:
            dirn = 360

        # Get angle to player
        if difx == 0:
            if dify <= 0:
                angle = 0
            else:
                angle = 180
        elif difx < 0:
            if dify <= 0:
                angle = math.degrees(math.asin(math.fabs(difx)/hyp))
            else:
                angle = 180-math.degrees(math.asin(math.fabs(difx)/hyp))
        else:
            if dify >= 0:
                angle = math.degrees(math.asin(math.fabs(difx)/hyp)) + 180
            else:
                angle = 360 - math.degrees(math.asin(math.fabs(difx)/hyp))

        # Decide which direction to turn
        if math.fabs(angle - dirn) >= 6 and math.fabs(angle - dirn) < 180:
            if angle > dirn:
                self.rright = 0
                self.rleft = left
            else:
                self.rright = right
                self.rleft = 0
        elif math.fabs(angle - dirn) >= 180:
            if angle > dirn:
                self.rright = right
                self.rleft = 0
            else:
                self.rright = 0
                self.rleft = left
        else:
            self.rright = 0
            self.rleft = 0
        # Shoot on time even if not aiming at player
        if self.reload_time >= BOSS_RELOAD_TIME:
            boss_shot_sound.play()
            BossShot((self.direction * math.pi / 180), self.position)
            self.reload_time = 0

        self.direction = dirn
        
        # Establish rotation and movement direction
        rad = math.radians(self.direction)
        self.direction += (self.rright + self.rleft)
        x, y = self.position
        x += (-self.speedv * math.sin(rad)) + (self.speedh * math.sin(rad -
                                                                (math.pi / 2)))
        y += (-self.speedv * math.cos(rad)) + (self.speedh * math.cos(rad -
                                                                (math.pi / 2)))

        # Make screen wrap-around
        if x > screen.get_width() + 50:
            x = -50
        elif x < -50:
            x = screen.get_width() + 50
        if y > screen.get_height() + 50:
            y = -50
        elif y < -50:
            y = screen.get_height() + 50

        # Move
        self.position = (x, y)
        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

        # Draw health
        posx = x - 25
        posy = y - 40
        draw_rect((posx,posy), (50,5), (255,0,0))
        draw_rect((posx,posy), ((float(self.health)/self.max_health) * 50,
                            5), (0,255,0))

        # Cheack for death
        if self.health <= 0:
            self.kill()
        
    def gunrot(self):
        return self.direction * math.pi / 180

    def gunpos(self):
        return self.position

class Target(pygame.sprite.Sprite):
    image = []
    def __init__(self, arena):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.image[0]
        self.arenax = arena.get_width()
        self.arenay = arena.get_height()
        self.position = (randint(50, self.arenax - 50), randint(50,
                                                            self.arenay - 50))
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.position)
        self.dead = False

    def position(self):
        return self.position

    def update(self):
        if self.dead:
            self.kill()
            
#Bullet Classes
class PlayerShot(pygame.sprite.Sprite):
    """ Creates a bullet at the Omnitank's cannon end and angle, the
        bullet dies at the end of the screen.
    """
    image = []
    def __init__(self, rotation, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rotation = (180 * rotation) / math.pi
        self.rad = rotation
        self.image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.move_ip(pos)
        self.boundries = screen

    def update(self):
        x, y = self.rect.center
        rad = self.rad
        x += (-PLAYER_BULLET_SPEED  * math.sin(rad))
        y += (-PLAYER_BULLET_SPEED  * math.cos(rad))
        self.rect.center = (x, y)
        
        if (self.rect.centerx < -100 or self.rect.centerx >
            self.boundries.get_width() + 100 or self.rect.centery < -100 or
            self.rect.centery > self.boundries.get_height() + 100):
            self.kill()

class SaucerShot(pygame.sprite.Sprite):
    image = []
    def __init__(self, rotation, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rotation = (180 * rotation) / math.pi
        self.rad = rotation
        self.image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.move_ip(pos)
        self.boundries = screen
        
    def update(self):
        x, y = self.rect.center
        rad = self.rad
        x += (-SAUCER_BULLET_SPEED  * math.sin(rad))
        y += (-SAUCER_BULLET_SPEED  * math.cos(rad))
        self.rect.center = (x, y)
        
        if (self.rect.centerx < -100 or self.rect.centerx >
            self.boundries.get_width() + 100 or self.rect.centery < -100 or
            self.rect.centery > self.boundries.get_height() + 100):
            self.kill()

class TriangleShot(pygame.sprite.Sprite):
    image = []
    def __init__(self, rotation, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rotation = (180 * rotation) / math.pi
        self.rad = rotation
        self.image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.move_ip(pos)
        self.boundries = screen
        
    def update(self):
        x, y = self.rect.center
        rad = self.rad
        x += (-TRIANGLE_BULLET_SPEED  * math.sin(rad))
        y += (-TRIANGLE_BULLET_SPEED  * math.cos(rad))
        self.rect.center = (x, y)
        
        if (self.rect.centerx < -100 or self.rect.centerx >
            self.boundries.get_width() + 100 or self.rect.centery < -100 or
            self.rect.centery > self.boundries.get_height() + 100):
            self.kill()

class TankShot(pygame.sprite.Sprite):
    image = []
    def __init__(self, rotation, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rotation = (180 * rotation) / math.pi
        self.rad = rotation
        self.image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.move_ip(pos)
        self.boundries = screen
        
    def update(self):
        x, y = self.rect.center
        rad = self.rad
        x += (-TANK_BULLET_SPEED  * math.sin(rad))
        y += (-TANK_BULLET_SPEED  * math.cos(rad))
        self.rect.center = (x, y)
        
        if (self.rect.centerx < -100 or self.rect.centerx >
            self.boundries.get_width() + 100 or self.rect.centery < -100 or
            self.rect.centery > self.boundries.get_height() + 100):
            self.kill()

class MineShot(pygame.sprite.Sprite):
    animcycle = 3
    images = []
    def __init__(self, rotation, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rotation = (180 * rotation) / math.pi
        self.rad = rotation
        self.image = pygame.transform.rotate(self.images[0], self.rotation)
        self.rect = self.image.get_rect()
        self.rect.move_ip(pos)
        self.life = 0

    def update(self):
        self.life += 1
        self.image = self.images[self.life//self.animcycle%2]

class TriShot(pygame.sprite.Sprite):
    image = []
    def __init__(self, rotation, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rotation = (180 * rotation) / math.pi
        self.rad = rotation
        self.image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.move_ip(pos)
        self.boundries = screen
        
    def update(self):
        x, y = self.rect.center
        rad = self.rad
        x += (-TRISHOT_BULLET_SPEED  * math.sin(rad))
        y += (-TRISHOT_BULLET_SPEED  * math.cos(rad))
        self.rect.center = (x, y)
        
        if (self.rect.centerx < -100 or self.rect.centerx >
            self.boundries.get_width() + 100 or self.rect.centery < -100 or
            self.rect.centery > self.boundries.get_height() + 100):
            self.kill()

class BossShot(pygame.sprite.Sprite):
    image = []
    def __init__(self, rotation, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rotation = (180 * rotation) / math.pi
        self.rad = rotation
        self.image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.move_ip(pos)
        self.boundries = screen
        
    def update(self):
        x, y = self.rect.center
        rad = self.rad
        x += (-BOSS_BULLET_SPEED  * math.sin(rad))
        y += (-BOSS_BULLET_SPEED  * math.cos(rad))
        self.rect.center = (x, y)
        
        if (self.rect.centerx < -100 or self.rect.centerx >
            self.boundries.get_width() + 100 or self.rect.centery < -100 or
            self.rect.centery > self.boundries.get_height() + 100):
            self.kill()

class Explosion(pygame.sprite.Sprite):
    defaultlife = 12
    animcycle = 3
    images = []
    def __init__(self, actor):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images = choice(self.images)
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=actor.rect.center)
        self.life = self.defaultlife

    def update(self):
        self.life -= 1
        self.image = self.images[self.life//self.animcycle%2]
        if self.life <= 0: self.kill()

#Load Data Functions
def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join('images', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface

def load_sound(file):
    "loads a sound, prepares it for play"
    #if not pygame.mixer: return dummysound()
    file = os.path.join('sounds', file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print ('Warning, unable to load, %s' % file)
    return dummysound()

def load_and_assign_all_images(player_model):
    #load player images
    player_img = load_image(player_model).convert_alpha()
    saucer_img = load_image('saucer_enemy.png')
    triangle_img = load_image('triangle_enemy.png')
    tank_img = load_image('tank_enemy.png')
    mine_img = load_image('mine_enemy.png')
    trishot_img = load_image('trishot_enemy.png')
    boss_img = load_image('boss.png')
    target_img = load_image('target_S.png')

    #assign player images
    Player.image = [player_img]
    SaucerEnemy.image = [saucer_img]
    TriangleEnemy.image = [triangle_img]
    TankEnemy.image = [tank_img]
    MineEnemy.image = [mine_img]
    TrishotEnemy.image = [trishot_img]
    BossEnemy.image = [boss_img]
    Target.image = [target_img]

    #load bullet images
    player_bullet_img = load_image('omni_bullet.png')
    saucer_bullet_img = load_image('saucer_bullet.png')
    triangle_bullet_img = load_image('triangle_bullet.png')
    tank_bullet_img = load_image('tank_bullet.png')
    mine_img1 = load_image('mine1.png')
    mine_img2 = load_image('mine2.png')
    mine_shot_imgs = [mine_img1,mine_img2]
    trishot_laser_img = load_image('trishot_laser.png')
    boss_laser_img = load_image('boss_laser.png')

    #assign bullet images
    PlayerShot.image = player_bullet_img
    SaucerShot.image = saucer_bullet_img
    TriangleShot.image = triangle_bullet_img
    TankShot.image = tank_bullet_img
    MineShot.images = mine_shot_imgs
    TriShot.image = trishot_laser_img
    BossShot.image = boss_laser_img

    #load/assign explosion images
    expl_image1 = load_image('explosion1.png')
    expl_image2 = load_image('explosion2.png')
    expl_image3 = load_image('explosion3.png')
    expl_img1 = [expl_image1, pygame.transform.flip(expl_image1, 1, 1)]
    expl_img2 = [expl_image2, pygame.transform.flip(expl_image2, 1, 1)]
    expl_img3 = [expl_image3, pygame.transform.flip(expl_image3, 1, 1)]
    expl_img = [expl_img1, expl_img2, expl_img3]
    Explosion.images = expl_img

    #other images
    global bgdtile
    bgdtile = load_image('grey_background.png')

def load_all_sounds():
    global player_shot_sound
    global saucer_shot_sound
    global triangle_shot_sound
    global tank_shot_sound
    global mine_drop_sound
    global explosion_sound
    global trishot_sound
    global boss_shot_sound
    player_shot_sound = load_sound('player_shot.wav')
    saucer_shot_sound = load_sound('saucer_shot.wav')
    triangle_shot_sound = load_sound('tirangle_shot.wav')
    tank_shot_sound = load_sound('tank_shot.wav')
    mine_drop_sound = load_sound('mine_drop.wav')
    explosion_sound = load_sound('explosion.wav')
    trishot_sound = load_sound('trishot_shot.wav')
    boss_shot_sound = load_sound('boss_shot.wav')

    #set effecs volumes
    saucer_shot_sound.set_volume(.5)
    triangle_shot_sound.set_volume(.5)
    
#Drawing Functions
def draw_message(position, size, message):
    """
        position format --> (x,y)
        size format --> just a number
        message format --> "message"
    """
    
    font = pygame.font.SysFont('arial', size)
    Message = font.render(message, True, Color('white'))
    screen.blit(Message, position)

def draw_rect(position, size, color):
    """
        Used for displaying health bar

        position (of top left corner) --> (x,y)
        size --> (legth of x, legth of y)
        color --> (R,G,B)
    """

    pos_x = position[0]
    pos_y = position[1]
    size_x = size[0]
    size_y = size[1]
    screen.fill(color, (pos_x, pos_y, size_x, size_y))

def draw_background():
    background = pygame.Surface(SCREENRECT.size)
    for x in range(0, SCREENRECT.width, bgdtile.get_width()):
        for y in range (0, SCREENRECT.height, bgdtile.get_height()):
            background.blit(bgdtile, (x,y))
    screen.blit(background, (0,0))

def draw_HUD(player, score, lives, level, time, jdbr, num_enemies):
    #constants
    lives_location   = (420,740)
    score_location   = (10,740)
    level_location   = (5,5)
    timer_location   = (650,0)
    bonus_location   = (300,0)
    enemies_location = (100,5)
    health_pos       = (500,740)
    health_size      = (500,20)
    dark_blue        = (89,141,178)
    light_blue       = (127,201,255)
    grey             = (64,64,64)
    
    #draw lives
    draw_rect(lives_location, (80,20), grey)
    draw_message(lives_location, 20, 'Lives: %d' %lives)

    #draw player health bar
    draw_rect(health_pos, health_size, dark_blue)
    draw_rect(health_pos, ((float(player.health)/
                            PLAYER_MAX_HEALTH) * 500,
                            20), light_blue)
    draw_message((725,740), 20, '%d/%d' %(player.health,
                                     PLAYER_MAX_HEALTH))

    #draw score
    draw_rect(score_location, (410,20), grey)
    draw_message(score_location, 20, 'Score: %d' %score)

    #draw level number and remaining enemies
    draw_rect(level_location, (400,20), grey)
    draw_message(level_location, 20, 'Level: %0.1f' %level)
    draw_message(enemies_location, 20, 'Enemies Remaining: %d' %num_enemies)

    #draw timer on bonous rounds
    draw_rect(timer_location, (400,60), grey)
    draw_rect(bonus_location, (260,60), grey)
    if bonus_round(level, time) and not jdbr:
         draw_message(timer_location, 50, "Time Remaining: %d" %time)
         draw_message(bonus_location, 50, "Bonus Round!")
         
         #hide enemy display
         draw_rect(enemies_location, (200,25), grey)

#Game Control Functions
def bonus_round(level, time):
    """
        Returns True if it is time for a bonus round
    """
    value = ((int(level*10)-9) % 50)
    if level > 1 and time > 0: return not bool(value)
    else: return False

def start_of_new_level(level):
    """
        Retruns True if the next level is a new one (not a wave)
    """
    level_str = str(level)
    last_digit = int(level_str[-1])
    if level > 1 and last_digit == 0: return True
    else: return False

def create_enemies(level, prev_level, time, jdbr, num_enemies, player):
    level_str = str(level)
    last_digit = int(level_str[-1])
    if bonus_round(level, time) and not jdbr:
        max_enemies = 1
        if prev_level != level:
            num_enemies = 0
        if num_enemies < max_enemies:
            Target(screen)
            num_enemies += 1
    else:
        if last_digit == 9:
            max_enemies = 1
        else:
            max_enemies = last_digit + 1
        while num_enemies < max_enemies:
            rand = randint(1,100)
            if level < 1.9:
                SaucerEnemy(player, level)
                num_enemies += 1
            elif level >= 2.0 and level < 2.9:
                if rand <= 50: # 50% chance
                    SaucerEnemy(player, level)
                    num_enemies += 1
                else: # 50% chance
                    TriangleEnemy(player, level)
                    num_enemies += 1
            elif level >= 3 and level < 3.9:
                if rand <= 50: #40% chance
                    SaucerEnemy(player, level)
                    num_enemies += 1
                elif rand > 50 and rand <= 80: #30% chance
                    TriangleEnemy(player, level)
                    num_enemies += 1
                else: #20% chance
                    TankEnemy(player, level)
                    num_enemies += 1
            elif level >= 4 and level <= 4.8:
                if rand <= 40: #40% chance
                    SaucerEnemy(player, level)
                    num_enemies += 1
                elif rand > 40 and rand <= 75: #35% chance
                    TriangleEnemy(player, level)
                    num_enemies += 1
                elif rand > 75 and rand <= 90: #15% chance
                    TankEnemy(player, level)
                    num_enemies += 1
                else: #10% chance
                    MineEnemy(level)
                    num_enemies +=  1
            elif level > 4.9 and last_digit != 9:
                if rand <= 40: #40% chance
                    SaucerEnemy(player, level)
                    num_enemies += 1
                elif rand > 40 and rand <= 65: #25% chance
                    TriangleEnemy(player, level)
                    num_enemies += 1
                elif rand > 65 and rand <= 80: #15% chance
                    TankEnemy(player, level)
                    num_enemies += 1
                elif rand > 80 and rand <= 90: #10% chance
                    MineEnemy(level)
                    num_enemies += 1
                else: #10% chance
                    TrishotEnemy(player,level)
                    num_enemies += 1
            else: #This only occurs if last_digit = 9
                BossEnemy(player, level)
                num_enemies += 1
        
    return max_enemies, num_enemies, prev_level
     
def initialize_groups():
    global player_group
    global player_bullet_group
    global saucer_group
    global saucer_bullet_group
    global triangle_group
    global triangle_bullet_group
    global tank_group
    global tank_bullet_group
    global mine_group
    global mine_mine_group
    global trishot_group
    global trishot_laser_group
    global boss_group
    global boss_laser_group
    global target_group
    global explosion_group
    global enemy_group
    global bullet_group
    global all
    
    player_group = pygame.sprite.Group()
    player_bullet_group = pygame.sprite.Group()
    saucer_group = pygame.sprite.Group()
    saucer_bullet_group = pygame.sprite.Group()
    triangle_group = pygame.sprite.Group()
    triangle_bullet_group = pygame.sprite.Group()
    tank_group = pygame.sprite.Group()
    tank_bullet_group = pygame.sprite.Group()
    mine_group = pygame.sprite.Group()
    mine_mine_group = pygame.sprite.Group()
    trishot_group = pygame.sprite.Group()
    trishot_laser_group = pygame.sprite.Group()
    boss_group = pygame.sprite.Group()
    boss_laser_group = pygame.sprite.Group()
    target_group = pygame.sprite.Group()
    explosion_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    all = pygame.sprite.RenderUpdates()

    Player.containers = all, player_group
    PlayerShot.containers = all, player_bullet_group, bullet_group
    SaucerEnemy.containers = all, saucer_group, enemy_group
    SaucerShot.containers = all, saucer_bullet_group, bullet_group
    TriangleEnemy.containers = all, triangle_group, enemy_group
    TriangleShot.containers = all, triangle_bullet_group, bullet_group
    TankEnemy.containers = all, tank_group, enemy_group
    TankShot.containers = all, tank_bullet_group, bullet_group
    MineEnemy.containers = all, mine_group, enemy_group
    MineShot.containers = all, mine_mine_group, bullet_group
    TrishotEnemy.containers = all, trishot_group, enemy_group
    TriShot.containers = all, trishot_laser_group, bullet_group
    BossEnemy.containers = all, boss_group, enemy_group
    BossShot.containers = all, boss_laser_group, bullet_group
    Target.containers = all, target_group
    Explosion.containers = all, explosion_group

def initialize_game():
    pygame.init()
    wintitle = pygame.display.set_caption("OmniTank Game")
    pygame.mouse.set_visible(False)
    if pygame.mixer and not pygame.mixer.get_init():
        print ('Warning, no sound')
        pygame.mixer = None

def game_state(level,time,jdbr):
    if bonus_round(level, time) and not jdbr:
        state = 'bonus'
    else:
        state = 'game'
    return state

def state_changed(state,prev_state):
    if prev_state != state:
        return True
    else: return False       

def get_user_input(player, level, shots_fired, pause_result, mus_pause, player_reload):
    for event in pygame.event.get():
        if not hasattr(event, 'key'):
            return level, shots_fired, pause_result, mus_pause, player_reload
        down = event.type == KEYDOWN
        if event.key == K_SPACE and down:
            if player_reload >= PLAYER_RELOAD:
                PlayerShot(player.gunrot(), player.gunpos())
                player_shot_sound.play()
                shots_fired += 1
                player_reload = 0
            pygame.event.post(event)
        elif event.key == K_SPACE and event.type == KEYUP:
            pygame.event.poll()
        if event.key == K_RIGHT:
            player.k_right = down * (TURN_SPEED * -1)
        elif event.key == K_LEFT:
            player.k_left = down * TURN_SPEED
        elif event.key == K_w:
            player.k_w = down * ACCELERATION
        elif event.key == K_s:
            player.k_s = down * (ACCELERATION * -1)
        elif event.key == K_a:
            player.k_a = down * ACCELERATION
        elif event.key == K_d:
            player.k_d = down * (ACCELERATION * -1)
        elif event.key == K_p and down:
            pause_result = Pause_Menu.pause()
        elif event.key == K_m and down:
            if mus_pause:
                mus_pause = False
                pygame.mixer.music.unpause()
            else:
                mus_pause = True
                pygame.mixer.music.pause()
    return level, shots_fired, pause_result, mus_pause, player_reload

def detect_collisions(score, level_score, num_enemies, shots_hit):
    for target in pygame.sprite.groupcollide(target_group, player_bullet_group,1,1):
        target_group.dead = True
        score += TARGET_POINTS
        level_score += TARGET_POINTS
        num_enemies -= 1
        shots_hit += 1
    for saucer in pygame.sprite.groupcollide(saucer_group, player_bullet_group,0,1):
        saucer.health -= PLAYER_DAMAGE
        if saucer.health <= 0:
            explosion_sound.play()
            Explosion(saucer)
            score += SAUCER_POINTS
            level_score += SAUCER_POINTS
            num_enemies -= 1
        shots_hit += 1
    for player in pygame.sprite.groupcollide(player_group, saucer_bullet_group,0,1):
        player.hit = True
        player.damage_type = 'saucer'
    for triangle in pygame.sprite.groupcollide(triangle_group, player_bullet_group,0,1):
        triangle.health -= PLAYER_DAMAGE
        if triangle.health <= 0:
            explosion_sound.play()
            Explosion(triangle)
            score += TRIANGLE_POINTS
            level_score += TRIANGLE_POINTS
            num_enemies -= 1
        shots_hit += 1
    for player in pygame.sprite.groupcollide(player_group, triangle_bullet_group,0,1):
        player.hit = True
        player.damage_type = 'triangle'
    for tank in pygame.sprite.groupcollide(tank_group, player_bullet_group,0,1):
        tank.health -= PLAYER_DAMAGE
        if tank.health <= 0:
            explosion_sound.play()
            Explosion(tank)
            score += TANK_POINTS
            level_score += TANK_POINTS
            num_enemies -= 1
        shots_hit += 1
    for player in pygame.sprite.groupcollide(player_group, tank_bullet_group,0,0):
        for tank_bullet in pygame.sprite.groupcollide(tank_bullet_group, player_group,1,0):
            explosion_sound.play()
            Explosion(tank_bullet)
        player.hit = True
        player.damage_type = 'tank'
    for mine_enemy in pygame.sprite.groupcollide(mine_group, player_bullet_group,0,1):
        mine_enemy.health -= PLAYER_DAMAGE
        if mine_enemy.health <= 0:
            explosion_sound.play()
            Explosion(mine_enemy)
            score += MINE_POINTS
            level_score += MINE_POINTS
            num_enemies -= 1
        shots_hit += 1
    for player in pygame.sprite.groupcollide(player_group, mine_mine_group,0,0):
        for mine in pygame.sprite.groupcollide(mine_mine_group, player_group,1,0):
            explosion_sound.play()
            Explosion(mine)
        player.hit = True
        player.damage_type = 'mine'
    for mine in pygame.sprite.groupcollide(mine_mine_group, player_bullet_group,1,1):
        explosion_sound.play()
        Explosion(mine)
        shots_hit += 1
    for trishot in pygame.sprite.groupcollide(trishot_group, player_bullet_group,0,1):
        trishot.health -= PLAYER_DAMAGE
        if trishot.health <= 0:
            explosion_sound.play()
            Explosion(trishot)
            score += TRISHOT_POINTS
            level_score += TRISHOT_POINTS
            num_enemies -= 1
        shots_hit += 1
    for player in pygame.sprite.groupcollide(player_group, trishot_laser_group,0,1):
        player.hit = True
        player.damage_type = 'trishot'
    for boss in pygame.sprite.groupcollide(boss_group, player_bullet_group,0,1):
        boss.health -= PLAYER_DAMAGE
        if boss.health <= 0:
            explosion_sound.play()
            Explosion(boss)
            score += BOSS_POINTS
            level_score += BOSS_POINTS
            num_enemies -= 1
        shots_hit += 1
    for player in pygame.sprite.groupcollide(player_group, boss_laser_group,0,1):
        player.hit = True
        player.damage_type = 'boss'
    return score, level_score, num_enemies, shots_hit

def clear_bullets():
    for bullet in bullet_group:
        bullet.kill()
    for explosion in explosion_group:
        explosion.kill()

def clear_enemies(num_enemies):
    for enemy in enemy_group:
        enemy.kill()
        num_enemies -= 1
    return num_enemies

def update_all():
    all.clear(screen, background)
    all.update()
    dirty = all.draw(screen)
    pygame.display.update(dirty)
    pygame.display.flip()

def game(player_model):
    #initialize game, images, sounds, and groups
    initialize_game()
    load_and_assign_all_images(player_model)
    load_all_sounds()
    initialize_groups()

    #initialize game variables
    score        = 0
    level_score  = 0
    bonus_points = 0
    lives        = LIVES
    level        = 1.0
    prev_level   = 0.0
    high_level   = 0.0
    time         = BONUS_START_TIME
    Game_State   = 'game'
    Prev_State   = Game_State
    max_enemies  = 0
    num_enemies  = 0
    jdbr         = False #Just Did Bonus Round
    shots_fired  = 0
    shots_hit    = 0
    accuracy     = 0
    pause_result = ''
    mus_pause    = False
    create       = True
    player_reload = 0

    #set up background
    draw_background()
    background.fill((64,64,64))

    player = Player()

    while lives > 0:
        clock.tick(50)

        player_reload += 20
        
        if not player.alive:
            if not jdbr and not start_of_new_level(level):
                explosion_sound.play()
                Explosion(player)
                lives -= 1
                if lives != 0:
                    score -= level_score
                level_score = 0
                level = float(int(level))
                create = True
            player = Player()
            num_enemies = clear_enemies(num_enemies)
            clear_bullets()
                
        Game_State = game_state(level,time,jdbr)

        if Game_State == 'bonus':
            if state_changed(Game_State, Prev_State):
                Prev_State = Game_State
                shots_fired = 0
                shots_hit = 0
            time -= clock.get_time()/1000.0
            max_enemies, num_enemies, prev_level = create_enemies(level,
                                    prev_level, time, jdbr, num_enemies, player)
            prev_level = level
        elif Game_State == 'game':
            if state_changed(Game_State, Prev_State):
                time = BONUS_START_TIME
                Prev_State = Game_State
                jdbr = True
                player.health = 0
                for target in target_group:
                    target.dead = True
                    num_enemies -= 1
                screen.blit(background, (0,0))
                bonus_points, accuracy = Level_Results.report(shots_fired,
                                                    shots_hit, level_score,jdbr)
                score += bonus_points
                bonus_points = 0
                if accuracy >= 85:
                    lives += 1
                level -= .1
                prev_level = level
            if state_changed(level,prev_level) or jdbr:
                if create:
                    max_enemies, num_enemies, prev_level = create_enemies(level,
                                    prev_level, time, jdbr,num_enemies, player)
                    create = False
            if num_enemies <= 0:
                prev_level = level
                level += .1
                clear_bullets()
                if int(str(level)[-1]) == 1:
                    jdbr = False
                create = True
                if start_of_new_level(level):
                    screen.blit(background, (0,0))
                    if not jdbr:
                        bonus_points, accuracy = Level_Results.report(shots_fired,
                                                    shots_hit, level_score, jdbr)
                    score += bonus_points
                    bonus_points = 0
                    shots_fired = 0
                    shots_hit = 0
                    level_score = 0
                    player.health = 0
                    if accuracy >=65:
                        lives += 1

        level, shots_fired, pause_result, mus_pause, player_reload = get_user_input(player,
                    level, shots_fired, pause_result, mus_pause, player_reload)

        if pause_result == 'main menu':
            screen.blit(background, (0,0))
            lives = 0
        elif pause_result == 'resume':
            screen.blit(background, (0,0))
            pause_result = ''

        score, level_score, num_enemies, shots_hit = detect_collisions(score,
                                            level_score, num_enemies, shots_hit)
        screen.blit(background, (0,0))
        draw_HUD(player, score, lives, level, time, jdbr, num_enemies)      
        update_all()

        if level > high_level:
            high_level = level

    Highscores.highscores(int(round(score)), high_level)
    return

if __name__ == '__main__':
    game('omnitank_blue.png')
