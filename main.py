import pygame
from pygame.locals import *
from pygame import mixer

pygame.init()

clock =pygame.time.Clock()
fps = 70

bg= (0,0,0)
font = pygame.font.SysFont('Constantia',30)

mixer.music.load('[MP3DOWNLOAD.TO] Darth Maul Theme Song (Duel of The Fates) by John Williams-192k.mp3')
mixer.music.play(-1)
mixer.music.pause()
window_width= 800
window_height= 500
window = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption('Pong')
num_of_middlebar= window_height//19
bar_color= (255,255,255)
text_color = (255,255,255)
score_p1= 0
score_p2=0
game_over= False
game_status= False

class Bar():
    def __init__(self,x):
        self.height=75
        self.width= 15
        self.x= x
        self.y= int(window_height/2-self.height/2)
        self.speed= 6
        self.rect = Rect(self.x, self.y, self.width, self.height)

    def move1(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if key[pygame.K_DOWN] and self.rect.bottom < window_height:
            self.rect.y += self.speed
    def move2(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if key[pygame.K_s] and self.rect.bottom < window_height:
            self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(window,bar_color,self.rect)


class MiddleBars():
    def __init__(self):
        self.width=9
        self.height= 9
        self.x= int(window_width/2-9)

    def draw(self):
        self.middlebar= []
        initialy = 10
        for i in range(num_of_middlebar):
            self.middlebar.append(Rect(self.x,initialy,self.width,self.height))
            initialy += 19
            pygame.draw.rect(window,bar_color,self.middlebar[i])

class Ball():
    def __init__(self,x,y):
        self.ball_rad= 7
        self.x = x - self.ball_rad
        self.y = y
        self.rect = Rect(self.x,self.y,self.ball_rad, self.ball_rad)
        self.speed_x=1
        self.speed_y=1
        self.acc= 0.02

    def draw(self):
        pygame.draw.circle(window,bar_color,(self.rect.x+self.ball_rad,self.rect.y + self.ball_rad),self.ball_rad)

    def move(self):
        global score_p1
        global score_p2
        self.rect.x += self.speed_x
        self.rect.y +=self.speed_y
        collision_tresh= 10
        if self.speed_x < 6 and self.speed_x>0:
            self.speed_x += self.acc
        if self.speed_y < 6 and self.speed_y>0:
            self.speed_y += self.acc
        if self.speed_x > -6 and self.speed_x < 0:
            self.speed_x -= self.acc
        if self.speed_y > -6 and self.speed_y < 0:
            self.speed_y -= self.acc
        if self.rect.right > window_width:
            score_p1 +=1
            self.speed_x=1
            self.speed_y=1
            self.rect.x= self.x
            self.rect.y= self.y
        if self.rect.left <0:
            score_p2 +=1
            self.speed_x=-1
            self.speed_y= 1
            self.rect.x = self.x
            self.rect.y = self.y
        if self.rect.top < 0 or self.rect.bottom > window_height:
            self.speed_y *= -1
        if self.rect.colliderect(player1):
            if abs(self.rect.right- player1.rect.left) < collision_tresh and self.speed_x > 0:
                self.speed_x *= -1
                if self.rect.centery-player1.rect.centery < 0:
                    self.speed_y *=-1
        if self.rect.colliderect(player2):
            if abs(self.rect.left - player2.rect.right) < collision_tresh and self.speed_x < 0:
                self.speed_x *= -1
                if self.rect.centery-player2.rect.centery<0:
                    self.speed_y *=-1
    def stop(self):
        self.speed_y =0
        self.speed_x = 0

def drawtext(text, font, text_color,x,y):
    img=font.render(text,True, text_color)
    window.blit(img,(x,y))

player1= Bar(750)
player2= Bar(50)
middlebars= MiddleBars()
ball= Ball(window_width/2, 50)

run = True
while run:

    clock.tick(fps)

    window.fill(bg)

    player1.draw()
    player2.draw()
    ball.draw()

    if game_status == False and game_over== False:
        drawtext("CLICK ANYWHERE TO START", font,text_color,200,window_height/2-50)

    if game_status:
        mixer.music.unpause()
        middlebars.draw()
        player1.move1()
        player2.move2()
        ball.move()
        drawtext(str(score_p1),font,text_color,window_width/4-5,30)
        drawtext(str(score_p2),font,text_color,window_width-window_width/4+5,30)

    if score_p1 == 5:
        game_status == False
        drawtext("PLAYER 1 WINS",font,(70,218,53),90,80)
        ball.stop()
        mixer.music.fadeout(3000)

    if score_p2 == 5:
        game_status == False
        drawtext("PLAYER 2 WINS", font, (70, 218, 53), 485, 80)
        ball.stop()
        mixer.music.fadeout(3000)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and game_status== False:
            game_status = True

    pygame.display.update()

pygame.quit()
