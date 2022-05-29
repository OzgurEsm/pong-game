import pygame

pygame.init()

# Don't forget; adding or subbing is movement as well

WIDTH , HEIGHT = 700 ,500 #All capital variable is constant!!!
MY_WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Ping-Pong')

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

SCORE_FONT = pygame.font.SysFont('comicsans', 50)

WINNING_SCORE = 10

sound_ball = pygame.mixer.Sound('racquet.wav')
sound_ball2 = pygame.mixer.Sound('rubber-ball.wav')
sound_cheer = pygame.mixer.Sound('crowd.wav')
sound_clap = pygame.mixer.Sound('moreclaps.wav')
sound_ball.set_volume(0.5)
sound_ball2.set_volume(0.5)

class Paddle:
    COLOR = WHITE
    VELOCITY = 4
    
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x # to reset position after scoring
        self.y = self.original_y = y
        self.width = width
        self.height = height
        
    def draw_paddle(self,win):
        pygame.draw.rect(
            win, self.COLOR, (self.x, self.y, self.width, self.height))
        
    def move_paddle(self, up=True):
        if up:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY
    
    def reset_paddle(self):
        self.x = self.original_x
        self.y = self.original_y        

class Ball:
    MAX_VEL = 5
    COLOR = WHITE
    
    def __init__(self, x, y, radius):
        self.x = self.original_x = x # setting original coz we need to reset the ball position after scoring
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw_ball(self,win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move_ball(self):
        self.x += self.x_vel
        self.y += self.y_vel
    
    def reset_ball(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1
        
def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)
    
    left_score_text = SCORE_FONT.render(f'{left_score}', True, WHITE)
    right_score_text = SCORE_FONT.render(f'{right_score}', True, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))
    
    for paddle in paddles:
        paddle.draw_paddle(win)
    
    for i in range(10, HEIGHT, HEIGHT//20): 
        if i % 2 == 1:
            continue # pass odd numbers so we get dashed line
        pygame.draw.rect(MY_WIN, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))
        # x = WIDTH//2 - rectangle's width/2
        # y = i 
        # rectangle's width = 10
        # rectangle's height HEIGHT//20 
        # it's drawing 10,25 white rectangle and 10,25 black rectangle if we'd code 1 by 1
    
    ball.draw_ball(MY_WIN)
        
    pygame.display.update()

