#15-3-2010

import pygame, sys, os , os.path
from random import randint
from pygame.locals import *

screen = pygame.display.set_mode((1024, 768))
wintitle = pygame.display.set_caption("OmniTank Game Report")
clock = pygame.time.Clock()

def draw_message(position, size, message, color):
    """
        position format --> (x,y)
        size format --> just a number
        message format --> "message"
    """
    
    font = pygame.font.SysFont('arial', size)
    Message = font.render(message, True, color)
    screen.blit(Message, position)

def disp_results(shots_fired, shots_hit, level_score, jdbr):
    rand = randint(1,8)
    dark_blue    = (89,141,178)
    green        = (0,255,33)
    if shots_fired == 0:
        accuracy = 0
    else:
        accuracy     = (float(shots_hit)/shots_fired)*100
    bonus_points = (accuracy*.04*level_score)

    draw_message((520,322), 15, "%d" %shots_fired, dark_blue)
    draw_message((520,337), 15, "%d" %shots_hit, dark_blue)
    draw_message((520,352), 15, "%.2f %s" %(accuracy, '%'), dark_blue)
    draw_message((520,367), 15, "%d" %bonus_points, green)
    draw_message((520,382), 15, "%d" %(bonus_points+level_score), dark_blue)
    if (accuracy >= 65 and not jdbr) or (accuracy >= 85 and jdbr):
        draw_message((600,352), 15, "Bonus", green)
        draw_message((600,367), 15, " Lives", green)
        draw_message((600,382), 15, "Added!", green)

    #draw tip
    if rand == 1:
        draw_message((400,455), 20, "You can destroy mines by shooting", dark_blue)
        draw_message((400, 480), 20, "them.", dark_blue)
    elif rand == 2:
        draw_message((400, 455), 20, "In a normal level the accuracy required", dark_blue)
        draw_message((400, 480), 20, "for extra lives is only 65%. Just be", dark_blue)
        draw_message((400, 505), 20, "sure to pick your shots against the", dark_blue)
        draw_message((400, 530), 20, "boss.", dark_blue)
    elif rand == 3:
        draw_message((400, 455), 20, "Use the 'wrap-around' walls to escape", dark_blue)
        draw_message((400, 480), 20, "from bullets and get behind the", dark_blue)
        draw_message((400, 505), 20, "enemeis.", dark_blue)
    elif rand == 4:
        draw_message((400, 455), 20, "You move faster diagonally.", dark_blue)
    elif rand == 5:
        draw_message((400, 455), 20, "Set your priorities. You may be better", dark_blue)
        draw_message((400, 480), 20, "off taking care of certain enemies first.", dark_blue)
    elif rand == 6:
        draw_message((400, 455), 20, "Enemies are predictable.", dark_blue)
    elif rand == 7:
        draw_message((400, 455), 20, "you might be better of with accuracy", dark_blue)
        draw_message((400, 480), 20, "as your main goal during the bonus", dark_blue)
        draw_message((400, 505), 20, "round and normal levels. It gives large", dark_blue)
        draw_message((400, 530), 20, "bonus points and potentially lives.", dark_blue)
    elif rand == 8:
        draw_message((400, 455), 20, "Keep moving! Staying still will mean", dark_blue)
        draw_message((400, 480), 20, "certain death.", dark_blue)
        
    return bonus_points, accuracy
    
    
def report(shots_fired, shots_hit, level_score, jdbr):
    pygame.init()
    Rect = screen.get_rect()

    mus_pause = False
    
    # Image
    report_file_name = os.path.join('images', 'end_level_results.png')

    # Create background
    background = pygame.image.load(report_file_name)
    screen.blit(background, (0,0))

    bonus_points, accuracy = disp_results(shots_fired, shots_hit,
                                          level_score, jdbr)
    pygame.display.flip()

    while 1:
        time_passed = clock.tick(30)

        # User Input
        for event in pygame.event.get():
            if not hasattr(event, 'key'):
                continue
            down = event.type == KEYDOWN
            if event.key == K_r and down:
                return bonus_points, accuracy
            if event.key == K_m and down:
                if mus_pause:
                    mus_pause = False
                    pygame.mixer.music.unpause()
                else:
                    mus_pause = True
                    pygame.mixer.music.pause()

if __name__ == '__main__':
    report(1,1,1)
