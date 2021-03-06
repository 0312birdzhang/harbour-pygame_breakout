#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
功能：使用pyGame实现一个简单的打砖块游戏 
Created on Nov 30, 2012 
@author: liury_lab 

@author: BirdZhang
'''

try:
    import pygame_sdl2 as pg
    pg.import_as_pygame()
except Exception as e:
    pass
import pygame, sys, time, random ,os    #@UnusedImport
from pygame.locals import *         #@UnusedWildImport  

def main():
    # 一些关于窗口的常量定义
    WINDOW_WIDTH  = 540
    WINDOW_HEIGHT = 960


    # 游戏状态常量定义
    GAME_STATE_INIT        = 0
    GAME_STATE_START_LEVEL = 1
    GAME_STATE_RUN         = 2
    GAME_STATE_GAMEOVER    = 3
    GAME_STATE_SHUTDOWN    = 4
    GAME_STATE_EXIT        = 5

    # 小球的常量定义
    BALL_START_Y  = (WINDOW_HEIGHT//2)
    BALL_SIZE     = 4

    # 挡板的常量定义
    PADDLE_START_X  = (WINDOW_WIDTH/2 - 16)
    PADDLE_START_Y  = (WINDOW_HEIGHT - 32);
    PADDLE_WIDTH    = 90
    PADDLE_HEIGHT   = 8

    # 砖块的常量定义
    NUM_BLOCK_ROWS    = 6
    NUM_BLOCK_COLUMNS = 8
    BLOCK_WIDTH       = 64
    BLOCK_HEIGHT      = 16
    BLOCK_ORIGIN_X    = 8
    BLOCK_ORIGIN_Y    = 8
    BLOCK_X_GAP       = 80
    BLOCK_Y_GAP       = 32

    # 一些颜色常量定义
    BACKGROUND_COLOR = (0, 0, 0)
    BALL_COLOR       = (0, 0, 255)
    PADDLE_COLOR     = (128, 64, 64)
    BLOCK_COLOR      = (255, 128, 0)
    TEXT_COLOR       = (255, 255, 255)

    # 游戏的一些属性信息
    TOTAL_LIFE       = 5
    FPS              = 25
    keep_going       = True
    # 初始化砖块数组
    def InitBlocks():
        #blocks = [[1] * NUM_BLOCK_COLUMNS] * NUM_BLOCK_ROWS
        blocks = []
        for i in range(NUM_BLOCK_ROWS):             #@UnusedVarialbe
            blocks.append([i+1] * NUM_BLOCK_COLUMNS)
        return blocks

    # 检测小球是否与挡板或者砖块碰撞
    def ProcessBall(blocks, ball_x, ball_y, paddle):
        if (ball_y > WINDOW_HEIGHT//2):
            if (ball_x+BALL_SIZE >= paddle['rect'].left and
                ball_x-BALL_SIZE <= paddle['rect'].left+PADDLE_WIDTH and
                ball_y+BALL_SIZE >= paddle['rect'].top and
                ball_y-BALL_SIZE <= paddle['rect'].top+PADDLE_HEIGHT):
                return None

    # 显示文字
    def DrawText(text, font, surface, x, y):
        text_obj = font.render(text, 1, TEXT_COLOR)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_obj, text_rect)

    # 退出游戏
    def Terminate():
        os.system("/bin/sh /usr/share/harbour-pygame_breakout/stop.sh")
        sys.exit()

    # 等待用户输入
    def WaitForPlayerToPressKey():
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return
                if event.type == QUIT:
                    Terminate()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        Terminate()
                    return
                if event.type == pygame.FINGERMOTION:
                    return



    mainClock = pygame.time.Clock()

    # 小球的位置和速度
    ball_x  = 0
    ball_y  = 0
    ball_dx = 0
    ball_dy = 0

    # 挡板的运动控制
    paddle_move_left  = False
    paddle_move_right = False

    # 挡板的位置和颜色
    paddle  = {'rect' :pygame.Rect(0, 0, PADDLE_WIDTH, PADDLE_HEIGHT),
               'color': PADDLE_COLOR}

    # 游戏状态
    game_state  = GAME_STATE_INIT
    blocks      = []
    life_left   = TOTAL_LIFE
    game_over   = False
    blocks_hit  = 0
    score       = 0
    level       = 1

    game_start_font = pygame.font.SysFont(None, 40)
    game_over_font  = pygame.font.SysFont(None, 40)
    text_font       = pygame.font.SysFont(None, 20)

    # game_over_sound = pygame.mixer.Sound('background.wav')
    # game_hit_sound = pygame.mixer.Sound('background.wav')
    #pygame.mixer.music.load('background.wav')
    windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), FULLSCREEN)
    #WINDOW_WIDTH, WINDOW_HEIGHT = windowSurface.get_size()

    pygame.display.set_caption('打砖块')


    DrawText('pyBreakOut', game_start_font, windowSurface,
             (WINDOW_WIDTH/4), (WINDOW_HEIGHT/4 + 50))
    DrawText('Press any key to start.', game_start_font, windowSurface,
             (WINDOW_WIDTH/4)-60, (WINDOW_HEIGHT)/4+100)
    pygame.display.update()
    WaitForPlayerToPressKey()


    # 播放背景音乐
    #pygame.mixer.music.play(-1, 0.0)

    # 游戏主循环
    while keep_going:
        # 事件监听
        for event in pygame.event.get():
            if event.type == QUIT:
                keep_going = False
                Terminate()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    paddle_move_left = True
                if event.key == K_RIGHT:
                    paddle_move_right = True
                if event.key == K_ESCAPE:
                    keep_going = False
                    Terminate()
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    paddle_move_left = False
                if event.key == K_RIGHT:
                    paddle_move_right = False

            if event.type == FINGERMOTION:
                if event.dx > 0:
                    paddle_move_right = True
                elif event.dx < 0:
                    paddle_move_left = True
            if event.type == FINGERUP:
                paddle_move_left  = False
                paddle_move_right = False
        # 游戏控制流程
        if game_state == GAME_STATE_INIT:
            # 初始化游戏
            ball_x  = random.randint(8, WINDOW_WIDTH-8)
            ball_y  = BALL_START_Y
            ball_dx = random.randint(-3, 4)
            ball_dy = random.randint( 5, 8)

            paddle['rect'].left = PADDLE_START_X
            paddle['rect'].top  = PADDLE_START_Y

            paddle_move_left  = False
            paddle_move_right = False

            life_left   = TOTAL_LIFE
            game_over   = False
            blocks_hit  = 0
            score       = 0
            level       = 1
            game_state  = GAME_STATE_START_LEVEL
        elif game_state == GAME_STATE_START_LEVEL:
            # 新的一关
            blocks = InitBlocks()
            game_state = GAME_STATE_RUN
        elif game_state == GAME_STATE_RUN:
            # 游戏运行

            # 球的运动
            ball_x += ball_dx;
            ball_y += ball_dy;

            if ball_x > (WINDOW_WIDTH-BALL_SIZE) or ball_x < BALL_SIZE:
                ball_dx = -ball_dx
                ball_x  += ball_dx;
            elif ball_y < BALL_SIZE:
                ball_dy = -ball_dy
                ball_y  += ball_dy
            elif ball_y > WINDOW_HEIGHT-BALL_SIZE:
                if life_left == 0:
                    game_state = GAME_STATE_GAMEOVER
                else:
                    life_left -= 1
                    # 初始化游戏
                    ball_x  = paddle['rect'].left + PADDLE_WIDTH // 2
                    ball_y  = BALL_START_Y
                    ball_dx = random.randint(-4, 5)
                    ball_dy = random.randint( 6, 9)

            # 检测球是否与挡板碰撞
            if ball_y > WINDOW_HEIGHT // 2:
                if (ball_x+BALL_SIZE >= paddle['rect'].left and
                    ball_x-BALL_SIZE <= paddle['rect'].left+PADDLE_WIDTH and
                    ball_y+BALL_SIZE >= paddle['rect'].top and
                    ball_y-BALL_SIZE <= paddle['rect'].top+PADDLE_HEIGHT):
                    ball_dy = - ball_dy
                    ball_y += ball_dy
                    #game_hit_sound.play()
                    if paddle_move_left:
                        ball_dx -= random.randint(0, 3)
                    elif paddle_move_right:
                        ball_dx += random.randint(0, 3)
                    else:
                        ball_dx += random.randint(-1, 2)

            # 检测球是否与砖块碰撞
            cur_x = BLOCK_ORIGIN_X
            cur_y = BLOCK_ORIGIN_Y
            for row in range(NUM_BLOCK_ROWS):
                cur_x = BLOCK_ORIGIN_X
                for col in range(NUM_BLOCK_COLUMNS):
                    if blocks[row][col] != 0:
                        if (ball_x+BALL_SIZE >= cur_x and
                            ball_x-BALL_SIZE <= cur_x+BLOCK_WIDTH and
                            ball_y+BALL_SIZE >= cur_y and
                            ball_y-BALL_SIZE <= cur_y+BLOCK_HEIGHT):
                            blocks[row][col] = 0
                            blocks_hit += 1
                            ball_dy = -ball_dy
                            ball_dx += random.randint(-1, 2)
                            score += 5 * (level + abs(ball_dx))
                            #game_hit_sound.play()
                    cur_x += BLOCK_X_GAP
                cur_y += BLOCK_Y_GAP

            if blocks_hit == NUM_BLOCK_ROWS * NUM_BLOCK_COLUMNS:
                level       += 1
                blocks_hit  = 0
                score       += 1000
                game_state  = GAME_STATE_START_LEVEL

            # 挡板的运动
            if paddle_move_left:
                paddle['rect'].left -= 8
                if paddle['rect'].left < 0:
                    paddle['rect'].left = 0
            if paddle_move_right:
                paddle['rect'].left += 8
                if paddle['rect'].left > WINDOW_WIDTH-PADDLE_WIDTH:
                    paddle['rect'].left = WINDOW_WIDTH-PADDLE_WIDTH

            # 绘制过程
            windowSurface.fill(BACKGROUND_COLOR)
            # 绘制挡板
            pygame.draw.rect(windowSurface, paddle['color'], paddle['rect'])
            # 绘制小球
            pygame.draw.circle(windowSurface, BALL_COLOR, (ball_x, ball_y),
                               BALL_SIZE, 0)
            # 绘制砖块
            cur_x = BLOCK_ORIGIN_X
            cur_y = BLOCK_ORIGIN_Y
            for row in range(NUM_BLOCK_ROWS):
                cur_x = BLOCK_ORIGIN_X
                for col in range(NUM_BLOCK_COLUMNS):
                    if blocks[row][col] != 0:
                        pygame.draw.rect(windowSurface, BLOCK_COLOR,
                                         (cur_x, cur_y, BLOCK_WIDTH, BLOCK_HEIGHT))
                    cur_x += BLOCK_X_GAP
                cur_y += BLOCK_Y_GAP

            # 绘制文字描述信息
            message = 'Level: ' + str(level) + '    Life: ' + str(life_left) + '    Score: ' + str(score)
            DrawText(message, text_font, windowSurface, 8, (WINDOW_HEIGHT - 16))
        elif game_state == GAME_STATE_GAMEOVER:
            DrawText('GAME OVER', game_over_font, windowSurface,
                     (WINDOW_WIDTH / 3), (WINDOW_HEIGHT / 3))
            DrawText('Level: ' + str(level), game_over_font, windowSurface,
                     (WINDOW_WIDTH / 3)+20, (WINDOW_HEIGHT / 3) + 50)
            DrawText('Score: ' + str(score), game_over_font, windowSurface,
                     (WINDOW_WIDTH / 3)+20, (WINDOW_HEIGHT / 3) + 100)
            DrawText('Press any key to play again.', game_over_font, windowSurface,
                     (WINDOW_WIDTH / 3)-80, (WINDOW_HEIGHT / 3) + 150)
            pygame.display.update()

            pygame.mixer.music.stop()
            #game_over_sound.play()

            WaitForPlayerToPressKey()
            game_state = GAME_STATE_INIT
        elif game_state == GAME_STATE_SHUTDOWN:
            game_state = GAME_STATE_EXIT

        pygame.display.update()
        mainClock.tick(FPS + level*2)
    
if __name__ == "__main__":
    # 游戏界面的初始化
    pygame.init()
    main()
    pygame.quit()
