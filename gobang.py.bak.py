import pygame
from pygame.locals import *
from sys import exit
import numpy as np

board_size = 19;
position_size = 25;
border_size = 20;

button_width = 120
button_height = 60
screen_width = 500
screen_height = 500
button_x = screen_width / 2 - button_width / 2
button_y = screen_height * 3 / 4 - button_height / 2


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
# start = None

def is_win(x, y, array):
    m = int(round((x - (position_size)) / position_size))
    n = int(round((y - (position_size)) / position_size))
    count = 0
    # 垂直 (0, 0), (1, 0), (2, 0), (3, 0), (4, 0)
    # 平行 (0, 0), (0, 1), (0, 2), (0, 3), (0, 4)
    # 正斜 (0, 0), (1, 1), (2, 2), (3, 3), (4, 4)
    # 垂直 (0, 4), (1, 3), (2, 2), (3, 1), (4, 0)

    # 垂直
    position = m - 1
    while(position >= 0):
        if(array[position][n]):
            count += 1
            position -= 1
        else:
            break        
    
    position = m + 1
    while(position < board_size):
        if(array[position][n]):
            count += 1
            position += 1
        else:
            break        

    if count >= 4:
        return True
    else:
        count = 0

    # 平行
    position = n - 1
    while(position >= 0):
        if(array[m][position]):
            count += 1
            position -= 1
        else:
            break        
    
    position = n + 1
    while(position < board_size):
        if(array[m][position]):
            count += 1
            position += 1
        else:
            break        

    if count >= 4:
        return True
    else:
        count = 0

    # 正斜
    position_m = m - 1
    position_n = n - 1
    while(position_m >= 0 and position_n >= 0):
        if(array[position_m][position_n]):
            count += 1
            position_m -= 1
            position_n -= 1
        else:
            break        
    
    position_m = m + 1
    position_n = n + 1
    while(position_m < board_size and position_n < board_size):
        if(array[position_m][position_n]):
            count += 1
            position_m += 1
            position_n += 1
        else:
            break        

    if count >= 4:
        return True
    else:
        count = 0

    # 反斜
    position_m = m - 1
    position_n = n + 1
    while(position_m >= 0 and position_n < board_size):
        if(array[position_m][position_n]):
            count += 1
            position_m -= 1
            position_n += 1
        else:
            break        
    
    position_m = m + 1
    position_n = n - 1
    while(position_m < board_size and position_n  >= 0):
        if(array[position_m][position_n]):
            count += 1
            position_m += 1
            position_n -= 1
        else:
            break        

    if count >= 4:
        return True
    else:
        count = 0

    return False

def winner_text(word, screen):
    font = pygame.font.SysFont("arial", 60);
    text = font.render(word, True, (142, 91, 67))
    text_rect = text.get_rect()
    text_rect.center = screen.get_rect().center
    screen.blit(text, text_rect)
    
    # draw restart button
    button_bg = 'button_bg.png'
    btn_bg = pygame.image.load(button_bg).convert_alpha()
    screen.blit(btn_bg, (button_x, button_y)) # draw the backgroud in (0, 0)

    # draw button text
    button_font = pygame.font.SysFont("arial", 30);
    button_text = button_font.render('Restart', True, (142, 91, 67))
    button_text_rect = button_text.get_rect()
    button_text_rect.center = (button_x + button_width / 2, button_y + button_height / 2)
    # print(button_x)
    # print(button_y)

    screen.blit(button_text, button_text_rect)

def restart(x, y):
    if button_x <= x <= button_x + button_width and button_y <= y <= button_y + button_height:
        main()

def main():
    backgroud_image = 'backgroud.jpg'
    white_image = 'white.png'
    black_image = 'black.png'

    background = pygame.image.load(backgroud_image).convert()
    white = pygame.image.load(white_image).convert_alpha()
    black = pygame.image.load(black_image).convert_alpha()

    screen.blit(background, (0,0)) # draw the backgroud in (0, 0)
    pygame.event.set_blocked([KEYUP, KEYDOWN, JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION])
    pygame.event.set_allowed([MOUSEBUTTONDOWN, MOUSEBUTTONUP])

    white_list = np.zeros((board_size, board_size))
    black_list = np.zeros((board_size, board_size))
    total_list = np.zeros((board_size, board_size))
    dot_list = [((i + 1) * position_size - position_size / 2, (j + 1) * position_size - position_size / 2) for i in range(board_size) for j in range(board_size)]

    change = True # True為黑子 False為白子
    start = True
    while True:
        for event in pygame.event.get():
            if(event.type == QUIT):
                exit()

            if(event.type == MOUSEBUTTONDOWN and start):
                x,y = pygame.mouse.get_pos()
                m = int(round((x - (position_size)) / position_size))
                n = int(round((y - (position_size)) / position_size))
                if border_size <= x <= (screen_width - border_size) and border_size <= y <= (screen_height - border_size) and total_list[m][n] == 0:
                    total_list[m][n] = 1
                    try:
                        if(change):
                            screen.blit(black, dot_list[board_size * m + n])
                            black_list[m][n] = 1
                            change = not change
                            if is_win(x, y, black_list):
                                winner_text('Winner is Brown!', screen)
                                start = False
                        else:
                            screen.blit(white, dot_list[board_size * m + n])
                            white_list[m][n] = 1
                            change = not change
                            if is_win(x, y, white_list):
                                winner_text('Winner is Cony!', screen)
                                start = False
                    except :
                        pass

            if(event.type == MOUSEBUTTONDOWN and start == False):
                x,y = pygame.mouse.get_pos()
                restart(x, y)

        pygame.display.update()

if __name__ == "__main__":
    main()