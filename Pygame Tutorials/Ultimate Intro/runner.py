import pygame
import sys
from random import randint, choice
from runner_class import Player, Obstacle

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf', 50)

GROUND_Y = 300

# Background
sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

# Characters
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

# Intro Screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2) # surface, angle, scale
player_stand_rect = player_stand.get_rect(center = (400,200))

title_surf = font.render('Pixel Runner', False, (111,196,169))
title_rect = title_surf.get_rect(center = (400,80))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# Music
music = pygame.mixer.Sound('audio/music.wav')

music.set_volume(0.1)
music.play(loops = -1)

# Variables
game_active = False
start_time = 0
score = 0

# Main
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_active:            
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
        
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()
    
    if game_active:
        # Background
        screen.blit(sky_surf, (0,0))
        screen.blit(ground_surf, (0,GROUND_Y))

        # Update Player
        player.draw(screen)
        player.update()

        # Update Obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Collisions
        if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
            obstacle_group.empty()
            game_active = False

        # Display Score
        score = int((pygame.time.get_ticks() - start_time) / 1000)
        score_surf = font.render(f'Score: {score}', False, (64,64,64))
        score_rect = score_surf.get_rect(center = (400,50))
        screen.blit(score_surf, score_rect)

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)

        subtitle_surf = font.render('Press Space to Start', False, (111,196,169))
        if score > 0:
            subtitle_surf = font.render(f'Your Score: {score}', False, (111,196,169))
        subtitle_rect = subtitle_surf.get_rect(center = (400,330))

        screen.blit(title_surf, title_rect)
        screen.blit(subtitle_surf, subtitle_rect)

    pygame.display.update()
    clock.tick(60)
