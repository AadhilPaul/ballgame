import pygame
import sys

pygame.init()


width, height = 1000, 700
window = pygame.display.set_mode((width, height))
caption = "i dont know the name"
pygame.display.set_caption(caption)

gap = 15
# colors
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
yellow = (255, 255, 0)
purple = (128, 0, 128)
orange = (255, 165, 0)
grey = (128, 128, 128)
turquoise = (64, 224, 208)

# score and fonts
SCORE_FONT = pygame.font.SysFont("comicsans", 27)
WIN_FONT = pygame.font.SysFont("comicsans", 60)
LIVES_FONT = pygame.font.SysFont("comicsans", 27)
score = 0

# game borders
left_border = ((gap, gap), (gap, height - gap))
right_border = ((width - gap, gap), (width - gap, height - gap))
bottom_border = ((gap, height - gap), (width - gap, height - gap))
top_border = ((gap, gap), (width - gap, gap))
border_list = [right_border, left_border, bottom_border, top_border]

draw_death_line = lambda win: pygame.draw.line(
    win,
    red,
    (bottom_border[0][0], bottom_border[0][1] - 20),
    (bottom_border[1][0], bottom_border[1][1] - 20),
    1,
)

lives = 3

# draw a platform
platform_width, platform_height = 120, 3
platform_velocity = 5
platform_pos_x = width / 2 - (platform_width / 2)
platform_pos_y = height - 50 - platform_height
draw_platform = lambda win: pygame.draw.rect(
    win, white, (platform_pos_x, platform_pos_y, platform_width, platform_height)
)
# draw ball
ball_width, ball_height = 30, 30
ball_velocity = [5, 5]
ball_pos_x, ball_pos_y = width / 2 - ball_width, height / 2 - ball_height
draw_ball = lambda win: pygame.draw.rect(
    win, white, (ball_pos_x, ball_pos_y, ball_width, ball_height)
)


def display_score_and_lives(win):
    # display scores
    score1_text = SCORE_FONT.render(f"Score: {str(score)}", 1, white)
    lives_text = LIVES_FONT.render(f"Lives: {str(lives)}", 1, white)
    win.blit(score1_text, (left_border[0][0] + 20, left_border[0][1] + 20))
    win.blit(lives_text, (right_border[0][0] - 90, top_border[0][1] + 20))


def draw_border(border_list, win):
    for i, e in enumerate(border_list):
        pygame.draw.line(win, white, e[0], e[1], 3)


def display_winner(win):
    win.fill(black)
    score_win_text = SCORE_FONT.render(f"Score: {str(score)}", 1, white)
    win.blit(score_win_text, (width / 2, height / 2))
    pygame.display.update()
    pygame.time.delay(2500)


def draw_game_window(win):
    win.fill(black)
    display_score_and_lives(win)
    draw_border(border_list, win)
    draw_death_line(win)
    draw_platform(win)
    draw_ball(win)
    pygame.display.update()


def game_main(win):
    global platform_pos_x, ball_pos_x, ball_pos_y, score, lives
    run = True
    clock = pygame.time.Clock()
    frames_per_second = 60

    while run:
        clock.tick(frames_per_second)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display_winner(win)
                run = False
                sys.exit()

        keys = pygame.key.get_pressed()
        if lives == 0:
            display_winner(win)
            run = False
            sys.exit()

        if keys[pygame.K_a] and platform_pos_x > left_border[0][0] + gap:
            platform_pos_x -= platform_velocity

        if (
            keys[pygame.K_d]
            and platform_pos_x < right_border[0][0] - platform_width - gap
        ):
            platform_pos_x += platform_velocity

        ball_pos_x += ball_velocity[0]
        ball_pos_y += ball_velocity[1]
        # if ball_pos_y + ball_height >= bottom_border[0][1] - 3:
        # ball_velocity[1] *= -1

        if ball_pos_x + ball_width >= right_border[0][0] - 3:
            ball_velocity[0] *= -1

        if ball_pos_y <= top_border[0][1] + 3:
            ball_velocity[1] *= -1

        if ball_pos_x <= left_border[0][0] + 3:
            ball_velocity[0] *= -1

        if (
            ball_pos_x >= platform_pos_x
            and ball_pos_y >= platform_pos_y - 20
            and ball_pos_y <= platform_pos_y + 20
            and ball_pos_x < platform_pos_x + platform_width
        ) or (
            ball_pos_x + ball_width >= platform_pos_x
            and ball_pos_y >= platform_pos_y - 20
            and ball_pos_y <= platform_pos_y + 20
            and ball_pos_x + width < platform_pos_x + width
        ):
            ball_velocity[1] *= -1
            score += 1
        if ball_pos_y + ball_height > bottom_border[0][1] - 20:
            ball_pos_x, ball_pos_y = width / 2 - ball_width, height / 2 - ball_height
            lives -= 1
            pygame.time.delay(1000)

        draw_game_window(win)


game_main(window)
pygame.quit()