def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT: # hitting bottom
        ball.y_vel *= -1 
    elif ball.y - ball.radius <= 0: # hitting ceiling
        ball.y_vel *= -1
    
    if ball.x_vel < 0: # direction of the ball
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height: # in heigt of paddle
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width: # if touching the surcafe of paddle
                ball.x_vel *= -1 # reversed the speed so it goes the other way
                sound_ball.play()
                
                paddle_middle_y = left_paddle.y + PADDLE_HEIGHT / 2 
                difference_in_y = ball.y - paddle_middle_y
                reduction_factor = (PADDLE_HEIGHT/2) / ball.MAX_VEL # colliding further away from mid point of the paddle the faster the ball gets by this factor
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = y_vel

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1
                sound_ball2.play()                  

                paddle_middle_y = right_paddle.y + PADDLE_HEIGHT / 2
                difference_in_y = ball.y - paddle_middle_y 
                reduction_factor = (PADDLE_HEIGHT/2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = y_vel
        
def handle_paddle_movement(keys, left_paddle, right_paddle, ball): # added ball for Ai conditions
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VELOCITY >= 0:
        left_paddle.move_paddle(up=True)
    if keys[pygame.K_s] and (left_paddle.y + left_paddle.height) - left_paddle.VELOCITY <= HEIGHT:
        left_paddle.move_paddle(up=False)
        
    # disabled for Ai    
    #if keys[pygame.K_UP] and right_paddle.y - right_paddle.VELOCITY >= 0: 
        #right_paddle.move_paddle(up=True)
    #if keys[pygame.K_DOWN] and (right_paddle.y + right_paddle.height) - right_paddle.VELOCITY <= HEIGHT:
        #right_paddle.move_paddle(up=False)
        # after 'and' we restrict the movement of paddles so they stay on screen
    
    # added Ai instead of a 2. player, already better than me.Need to add difficulty levels,after the cl final tho!            
    if ball.x_vel > 0 and ball.x > WIDTH//2: # Ai paddle movement conditions , ball moving towards right_paddle
        if ball.y - ball.radius < right_paddle.y : #and right_paddle.y - right_paddle.VELOCITY >= 0
            right_paddle.move_paddle(up=True)
        elif ball.y + ball.radius > right_paddle.y+ right_paddle.height: #and (right_paddle.y + right_paddle.height) - right_paddle.VELOCITY <= HEIGHT
            right_paddle.move_paddle(up=False)
    if ball.x_vel < 0: # paddle moves to starting pos. after hitting the ball
        if right_paddle.y > right_paddle.original_y:
            right_paddle.move_paddle(up=True)
        if right_paddle.y < right_paddle.original_y:
            right_paddle.move_paddle(up=False)
    
def play():
    run = True
    clock = pygame.time.Clock() # to run the game with same fps on every comp ;top-fps limit
    
    left_paddle = Paddle(
        10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT) # doing '//' to avoid floats
    right_paddle = Paddle(
        WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT) 
    ball = Ball(
        WIDTH//2,HEIGHT//2,BALL_RADIUS)
    
    left_score ,right_score = 0, 0
    
    
    while run:
        clock.tick(FPS)
        draw(MY_WIN, [left_paddle, right_paddle], ball, left_score, right_score) # paddles in list so we used for loop in draw(win)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run  = False
                break
        
        keys = pygame.key.get_pressed() # gives us a list so we dont have to make one   
        handle_paddle_movement(keys, left_paddle, right_paddle, ball) # added ball for Ai conditions
        ball.move_ball()    
        handle_collision(ball, left_paddle, right_paddle)
        
        score_up = False # trying to tidy up resets
        if ball.x < 0 : 
            right_score += 1
            score_up = True
        elif ball.x > WIDTH:
            left_score += 1
            score_up = True
        if score_up:
            sound_clap.play()
            ball.reset_ball()
            left_paddle.reset_paddle()
            right_paddle.reset_paddle()
        
        won = False # to tidy up again
        if left_score >= 10:
            won = True
            win_text = 'Left Player Won!'
        elif right_score >= 10:
            won = True
            win_text = 'Right Player Won!'
        if won:
            sound_cheer.play()
            won_text = SCORE_FONT.render(win_text, True, WHITE)
            MY_WIN.blit(won_text, (WIDTH//2 - won_text.get_width() //2, HEIGHT//2 - won_text.get_height() //2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset_ball()
            right_paddle.reset_paddle()
            left_paddle.reset_paddle()     
            left_score = 0
            right_score = 0
    return main()
    
def main():
    pygame.display.set_caption('Menu')
    
    while True:
        MY_WIN.fill(BLACK)
        menu_text = SCORE_FONT.render('WELCOME', True, WHITE)
        menu_rect = menu_text.get_rect(center=(WIDTH//2, HEIGHT*0.2))
        MY_WIN.blit(menu_text, menu_rect)
        
        # want to implement both PvP and PvE,have to split the 1 single file system i guess
        
        #single_font = pygame.font.Font(None, 30)
        #single_text = single_font.render('For Single Player: Press 1', True, WHITE)
        #single_rect = single_text.get_rect(center=(WIDTH//2, HEIGHT*0.4))
        #MY_WIN.blit(single_text, single_rect)
        #
        #multi_font = pygame.font.Font(None, 30)
        #multi_text = multi_font.render('For Multiplayer: Press 2', True, WHITE)
        #multi_rect = multi_text.get_rect(center=(WIDTH//2,HEIGHT*0.45))
        #MY_WIN.blit(multi_text, multi_rect)
        
        guide_font = pygame.font.Font(None, 30)
        guide_text1 = guide_font.render('Player 1: Use "w" and "s" to move', True, WHITE)
        guide_text2 = guide_font.render('Player 2: Use arrow keys to move', True, WHITE)
        guide_text1_rect = guide_text1.get_rect(center=(WIDTH//4, HEIGHT*0.6))
        guide_text2_rect = guide_text2.get_rect(center=(WIDTH*(3/4), HEIGHT*0.6))
        MY_WIN.blit(guide_text1, guide_text1_rect)
        MY_WIN.blit(guide_text2, guide_text2_rect)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                quit()
            if keys[pygame.K_RETURN]:
                play()
                

if __name__ == '__main__':
    main()