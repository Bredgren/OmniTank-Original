#1-11-2009
# initialization
import pygame, sys, os , os.path
from pygame.locals import *
from OmniTank import *

screen = pygame.display.set_mode((1024, 768))
clock = pygame.time.Clock()

class MenuOutline(pygame.sprite.Sprite):
    def __init__(self, pos, image, x1, x2, y1, y2):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = image
        self.pos = pos
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        if not(pygame.mouse.get_pos()[0] <= self.x1 and
               pygame.mouse.get_pos()[0] >= self.x2 and
               pygame.mouse.get_pos()[1] <= self.y1 and
               pygame.mouse.get_pos()[1] >= self.y2):
            self.kill()

class dummysound:
    def play(self): pass
    
def load_sound(file):
    if not pygame.mixer: return dummysound()
    file = os.path.join('sounds', file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print ('Warning, unable to load, %s' % file)
    return dummysound()

def returnscreen():
    screen.blit(background, (0,0))
    pygame.display.flip()

def color_choice():
    pygame.init()
    Rect = screen.get_rect()
    wintitle = pygame.display.set_caption("OmniTank Color Choice")

    y_value = 310
    main_box = (634, 526)
    blue_box = (152, y_value)
    red_box = (302, y_value)
    green_box = (452, y_value)
    dark_box = (602, y_value)
    light_box = (752, y_value)
    selection = ''
    playsound = False
    mus_pause = False

    # Image
    tankcolor_file_name = os.path.join('images', 'tank_color.png')
    selectionbar_file_name = os.path.join("images","selection_outline.png")
    selectionbar2_file_name = os.path.join("images","tank_outline.png")
    outline = pygame.image.load(selectionbar_file_name)
    outline2 = pygame.image.load(selectionbar2_file_name)

    # Create background
    background = pygame.image.load(tankcolor_file_name)
    screen.blit(background, (0,0))
    pygame.display.flip()

    # Load sounds
    roll_over_sound = load_sound('menu_rollover.wav')
    click_sound = load_sound('menu_click.wav')

    all = pygame.sprite.RenderUpdates()

    MenuOutline.containers = all

    while 1:
        time_passed = clock.tick(60)

        in_box_main = (pygame.mouse.get_pos()[0] <= 924 and
                       pygame.mouse.get_pos()[0] >= 634 and
                       pygame.mouse.get_pos()[1] <= 566 and
                       pygame.mouse.get_pos()[1] >= 526)
        in_box_blue = (pygame.mouse.get_pos()[0] <= 272 and
                       pygame.mouse.get_pos()[0] >= 152 and
                       pygame.mouse.get_pos()[1] <= y_value + 150 and
                       pygame.mouse.get_pos()[1] >= y_value)
        in_box_red = (pygame.mouse.get_pos()[0] <= 422 and
                      pygame.mouse.get_pos()[0] >= 302 and
                      pygame.mouse.get_pos()[1] <= y_value + 150 and
                      pygame.mouse.get_pos()[1] >= y_value)
        in_box_green = (pygame.mouse.get_pos()[0] <= 572 and
                        pygame.mouse.get_pos()[0] >= 452 and
                        pygame.mouse.get_pos()[1] <= y_value + 150 and
                        pygame.mouse.get_pos()[1] >= y_value)
        in_box_dark = (pygame.mouse.get_pos()[0] <= 722 and
                       pygame.mouse.get_pos()[0] >= 602 and
                       pygame.mouse.get_pos()[1] <= y_value + 150 and
                       pygame.mouse.get_pos()[1] >= y_value)
        in_box_light = (pygame.mouse.get_pos()[0] <= 872 and
                        pygame.mouse.get_pos()[0] >= 752 and
                        pygame.mouse.get_pos()[1] <= y_value + 150 and
                        pygame.mouse.get_pos()[1] >= y_value)

        # Sound
        if (in_box_main or in_box_blue or in_box_red or in_box_green or
            in_box_dark or in_box_light) and playsound:
            roll_over_sound.play()
            playsound = False
        if not (in_box_main or in_box_blue or in_box_red or in_box_green or
                in_box_dark or in_box_light):
            playsound = True

        # User Input
        for event in pygame.event.get():
            if in_box_main:
                MenuOutline(main_box, outline, 924, 634, 566, 526)
                selection = 'menu'
            elif in_box_blue:
                MenuOutline(blue_box, outline2, 272, 152, y_value+150, y_value)
                selection = 'blue'
            elif in_box_red:
                MenuOutline(red_box, outline2, 422, 302, y_value+150, y_value)
                selection = 'red'
            elif in_box_green:
                MenuOutline(green_box, outline2, 572, 452, y_value+150, y_value)
                selection = 'green'
            elif in_box_dark:
                MenuOutline(dark_box, outline2, 722, 602, y_value+150, y_value)
                selection = 'dark'
            elif in_box_light:
                MenuOutline(light_box, outline2, 872, 752, y_value+150, y_value)
                selection = 'light'
            if event.type == MOUSEBUTTONDOWN:
                if selection == 'menu':
                    click_sound.play()
                    return
                elif selection == 'blue':
                    game('omnitank_blue.png')
                    return
                elif selection == 'red':
                    game('omnitank_red.png')
                    return
                elif selection == 'green':
                    game('omnitank_green.png')
                    return
                elif selection == 'dark':
                    game('omnitank_dark.png')
                    return
                elif selection == 'light':
                    game('omnitank_light.png')
                    return
            if event.type == KEYDOWN:
                if event.key == K_m:
                    if mus_pause:
                        mus_pause = False
                        pygame.mixer.music.unpause()
                    else:
                        mus_pause = True
                        pygame.mixer.music.pause()
                    

        all.clear(screen, background)
        all.update()
        dirty = all.draw(screen)
        pygame.display.update(dirty)

if __name__ == '__main__':
    color_choice()
