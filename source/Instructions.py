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

def instructions():
    pygame.init()
    Rect = screen.get_rect()
    wintitle = pygame.display.set_caption("OmniTank Instructions")

    box = (676, 39)
    selection = ''
    playsound = False
    mus_pause = False

    # Image
    instructions_file_name = os.path.join('images', 'instructions.png')
    selectionbar_file_name = os.path.join("images","selection_outline.png")
    outline = pygame.image.load(selectionbar_file_name)

    # Create background
    background = pygame.image.load(instructions_file_name)
    screen.blit(background, (0,0))
    pygame.display.flip()

    # Load sounds
    roll_over_sound = load_sound('menu_rollover.wav')
    click_sound = load_sound('menu_click.wav')

    all = pygame.sprite.RenderUpdates()

    MenuOutline.containers = all

    while 1:
        time_passed = clock.tick(60)

        in_box = (pygame.mouse.get_pos()[0] <= 966 and
                  pygame.mouse.get_pos()[0] >= 676 and
                  pygame.mouse.get_pos()[1] <= 79 and
                  pygame.mouse.get_pos()[1] >= 39)

        # Sound
        if in_box and playsound:
            roll_over_sound.play()
            playsound = False
        if not in_box:
            playsound = True

        # User Input
        for event in pygame.event.get():
            if in_box:
                MenuOutline(box, outline, 966, 676, 79, 39)
                selection = 'menu'
            if event.type == MOUSEBUTTONDOWN:
                if selection == 'menu':
                    click_sound.play()
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
    instructions()
