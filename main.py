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

class Paddle:
    COLOR = WHITE
    VELOCITY = 4
    
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x # to reset position after scoring
        self.y = self.original_y = y
        self.width = width
        self.height = height
        
    def draw_pad(self,win):
        pygame.draw.rect(
            win, self.COLOR, (self.x, self.y, self.width, self.height))
        
    def move_pad(self, up=True):
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
        paddle.draw_pad(win)
    
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
    elif ball.y - ball.radius <= 0: #hitting ceiling
        ball.y_vel *= -1
    
    if ball.x_vel < 0: # direction of the ball
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height: # in heigt of paddle
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width: # if touching the surcafe of paddle
                ball.x_vel *= -1 # reversed the speed so it goes the other way
                
                paddle_middle_y = left_paddle.y + PADDLE_HEIGHT / 2 
                difference_in_y = ball.y - paddle_middle_y
                reduction_factor = (PADDLE_HEIGHT/2) / ball.MAX_VEL # further away from mid point the faster ball gets by this factor
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = y_vel

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1                    

                paddle_middle_y = right_paddle.y + PADDLE_HEIGHT / 2
                difference_in_y = ball.y - paddle_middle_y 
                reduction_factor = (PADDLE_HEIGHT/2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = y_vel
        
def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VELOCITY >= 0:
        left_paddle.move_pad(up=True)
    if keys[pygame.K_s] and (left_paddle.y + left_paddle.height) - left_paddle.VELOCITY <= HEIGHT:
        left_paddle.move_pad(up=False)
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VELOCITY >= 0:
        right_paddle.move_pad(up=True)
    if keys[pygame.K_DOWN] and (right_paddle.y + right_paddle.height) - right_paddle.VELOCITY <= HEIGHT:
        right_paddle.move_pad(up=False)
    # after 'and' we restrict the movement of paddles so they stay on screen
    
def main():
    run = True
    clock = pygame.time.Clock() #to run the game with same fps on every comp ;top-fps limit
    
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
        
        keys = pygame.key.get_pressed() #gives us a list so we dont have to make one   
        handle_paddle_movement(keys, left_paddle, right_paddle)
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
            won_text = SCORE_FONT.render(win_text, True, WHITE)
            MY_WIN.blit(won_text, (WIDTH//2 - won_text.get_width() //2, HEIGHT//2 - won_text.get_height() //2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset_ball()
            right_paddle.reset_paddle()
            left_paddle.reset_paddle()     
            left_score = 0
            right_score = 0
    pygame.quit()
    

if __name__ == '__main__':
    main()