# Example file showing a circle moving on screen
import pygame
import random

from cat import Cat

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 920))
clock = pygame.time.Clock()
running = True
dt = 0
random_location = random.choice([100,900])


player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() /9)
top = screen.get_height()/9

cat = Cat(screen.get_width(), screen.get_height()-200)
# Set a collision distance (e.g., sum of radii)
collision_distance = 80  # change this based on the size of items

distance = player_pos.distance_to(cat.position)
is_moving_down=False
grabbed = False

goal = pygame.Vector2(screen.get_width(),screen.get_width()/9)


#Drop box
rect_width = 300  # Width of the rectangle
rect_height = 200  # Height of the rectangle
rect_color = "pink"  # Color of the rectangle

# bottom right corner
rect_x = screen.get_width() - rect_width
rect_y = screen.get_height() - rect_height

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    pygame.draw.circle(screen, "red", player_pos, 40)
    pygame.draw.rect(screen, rect_color, (rect_x, rect_y, rect_width, rect_height))
    cat.fall()
    if is_moving_down:
        player_pos.y += 300 * dt  
        
        if distance <= collision_distance:
            is_moving_down = False
            grabbed = True
        
        if player_pos.y >= screen.get_height() - 100:
            player_pos.y = screen.get_height() - 100  
            is_moving_down = False
    
    if(is_moving_down==False):
        player_pos.y -= 300 *dt
        if player_pos.y <= top:
            player_pos.y = top

    if grabbed:
        cat.position.y = player_pos.y   
        is_moving_down = False
        print("grabbed true")
        if player_pos.y == top:
            player_pos.x += 300 *dt
            cat.position.x = player_pos.x
            if(player_pos.x >= rect_x+100):
                player_pos.x = rect_x
                grabbed = False
                print("Grabbed false")
                cat = Cat(screen.get_width(), screen.get_height() - 200)

            

            
    
    


    pygame.draw.circle(screen, "blue", (int(cat.position.x), int(cat.position.y)), 40)

    keys = pygame.key.get_pressed()
    dy = dx = 0
    #if keys[pygame.K_w]:
        #player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        if(is_moving_down == False and grabbed == False and player_pos.y == top):
            is_moving_down = True
    if keys[pygame.K_a]:
        if(player_pos.y==top and grabbed==False):
            player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        if(player_pos.y == top and grabbed == False):
            player_pos.x += 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()
    


    distance = player_pos.distance_to(cat.position)
    if distance < collision_distance:
        print("collision")



    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()