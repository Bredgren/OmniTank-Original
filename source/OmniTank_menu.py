#30-10-2009
# initialization
import pygame, sys, os , os.path
from pygame.locals import *
import color_choice, Instructions, Highscores


screen = pygame.display.set_mode((1024, 768))
clock = pygame.time.Clock()
mainmenu_file_name = os.path.join("images","main_menu.png")
background = pygame.image.load(mainmenu_file_name)

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
    wintitle = pygame.display.set_caption("OmniTank Menu")

def menu():
    pygame.init()
    Rect = screen.get_rect()
    pygame.mouse.set_visible(True)

    top = (367, 311)
    second = (367, 363)
    third = (367, 413)
    bottom = (367, 465)
    x_left = 367
    x_right = 657
    selection = ''
    playsound = False
    running = True
    mus_pause = False

    #images
    selectionbar_file_name = os.path.join("images","selection_outline.png")
    outline = pygame.image.load(selectionbar_file_name)

    icon_img = os.path.join("images", "icon.png")
    icon = pygame.image.load(icon_img)
    pygame.display.set_icon(icon)

    # Create background
    returnscreen()

    # Load sounds
    roll_over_sound = load_sound('menu_rollover.wav')
    click_sound = load_sound('menu_click.wav')

    #load/start music
    pygame.mixer.music.load(os.path.join('sounds', 'Mechanolith.mp3'))
    pygame.mixer.music.play(-1)

    all = pygame.sprite.RenderUpdates()

    MenuOutline.containers = all

    while running:
        time_passed = clock.tick(60)

        in_box1 = (pygame.mouse.get_pos()[0] <= x_right and
                   pygame.mouse.get_pos()[0] >= x_left and
                   pygame.mouse.get_pos()[1] <= 351 and
                   pygame.mouse.get_pos()[1] >= 311)
        in_box2 = (pygame.mouse.get_pos()[0] <= x_right and
                   pygame.mouse.get_pos()[0] >= x_left and
                   pygame.mouse.get_pos()[1] <= 402 and
                   pygame.mouse.get_pos()[1] >= 363)
        in_box3 = (pygame.mouse.get_pos()[0] <= x_right and
                   pygame.mouse.get_pos()[0] >= x_left and
                   pygame.mouse.get_pos()[1] <= 452 and
                   pygame.mouse.get_pos()[1] >= 413)
        in_box4 = (pygame.mouse.get_pos()[0] <= x_right and
                   pygame.mouse.get_pos()[0] >= x_left and
                   pygame.mouse.get_pos()[1] <= 505 and
                   pygame.mouse.get_pos()[1] >= 465)
        # Sound
        if (in_box1 or in_box2 or in_box3 or in_box4) and playsound:
            roll_over_sound.play()
            playsound = False
        if not (in_box1 or in_box2 or in_box3 or in_box4):
            playsound = True
            

        # User Input
        for event in pygame.event.get():
            if in_box1:
                MenuOutline(top, outline, x_right, x_left, 351, 311)
                selection = 'start game'
            elif in_box2:
                MenuOutline(second, outline, x_right, x_left, 402, 363)
                selection = 'instructions'
            elif in_box3:
                MenuOutline(third, outline, x_right, x_left, 452, 413)
                selection = 'highscores'
            elif in_box4:
                MenuOutline(bottom, outline, x_right, x_left, 505, 465)
                selection = 'quit'
            else:
                selection = ''
            if event.type == MOUSEBUTTONDOWN:
                if selection == 'start game':
                    click_sound.play()
                    game = color_choice.color_choice()
                    returnscreen()
                elif selection == 'instructions':
                    click_sound.play()
                    instructions = Instructions.instructions()
                    returnscreen()
                elif selection == 'highscores':
                    click_sound.play()
                    highscores = Highscores.highscores(None, 0)
                    returnscreen()
                elif selection == 'quit':
                    click_sound.play()
                    pygame.time.delay(300)
                    running = False
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

    sys.exit(0)

if __name__ == '__main__':
    menu()
    
