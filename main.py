import pygame, sys, random
from pygame.locals import *

try:
    import android
except ImportError:
    android = None

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load("img/grass.png").convert()
        self.rect = self.image.get_rect()
        
class Plant(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/treenarrow.png").convert_alpha()
        self.rect = self.image.get_rect()
        
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/blue_boy_small.png").convert_alpha()
        self.rect = self.image.get_rect(center = (240, 160))
        


class Bullet(pygame.sprite.Sprite):
    def __init__(self, direction, character):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((3, 3))
        self.image.fill((255, 0, 0))
        self.image.convert()
        self.rect = self.image.get_rect()
        self.direction = direction
        self.speed = 7
        if self.direction == "right":
            self.rect.center = (character.rect.right, character.rect.centery)
        if self.direction == "left":
            self.rect.center = (character.rect.left, character.rect.centery)
        if self.direction == "up":
            self.rect.center = (character.rect.centerx, character.rect.top)
        if self.direction == "down":
            self.rect.center = (character.rect.centerx, character.rect.bottom)
        if self.direction == "topLeft":
            self.rect.center = (character.rect.left, character.rect.top)
        if self.direction == "bottomLeft":
            self.rect.center = (character.rect.left, character.rect.bottom)
        if self.direction == "topRight":
            self.rect.center = (character.rect.right, character.rect.top)
        if self.direction == "bottomRight":
            self.rect.center = (character.rect.right, character.rect.bottom)
            
            
    
    ### movement for bullet
    def update(self):
      
        if self.direction == "right":
            if self.rect.centerx < 480:
                self.rect.centerx += self.speed
            else:
                self.kill()
        if self.direction == "left":
            if self.rect.centerx > 0:
                self.rect.centerx -= self.speed
            else:
                self.kill()
        if self.direction == "up":
            if self.rect.centery > 0:
                self.rect.centery -= self.speed
            else:
                self.kill()
        if self.direction == "down":
            if self.rect.centery < 320:
                self.rect.centery += self.speed
            else:
                self.kill()
        ### Diagonal bullet firing movement
        if self.direction == "topLeft":
            if self.rect.centerx > 0 and self.rect.centery > 0:
                self.rect.centerx -= 4
                self.rect.centery -= 4
            else:
                self.kill()
           
        
        if self.direction == "bottomLeft":
            if self.rect.centerx > 0 and self.rect.centery < 320:
                self.rect.centerx -= 4
                self.rect.centery += 4
            else:
                self.kill()
            
            
        if self.direction == "topRight":
            if self.rect.centerx < 480 and self.rect.centery > 0:
                self.rect.centerx += 4
                self.rect.centery -= 4
            else:
                self.kill()
            
            
        if self.direction == "bottomRight":
            if self.rect.centerx < 480 and self.rect.centery < 320:
                self.rect.centerx += 4
                self.rect.centery += 4
            
        
        
        
        
        
class Controls(pygame.sprite.Sprite):
    def __init__(self, control_type):
        pygame.sprite.Sprite.__init__(self)
        if control_type == "move":
            self.image = pygame.image.load("img/arrows_transparent.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.top = 170
            self.rect.left = 10
        elif control_type == "fire":
            self.image = pygame.image.load("img/arrows_fire_directions.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.top = 170
            self.rect.left = 320
        self.button_size = 50
        self.direction = "stop"
    
    def movement(self):
        
        pos = pygame.mouse.get_pos()
        
        ## creates rectangles for movement
        self.rect_right_leftedge = self.rect.right - self.button_size
        self.rect_right_topedge = self.rect.top + self.button_size
        self.right_rect = pygame.Rect(self.rect_right_leftedge, self.rect_right_topedge,
                                      self.button_size, self.button_size)
        if self.right_rect.collidepoint(pos):
            self.direction = "right"
        
        self.rect_left_leftedge = self.rect.left 
        self.rect_left_topedge = self.rect.top + self.button_size
        self.left_rect = pygame.Rect(self.rect_left_leftedge, self.rect_left_topedge,
                                     self.button_size, self.button_size)
        if self.left_rect.collidepoint(pos):
            self.direction = "left"
            
        self.rect_down_leftedge = self.rect.left + self.button_size
        self.rect_down_topedge = self.rect.top + self.button_size + self.button_size
        self.down_rect = pygame.Rect(self.rect_down_leftedge, self.rect_down_topedge,
                                     self.button_size, self.button_size)
        if self.down_rect.collidepoint(pos):
            self.direction = "down"
            
        self.rect_up_leftedge = self.rect.left + self.button_size
        self.rect_up_topedge = self.rect.top 
        self.up_rect = pygame.Rect(self.rect_up_leftedge, self.rect_up_topedge,
                                     self.button_size, self.button_size)
        if self.up_rect.collidepoint(pos):
            self.direction = "up"
            
        self.rect_stop_leftedge = self.rect.left + self.button_size
        self.rect_stop_topedge = self.rect.top + self.button_size
        self.stop_rect = pygame.Rect(self.rect_stop_leftedge, self.rect_stop_topedge,
                                     self.button_size, self.button_size)
        if self.stop_rect.collidepoint(pos):
            self.direction = "stop"
            
        return(self.direction)
        
    def firing(self, character, bullet_group):
        
        pos = pygame.mouse.get_pos()
        
        
        ### creates the rectangles for firing
        self.rect_right_leftedge = self.rect.right - self.button_size
        self.rect_right_topedge = self.rect.top + self.button_size
        self.right_rect = pygame.Rect(self.rect_right_leftedge, self.rect_right_topedge,
                                      self.button_size, self.button_size)
        if self.right_rect.collidepoint(pos):
            direction = "right"
            bullet = Bullet(direction, character)
            bullet_group.add(bullet)
        
        self.rect_left_leftedge = self.rect.left 
        self.rect_left_topedge = self.rect.top + self.button_size
        self.left_rect = pygame.Rect(self.rect_left_leftedge, self.rect_left_topedge,
                                     self.button_size, self.button_size)
        if self.left_rect.collidepoint(pos):
            direction = "left"
            bullet = Bullet(direction, character)
            bullet_group.add(bullet)
            
        self.rect_down_leftedge = self.rect.left + self.button_size
        self.rect_down_topedge = self.rect.top + self.button_size + self.button_size
        self.down_rect = pygame.Rect(self.rect_down_leftedge, self.rect_down_topedge,
                                     self.button_size, self.button_size)
        if self.down_rect.collidepoint(pos):
            direction = "down"
            bullet = Bullet(direction, character)
            bullet_group.add(bullet)
            
        self.rect_up_leftedge = self.rect.left + self.button_size
        self.rect_up_topedge = self.rect.top 
        self.up_rect = pygame.Rect(self.rect_up_leftedge, self.rect_up_topedge,
                                     self.button_size, self.button_size)
        if self.up_rect.collidepoint(pos):
            direction = "up"
            bullet = Bullet(direction, character)
            bullet_group.add(bullet)
        
        ### directions for diagonal shooting controls    
        self.rect_TopLeftDiag_leftedge = self.rect.left
        self.rect_TopLeftDiag_topedge = self.rect.top
        self.TopLeftDiag_rect = pygame.Rect(self.rect_TopLeftDiag_leftedge, self.rect_TopLeftDiag_topedge,
                                            self.button_size, self.button_size)
        if self.TopLeftDiag_rect.collidepoint(pos):
            direction = "topLeft"
            bullet = Bullet(direction, character)
            bullet_group.add(bullet)
            
        self.rect_BottomLeftDiag_leftedge = self.rect.left
        self.rect_BottomLeftDiag_topedge = self.rect.top + self.button_size + self.button_size
        self.BottomLeftDiag_rect = pygame.Rect(self.rect_BottomLeftDiag_leftedge, self.rect_BottomLeftDiag_topedge,
                                               self.button_size, self.button_size)
        if self.BottomLeftDiag_rect.collidepoint(pos):
            direction = "bottomLeft"
            bullet = Bullet(direction, character)
            bullet_group.add(bullet)
            
        self.rect_TopRightDiag_leftedge = self.rect.right - self.button_size
        self.rect_TopRightDiag_topedge = self.rect.top
        self.TopRightDiag_rect = pygame.Rect(self.rect_TopRightDiag_leftedge, self.rect_TopRightDiag_topedge,
                                             self.button_size, self.button_size)
        if self.TopRightDiag_rect.collidepoint(pos):
            direction = "topRight"
            bullet = Bullet(direction, character)
            bullet_group.add(bullet)
            
        self.rect_BottomRightDiag_leftedge = self.rect.right - self.button_size
        self.rect_BottomRightDiag_topedge = self.rect.top + self.button_size + self.button_size
        self.BottomRightDiag_rect = pygame.Rect(self.rect_BottomRightDiag_leftedge, self.rect_BottomRightDiag_topedge,
                                                self.button_size, self.button_size)
        if self.BottomRightDiag_rect.collidepoint(pos):
            direction = "bottomRight"
            bullet = Bullet(direction, character)
            bullet_group.add(bullet)
        
        
        return(bullet_group)
        
class Monster(pygame.sprite.Sprite):
    def __init__(self):
        ## use the line below in all sprite initialization
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/monster_small.png").convert_alpha()
        self.rect = self.image.get_rect()
        
        self.safe_surf = pygame.Surface((480, 320))
        #self.safe_surf.fill((0, 255, 0))
        #self.safe_surf.set_alpha(60)
        self.safe_zone = self.safe_surf.get_rect()
        self.safe_zone.center = (240, 160)
        
        self.in_safe = False
        while not self.in_safe:
            self.rect.right = random.randrange(480, 800)
            self.rect.top = random.randrange(-300, 0)
            if self.rect.colliderect(self.safe_zone):
                pass
            else:
                self.in_safe = True
                
        
        #self.rect.top = random.randrange(20, 290)
        self.speed = 1
    
    def update(self, character):
        self.char = character
        x = self.char.rect.centerx
        y = self.char.rect.centery
        if self.rect.centerx > x:
            self.rect.centerx -= self.speed
        if self.rect.centerx < x:
            self.rect.centerx += self.speed
        if self.rect.centery > y:
            self.rect.centery -= self.speed
        if self.rect.centery < y:
            self.rect.centery += self.speed
    
    #def uncrowd(self):
    #    self.speed = random.randrange(0, 4)

def uncrowd(mon_group):
    temp_group = mon_group.copy()
    for mon in mon_group:
        temp_group.remove(mon)
        if pygame.sprite.spritecollideany(mon, temp_group):
           mon.rect.centerx += random.randint(-10, 10)
           mon.rect.centery += random.randint(-10, 10)
        
        
           
class Timer():
    def __init__(self):
        self.start_time = pygame.time.get_ticks()
        self.trigger = False
        self.level = 1
        self.RED = (255, 0, 0)
        self.lightBlue = (0, 254, 237)
        self.GreenYellow = (160, 195, 7)
        self.initTimer()
        
        
    def initTimer(self):
       self.gameFont = pygame.font.Font("fonts/ASTONISH.TTF", 16)
       self.timeSprite = pygame.sprite.Sprite()
       self.timeSprite.image = self.gameFont.render("Time: ", True , self.RED)
       self.timeSprite.rect = self.timeSprite.image.get_rect(left = 90, top = 10)
       self.time_group = pygame.sprite.Group(self.timeSprite)
        
        
    def update(self, monster_group, windowSurface, superMonster_group, superMonster2_group, character, direction, forest_group):
        self.windowSurface = windowSurface
        self.monster_group = monster_group
        self.superMonster_group = superMonster_group
        self.character = character
        self.direction = direction
        self.forest_group = forest_group
        self.superMonster2_group = superMonster2_group
        self.elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        self.timeSprite.image = self.gameFont.render("Time: " + str(self.elapsed_time), True, self.RED, self.GreenYellow)
        self.CalcLevel()
        self.createMonsters()
        return(self.monster_group, self.time_group, self.windowSurface, self.superMonster_group, self.superMonster2_group, self.character, self.direction, self.forest_group)
       
    def CalcLevel(self):
        if len(self.monster_group) == 0 and self.level == 7:
            self.level = 8
            self.trigger = False
            
        if len(self.monster_group) == 0 and self.level == 6:
            self.level = 7
            self.trigger = False
            
        if len(self.monster_group) == 0 and self.level == 5:
            self.level = 6
            self.trigger = False
        
        if len(self.monster_group) == 0 and self.level == 4:
            self.level = 5
            self.trigger = False
            
        if len(self.monster_group) == 0 and self.level == 3:
            self.level = 4
            self.trigger = False
            
        if len(self.monster_group) == 0 and self.level == 2:
            self.level = 3
            self.trigger = False

        if len(self.monster_group) == 0 and self.level == 1:
            self.level = 2
            self.trigger = False
            
        
            
    def createMonsters(self):
        Green = (0, 255, 0)
        Pink = (255, 18, 248)
        level_rect = pygame.Rect(10, 10, 470, 310)
        level_rect2 = pygame.Rect(220, 85, 200, 100)
        levelFont = pygame.font.Font("fonts/BLOODY.ttf", 60)
        level_text = levelFont.render("Moving to Level ", False, Pink)
        level_text2 = levelFont.render(str(self.level), False, Pink)
        
        if self.trigger == False and self.level > 1:
            self.windowSurface.fill(Green)
            ## blit statement for the "changing levels
            self.windowSurface.blit(level_text, level_rect)
            self.windowSurface.blit(level_text2, level_rect2)
            pygame.display.update()
            pygame.time.wait(3000)
            self.character.rect.center = (240, 160)
            self.direction = "stop"
            
            ## blits the super Monsters at the beginning of each level
            superMonster2 = Monster()
            superMonster2.image = pygame.image.load("img/superMonster_crab.png").convert_alpha()
            superMonster2.rect.center = (random.randint(400, 500), random.randint(-120, 20))
            superMonster2.speed_trigger = 0
            superMonster2.current_trigger = 1
            self.superMonster2_group.empty()
            self.superMonster2_group.add(superMonster2)
            
            superMonster = Monster()
            superMonster.image = pygame.image.load("img/SuperMonster_mummy.png")
            superMonster.image.convert_alpha()
            superMonster.rect.center = (random.randint(400, 500), random.randint(150, 340))
            superMonster.speed_trigger = 1
            superMonster.current_trigger = 0
            self.superMonster_group.empty()
            self.superMonster_group.add(superMonster)
            
            
            if self.level == 2:
                tree = Plant()
                tree.rect.center = (15, 45)
                tree2 = Plant()
                tree2.rect.center = (460, 45)
                tree3 = Plant()
                tree3.rect.center = (15, 294)
                tree4 = Plant()
                tree4.rect.center = (460, 294)
                self.forest_group.add(tree, tree2, tree3, tree4)
            
            if self.level == 3:
                self.forest_group.empty()
                for x in range(10, 470, 32):
                    y = 35
                    tree = Plant()
                    tree.rect.center = (x, y)
                    self.forest_group.add(tree)
            
            if self.level == 4:
                for x in range(10, 470, 32):
                    y = 310
                    cactus = Plant()
                    cactus.image = pygame.image.load("img/cactus.png")
                    cactus.image.convert_alpha()
                    cactus.rect.center = (x, y)
                    self.forest_group.add(cactus)
            
            if self.level == 5:
                self.forest_group.empty()
                for x1 in range(40, 440, 30):
                    y1 = 50
                    pillar = Plant()
                    pillar.image = pygame.image.load("img/pillar.png")
                    pillar.image.convert_alpha()
                    pillar.rect.center = (x1, y1)
                for x2 in range(40, 440, 30):
                    y2 = 100
                    pillar2 = Plant()
                    pillar2.image = pygame.image.load("img/pillar.png")
                    pillar.image.convert_alpha()
                    pillar2.rect.center = (x2, y2)
                for x3 in range(40, 440, 30):
                    y3 = 150
                    pillar3 = Plant()
                    pillar3.image = pygame.image.load("img/pillar.png")
                    pillar3.image.convert_alpha()
                    pillar3.rect.center = (x3, y3)
                for x4 in range(40, 440, 30):
                    y4 = 200
                    pillar4 = Plant()
                    pillar4.image = pygame.image.load("img/pillar.png")
                    pillar4.image.convert_alpha()
                    pillar4.rect.center = (x4, y4)
                    
                
                
                    self.forest_group.add(pillar, pillar2, pillar3, pillar4)
                    
            if self.level == 6:
                self.forest_group.empty()
                for y in range(40, 260, 70):
                    for x in range(180, 330, 70):
                        dragon = Plant()
                        dragon.image = pygame.image.load("img/dragon.png")
                        dragon.image.convert_alpha()
                        dragon.rect.center = (x, y)
                        self.forest_group.add(dragon)
                    
            
            if self.level == 7:
                self.forest_group.empty()
                for x1 in range(30, 100, 30):
                    y1 = 100
                    pillar1 = Plant()
                    pillar1.image = pygame.image.load("img/pillar.png")
                    pillar1.image.convert_alpha()
                    pillar1.rect = pillar1.image.get_rect()
                    pillar1.rect.center = (x1, y1)
                    self.forest_group.add(pillar1)
                for x2 in range(15, 65, 30):
                    y2 = 200
                    pillar2 = Plant()
                    pillar2.image = pygame.image.load("img/pillar.png")
                    pillar2.image.convert_alpha()
                    pillar2.rect = pillar2.image.get_rect()
                    pillar2.rect.center = (x2, y2)
                    self.forest_group.add(pillar2)
                    
                statue1 = Plant()
                statue1.image = pygame.image.load("img/statue.png")
                statue1.image.convert_alpha()
                statue1.rect = statue1.image.get_rect()
                statue1.rect.center = (240, 100)
                statue2 = Plant()
                statue2.image = pygame.image.load("img/statue.png")
                statue2.image.convert_alpha()
                statue2.rect = statue2.image.get_rect()
                statue2.rect.center = (240, 220)
                statue3 = Plant()
                statue3.image = pygame.image.load("img/statue.png")
                statue3.image.convert_alpha()
                statue3.rect = statue3.image.get_rect()
                statue3.rect.center = (180, 160)
                statue4 = Plant()
                statue4.image = pygame.image.load("img/statue.png")
                statue4.image.convert_alpha()
                statue4.rect = statue4.image.get_rect()
                statue4.rect.center = (300, 160)
                
                for x3 in range(380, 460, 30):
                    y3 = 100
                    rubble = Plant()
                    rubble.image = pygame.image.load("img/rubble.png")
                    rubble.image.convert_alpha()
                    rubble.rect = rubble.image.get_rect()
                    rubble.rect.center = (x3, y3)
                    self.forest_group.add(rubble)
                for x4 in range(380, 460, 30):
                    y4 = 200
                    bones = Plant()
                    bones.image = pygame.image.load("img/bones.png")
                    bones.image.convert_alpha()
                    bones.rect = bones.image.get_rect()
                    bones.rect.center = (x4, y4)
                    self.forest_group.add(bones)
                
                self.forest_group.add(statue1, statue2, statue3, statue4)
                
                
                
            if self.level == 8:
                self.forest_group.empty()
                lightThrone = Plant()
                lightThrone.image = pygame.image.load("img/lightThrone.png")
                lightThrone.image.convert_alpha()
                lightThrone.rect.center = (420, 120)
                
                darkThrone = Plant()
                darkThrone.image = pygame.image.load("img/darkThrone.png")
                darkThrone.image.convert_alpha()
                darkThrone.rect.center = (60, 120)
                
                coffin = Plant()
                coffin.image = pygame.image.load("img/coffin.png")
                coffin.image.convert_alpha()
                coffin.rect.center = (240, 160)
                
                for x in range(160, 320, 42):
                    y = 300
                    knight = Plant()
                    knight.image = pygame.image.load("img/knight.png")
                    knight.image.convert_alpha()
                    knight.rect.center = (x, y)
                    self.forest_group.add(knight)
                    
                for x2 in range(340, 420, 28):
                    y2 = 50
                    crystal = Plant()
                    crystal.image = pygame.image.load("img/crystal.png")
                    crystal.image.convert_alpha()
                    crystal.rect = crystal.image.get_rect()
                    crystal.rect.center = (x2, y2)
                    self.forest_group.add(crystal)
                    
                for x3 in range(60, 140, 32):
                    y3 = 50
                    bones = Plant()
                    bones.image = pygame.image.load("img/bones.png")
                    bones.image.convert_alpha()
                    bones.rect = bones.image.get_rect()
                    bones.rect.center = (x3, y3)
                    self.forest_group.add(bones)
                
                self.forest_group.add(lightThrone, darkThrone, coffin)
                
                    
            
            self.monster_num = 6 + (self.level * 3)
            print("The level is " + str(self.level))
            print(str(self.monster_num) + " monsters created")
            print ("--------------------------------")
            
            for number in range(0, self.monster_num):
                monster = Monster()
                self.monster_group.add(monster)
                
                
            self.trigger = True
            
            
class Health():
    def __init__(self):
        self.alive = True
            
           



def main():
    
    pygame.init()
    
    clock = pygame.time.Clock()
    FPS = 30
    
    ### Load the awesome sunset
    sunset = pygame.image.load("img/sunset.jpg")
    
    windowSurface = pygame.display.set_mode((480, 320), 0, 32)
    warningSurface = pygame.Surface((480, 320))
    warning_rect = warningSurface.get_rect()
    warningSurface.fill((0, 0, 255))
    warningSurface.set_alpha(150)
    
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    PINK = (254, 15, 234)
    direction = ("stop")
    LIGHTBLUE = (0, 255, 252)
    DARKRED = (198, 46, 46)
    GREEN = (0, 255, 0)
    
    field_column = []
    forest_group = pygame.sprite.Group()
    
    for y in range(0, 320, 32):
        grass = Ground()
        grass.rect.right = 480
        grass.rect.top = y
        field_column.append(grass)
    
    ### initialize the tree + set pos
    x = 150
    for y in range(150, 320, 64):
        tree = Plant()
        tree.rect.center = (x, y)
        x = x + 32
        forest_group.add(tree)
        
    ## initialize the controls for pla yer
    controls = Controls("move")
    
    ## initialize the controls for shooting
    fire = Controls("fire")
    stop = pygame.sprite.Sprite()
    stop.image = pygame.Surface((40, 40))
    stop.rect = stop.image.get_rect()
    stop.rect.center = controls.rect.center
    stop.image.fill((199, 255, 0))
    stop.image.set_alpha(85)
    controls_group = pygame.sprite.Group(controls, fire, stop)
    

    ## instantiate the condition of the players life
    health = Health()
        
    
    ## Create a rectangle for the "Player DEAD :)
    endFont = pygame.font.Font("fonts/BLOODY.ttf", 130)
    endText = endFont.render("DEAD", True , RED)
    endText_rect = pygame.Rect(80, 150, 200, 200)
    
    ### Create a rectangle for Play Again 
    playAgain_font = pygame.font.Font("fonts/ASTONISH.TTF", 80)
    playAgain_text = playAgain_font.render("Play Again? ", True, LIGHTBLUE)
    playAgain_rect = pygame.Rect(10, 10, 480, 180)
    
    ### Create a rectangle for Play Again = No
    no_font = pygame.font.Font("fonts/BLOODY.ttf", 45)
    no_text = no_font.render("No...", True, DARKRED)
    no_rect = pygame.Rect(320, 100, 150, 60)
    
    ### Create a rectangle for Play Again = Yes
    yes_font = pygame.font.Font("fonts/ASTONISH.TTF", 60)
    yes_text = yes_font.render("YES!!!", True, GREEN)
    yes_rect = pygame.Rect(40, 90, 150, 60)
    
    ### Create a rectangle for the PLAYER HERO :)
    winFont = pygame.font.Font("fonts/ASTONISH.TTF", 90)
    winText = winFont.render("HERO", True, PINK)
    winText_rect = pygame.Rect(60, 230, 200, 200)
    
    ## Create a rectangle for large hero
    char_large = pygame.image.load("img/blue_boy_large.png")
    char_rect = char_large.get_rect(left = 220, bottom = 240)
            
    ## Create rectangle for girl
    girl = pygame.image.load("img/girl.png")
    girl_rect = girl.get_rect(left = 170, bottom = 210)
            
    ## initialize the player
    character = Player()
    
    ## initialize the bullet + create the bullet_group
    bullet_group = pygame.sprite.Group()
    
    ### initialize the monseter
    monster_group = pygame.sprite.Group()
    superMonster_group = pygame.sprite.Group()
    superMonster2_group = pygame.sprite.Group()
    for number in range(0, 8):
        monster = Monster()
        monster_group.add(monster)
    
    ## instantiate the super zombie
    superMonster = Monster()
    superMonster.image = pygame.image.load("img/SuperMonster_mummy.png")
    superMonster.image.convert_alpha()
    superMonster.rect.center = (random.randint(400, 500), random.randint(150, 340))
    superMonster.speed_trigger = 1
    superMonster.current_trigger = 0
    superMonster_group.add(superMonster)
    
    ## instantiate the super zombie2 ze CRAB
    superMonster2 = Monster()
    superMonster2.image = pygame.image.load("img/superMonster_crab.png").convert_alpha()
    superMonster2.rect.center = (random.randint(400, 500), random.randint(-120, 20))
    superMonster2.speed_trigger = 0
    superMonster2.current_trigger = 1
    superMonster2_group.add(superMonster2)
    


    ## initialize the clock
    timer = Timer()
    
    
    if android:
        android.init()
        android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
    
    gameOn = True
    
    
    while gameOn:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    gameOn = False
            if event.type == MOUSEBUTTONDOWN:
                bullet_group = fire.firing(character, bullet_group)
                direction = controls.movement()
                if health.alive == False:
                    if no_rect.collidepoint(pygame.mouse.get_pos()):
                        pygame.quit()
                        sys.exit()
                    elif yes_rect.collidepoint(pygame.mouse.get_pos()):
                        main()
                
       
        for x in range(480, 0, -32):
            for grass in field_column:
                grass.rect.right = x
                windowSurface.blit(grass.image, grass.rect)
                
    
                
        ## blits the tree
        for tree in forest_group:
            windowSurface.blit(tree.image, tree.rect)
        
        ## blit the controls for the player and shooting
        controls_group.draw(windowSurface)
    
        ### blit the timer onto the screen
        monster_group, time_group, windowSurface, superMonster_group, superMonster2_group, character, direction, forest_group = timer.update(monster_group, windowSurface,
                                                                           superMonster_group, superMonster2_group, character, direction, forest_group)
        time_group.draw(windowSurface)
        
        
        
        
        ## movement for character
        if direction == "right" and character.rect.right <= 480:
            character.rect.centerx = character.rect.centerx + 5
        if direction == "left" and character.rect.left >= 0:
            character.rect.centerx = character.rect.centerx - 5
        if direction == "up" and character.rect.top >= 0:
            character.rect.centery = character.rect.centery - 5
        if direction == "down" and character.rect.bottom <= 320:
            character.rect.centery = character.rect.centery + 5
            
        
        ### Collision detection for trees
        for tree in forest_group:
            if tree.rect.collidepoint(character.rect.center):
                direction = "stop"
        
        
        ## blits the player
        windowSurface.blit(character.image, character.rect)
        ## blits the monster
        ##windowSurface.blit(monster.image, monster.rect)
        monster_group.update(character)
        monster_group.draw(windowSurface)
        uncrowd(monster_group)
        if superMonster.current_trigger < superMonster.speed_trigger:
            superMonster.current_trigger = superMonster.current_trigger + 1
        else:
            superMonster_group.update(character)
            superMonster.current_trigger = 0
        if superMonster2.current_trigger < superMonster2.speed_trigger:
            superMonster2.current_trigger = superMonster2.current_trigger + 1
        else:
            superMonster2_group.update(character)
            superMonster2.current_trigger = 0
        superMonster2_group.draw(windowSurface)
        superMonster_group.draw(windowSurface)
    
        
        ## Test for collision between player and zombie
        if pygame.sprite.spritecollideany(character, superMonster_group):
            windowSurface.blit(warningSurface, warning_rect)
            health.alive = False
            
        if pygame.sprite.spritecollideany(character, superMonster2_group):
            windowSurface.blit(warningSurface, warning_rect)
            health.alive = False
        
        
        
        if health.alive == True and timer.level == 8 and len(monster_group) == 0:
            windowSurface.blit(sunset, warning_rect)
            windowSurface.blit(winText, winText_rect)
            windowSurface.blit(char_large, char_rect)
            windowSurface.blit(girl, girl_rect)
            superMonster_group.empty()
            superMonster2_group.empty()
            
        
        ## blits the bullets
        bullet_group.update()
        bullet_group.draw(windowSurface)
        
        ## collision detection for the monster and bullet
        pygame.sprite.groupcollide(bullet_group, monster_group, True, True)
        pygame.sprite.groupcollide(bullet_group, superMonster_group, True, False)
        pygame.sprite.groupcollide(bullet_group, forest_group, True, False)
        pygame.sprite.groupcollide(bullet_group, superMonster2_group, True, False)
            
            
        if pygame.sprite.spritecollideany(character, monster_group):
            windowSurface.blit(warningSurface, warning_rect)
            health.alive = False
        if health.alive == False:
            # blit statement for "Player DEAD"
            windowSurface.fill(BLACK)
            windowSurface.blit(endText, endText_rect)
            windowSurface.blit(playAgain_text, playAgain_rect)
            
            windowSurface.blit(no_text, no_rect)
            windowSurface.blit(yes_text, yes_rect)
            

        
            
        pygame.display.update()
        clock.tick(FPS)
        
main()