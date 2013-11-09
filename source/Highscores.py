#1-11-2009
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

def draw_message(position, size, message):
    """
        position format --> (x,y)
        size format --> just a number
        message format --> "message"
    """
    
    dark_blue    = (89,141,178)
    font = pygame.font.SysFont('arial', size)
    Message = font.render(message, True, dark_blue)
    screen.blit(Message, position)

def draw_rect(position, size):
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
    screen.fill((79,79,79), (pos_x, pos_y, size_x, size_y))

def highscore(score, score_list):
    """
        Retruns True or False if the player's score is a high score
    """

    if score >= score_list[-1]:
        return True
    else: return False

def gname(score, level):
    name = ''
    max_chr = 10
    again = True
    draw_message((390,370), 25, str(score))
    draw_message((630,370), 25, str(level))
    pygame.display.flip()
    while again:
        for event in pygame.event.get():
            if not hasattr(event, 'key'):
                continue
            down = event.type == KEYDOWN
            if event.key == K_a and down and len(name) < max_chr:
                name += 'A'
            elif event.key == K_b and down and len(name) < max_chr:
                name += 'B'
            elif event.key == K_c and down and len(name) < max_chr:
                name += 'C'
            elif event.key == K_d and down and len(name) < max_chr:
                name += 'D'
            elif event.key == K_e and down and len(name) < max_chr:
                name += 'E'
            elif event.key == K_f and down and len(name) < max_chr:
                name += 'F'
            elif event.key == K_g and down and len(name) < max_chr:
                name += 'G'
            elif event.key == K_h and down and len(name) < max_chr:
                name += 'H'
            elif event.key == K_i and down and len(name) < max_chr:
                name += 'I'
            elif event.key == K_j and down and len(name) < max_chr:
                name += 'J'
            elif event.key == K_k and down and len(name) < max_chr:
                name += 'K'
            elif event.key == K_l and down and len(name) < max_chr:
                name += 'L'
            elif event.key == K_m and down and len(name) < max_chr:
                name += 'M'
            elif event.key == K_n and down and len(name) < max_chr:
                name += 'N'
            elif event.key == K_o and down and len(name) < max_chr:
                name += 'O'
            elif event.key == K_p and down and len(name) < max_chr:
                name += 'P'
            elif event.key == K_q and down and len(name) < max_chr:
                name += 'Q'
            elif event.key == K_r and down and len(name) < max_chr:
                name += 'R'
            elif event.key == K_s and down and len(name) < max_chr:
                name += 'S'            
            elif event.key == K_t and down and len(name) < max_chr:
                name += 'T'            
            elif event.key == K_u and down and len(name) < max_chr:
                name += 'U'            
            elif event.key == K_v and down and len(name) < max_chr:
                name += 'V'
            elif event.key == K_w and down and len(name) < max_chr:
                name += 'W'
            elif event.key == K_x and down and len(name) < max_chr:
                name += 'X'
            elif event.key == K_y and down and len(name) < max_chr:
                name += 'Y'
            elif event.key == K_z and down and len(name) < max_chr:
                name += 'Z'
            elif event.key == K_SPACE and down and len(name) < max_chr:
                name += ' '
            elif event.key == K_BACKSPACE and down:
                name = name[:-1]
            elif event.key == K_RETURN and down:
                again = False
            draw_rect((390,320), (300,30))
            draw_message((390,320), 25, name)
            pygame.display.flip()
    return name

def update_scores(score, level, name, score_list, level_list, name_list):
    #update score list
    score_list.append(score)
    score_list.sort()
    score_list.reverse()
    score_list = score_list[:-1]

    #update name list
    name_list.insert(score_list.index(score), name)
    name_list = name_list[:-1]

    #update level list
    level_list.insert(score_list.index(score), level)
    level_list = level_list[:-1]

    return score_list, name_list, level_list

def rewrite_file(name_list, score_list, level_list):
    outfile = open("highscores.txt", 'w')
    for i in range(10):
        outfile.write("%s:%s:%s\n" %(name_list[i],score_list[i],level_list[i]))
    outfile.close()
        
def display_scores(name_list, score_list, level_list):
    message = ''
    for i in range(10):
        message = "%s:  %s  lvl: %s" %(name_list[i],score_list[i],level_list[i])
        draw_message((330, 163+(51*i)), 30, message) 
    
def highscores(score, level):
    pygame.init()
    Rect = screen.get_rect()
    wintitle = pygame.display.set_caption("OmniTank High Scores")
    pygame.mouse.set_visible(True)

    name_list = []
    score_list = []
    level_list = []
    name = ''
    
    infile = open("highscores.txt", 'r')

    for line in infile:
        line = line.rstrip()
        info = line.split(':')
        name_list.append(info[0])
        score_list.append(int(info[1]))
        level_list.append(float(info[2]))
        
    box = (368, 695)
    selection = ''
    playsound = False
    no_score = False
    mus_pause = False

    # Image
    highscores_file_name = os.path.join('images', 'highscores.png')
    get_name = os.path.join('images', 'get_name.png')
    selectionbar_file_name = os.path.join("images","selection_outline.png")
    outline = pygame.image.load(selectionbar_file_name)

    # Create background
    background = pygame.image.load(highscores_file_name)
    background2 = pygame.image.load(get_name)
    pygame.display.flip()

    # Load sounds
    roll_over_sound = load_sound('menu_rollover.wav')
    click_sound = load_sound('menu_click.wav')

    all = pygame.sprite.RenderUpdates()

    MenuOutline.containers = all

    if score != None:
        if highscore(score, score_list):
            screen.blit(background2, (0,0))
            pygame.display.flip()
            name = gname(score, level)
            score_list, name_list, level_list = update_scores(score, level,
                                        name, score_list, level_list, name_list)
            rewrite_file(name_list, score_list, level_list)
        else:
            no_score = True

    screen.blit(background, (0,0))
    if no_score:
        draw_message((390,15), 50, 'No Highscore')
    display_scores(name_list, score_list, level_list)
    pygame.display.flip()

    while 1:
        time_passed = clock.tick(30)

        in_box = (pygame.mouse.get_pos()[0] <= 657 and
                  pygame.mouse.get_pos()[0] >= 368 and
                  pygame.mouse.get_pos()[1] <= 734 and
                  pygame.mouse.get_pos()[1] >= 695)

        # Sound
        if in_box and playsound:
            roll_over_sound.play()
            playsound = False
        if not in_box:
            playsound = True

        # User Input
        for event in pygame.event.get():
            if in_box:
                MenuOutline(box, outline, 657, 368, 734, 695)
                selection = 'menu'
            if event.type == MOUSEBUTTONDOWN:
                if selection == 'menu':
                    click_sound.play()
                    infile.close()
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
    highscores(None, 0)
