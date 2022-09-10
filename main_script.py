import os
import pygame
import random

pygame.init()


screen_length,screen_width = 500,900
name = "project game"
screen = pygame.display.set_mode((screen_width, screen_length))
bg = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space_bg.jpg')), (screen_width,screen_length))
pygame.display.set_caption(name)
FPS = 60
font = pygame.font.SysFont('comicsans', 30, True) 
player_img = pygame.image.load(os.path.join('Assets','battleship.png'))
score,vel,dmg =0,5,64
rand_size,max_ast,ast_col = 0,5,(255,0,255)
proj_vel,proj_height,proj_width,proj_col = 30,64,4,(255,0,0)


class Player:
    
    def __init__(self,x,y,width,height,hp):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hp = hp       
        self.vel = 5
        self.dmg = 64
        self.hitbox = pygame.Rect((self.x,self.y),(64,64))
    def draw(self,screen):
        screen.blit(player_img, (self.x,self.y))
        

def draw(player,projectiles,asteroids,font,score):
    screen.blit(bg,(0,0))
    text = font.render('Score: ' + str(score), 1, (200,150,25))
    screen.blit(text, (750,10))
    player.draw(screen)
    for proj1 in projectiles:
        pygame.draw.rect(screen,proj_col,proj1)
    for asteroid in asteroids:
        pygame.draw.rect(screen,ast_col,asteroid)
    pygame.display.update()

def handle_collision(projectiles,asteroid,asteroids,score):
    for proj1 in projectiles:
        proj1.y -= proj_vel
        if proj1.y < 0: 
            projectiles.remove(proj1)
        elif pygame.Rect.colliderect(proj1,asteroid) and asteroid.y > -asteroid.h :
            projectiles.remove(proj1)
            asteroid.w -= dmg//2
            asteroid.h -= dmg//2
            asteroid = pygame.Rect((asteroid.x, asteroid.y),(asteroid.w,asteroid.h))
            if asteroid.w < 32:
                asteroids.remove(asteroid)
    
def handle_asteroids(player,asteroids,projectiles):
    while len(asteroids) < max_ast:
        rand_x = random.randrange(64,screen_width-64)
        ast_size = random.randrange(32,192)
        ast_hp = ast_size * 2
        asteroid = pygame.Rect((rand_x, -rand_x-rand_size),(ast_size,ast_size))
        asteroids.append(asteroid)
    for asteroid in asteroids:
        ast_vel = random.randrange(1,12)
        asteroid.y += ast_vel
        if asteroid.y > screen_length + 100:
            asteroids.remove(asteroid)
        if pygame.Rect.colliderect(player.hitbox,asteroid):
            asteroids.remove(asteroid)
            print('ship destroyed')
        else:
            handle_collision(projectiles,asteroid,asteroids,score)


    
def player_movement(keys,player):
    if keys[pygame.K_a] and player.x - vel > 0: ##left
        player.x -= vel
        player.hitbox.x -= vel
    if keys[pygame.K_d] and player.x + vel + 64 < screen_width: ##right
        player.x += vel
        player.hitbox.x += vel
    if keys[pygame.K_w] and player.y - vel > 0: ##up
        player.y -= vel
        player.hitbox.y -= vel
    if keys[pygame.K_s] and player.y + vel + 64 < screen_length: ##down
        player.y += vel
        player.hitbox.y += vel
        

def main():
    player = Player(screen_width//2 - 32,screen_length-72,64,64,100)
    projectiles = []
    asteroids = []
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:                   
                if event.key == pygame.K_SPACE:
                        proj1 = pygame.Rect((player.x,player.y-32),(proj_width,proj_height))
                        projectiles.append(proj1)
                        proj2 = pygame.Rect((player.x + 64, player.y-32),(proj_width,proj_height))
                        projectiles.append(proj2)
            keys = pygame.key.get_pressed()
        draw(player,projectiles,asteroids,font,score)
        handle_asteroids(player,asteroids,projectiles)
        player_movement(keys,player)
    pygame.quit()

if __name__ == "__main__":
    main()