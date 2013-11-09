#7-11-2009
# initialization
import pygame, sys, os , os.path
from pygame.locals import *

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

def pause():
    pygame.init()
    Rect = screen.get_rect()
    wintitle = pygame.display.set_caption("OmniTank Pause Menu")
    pygame.mouse.set_visible(True)

    top = (367, 314)
    bottom = (367, 365)
    selection = ''
    playsound = False
    mus_pause = False
    

    # Image
    pause_file_name = os.path.join('images', 'pause_menu.png')
    selectionbar_file_name = os.path.join("images","selection_outline.png")
    outline = pygame.image.load(selectionbar_file_name)

    # Create background
    global background
    background = pygame.image.load(pause_file_name)
    screen.blit(background, (0,0))
    pygame.display.flip()

    # Load sounds
    roll_over_sound = load_sound('menu_rollover.wav')
    click_sound = load_sound('menu_click.wav')

    all = pygame.sprite.RenderUpdates()

    MenuOutline.containers = all

    while 1:
        time_passed = clock.tick(60)

        in_box1 = (pygame.mouse.get_pos()[0] <= 676 and
                   pygame.mouse.get_pos()[0] >= 367 and
                   pygame.mouse.get_pos()[1] <= 354 and
                   pygame.mouse.get_pos()[1] >= 314)
        in_box2 = (pygame.mouse.get_pos()[0] <= 676 and
                   pygame.mouse.get_pos()[0] >= 367 and
                   pygame.mouse.get_pos()[1] <= 405 and
                   pygame.mouse.get_pos()[1] >= 365)

        # Sound
        if (in_box1 or in_box2) and playsound:
            roll_over_sound.play()
            playsound = False
        if not (in_box1 or in_box2):
            playsound = True

        # User Input
        for event in pygame.event.get():
            if in_box1:
                MenuOutline(top, outline, 676, 367, 354, 314)
                selection = 'resume'
            elif in_box2:
                MenuOutline(bottom, outline, 676, 367, 405, 365)
                selection = 'main menu'
            else:
                selection = ''
            if event.type == MOUSEBUTTONDOWN: #or event.type == KEYDOWN:
                if selection == 'resume': #or event.key == K_p:
                    click_sound.play()
                    pygame.mouse.set_visible(False)
                    return selection
                elif selection == 'main menu':
                    click_sound.play()
                    return selection
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
    pause()
