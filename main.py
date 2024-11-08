import pygame
import random
import spritesheet
import numpy as np

from cat import Cat

# pygame setup
pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((1280, 960))
clock = pygame.time.Clock() 
running = True
dt = 0
game_state = "navigate"

# fonts and colors
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)
white = (255, 255, 255)
purple = (128, 0, 128)
pink = (255, 182, 193)
blue = (174,198,207)










player_image = pygame.image.load("/home/elijahcroft49/cat_game/claw/claw-neutral.png")
player_image = pygame.transform.scale(player_image, (230, 240))

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 9)
top = screen.get_height() / 9

cat = Cat(screen.get_width(), screen.get_height() - 200)
collision_distance = 180  # distance threshold for collision detection
is_moving_down = False
grabbed = False
goal = pygame.Vector2(screen.get_width(), screen.get_width() / 9)

def start_screen():
    square = pygame.image.load("check.png")
    new_square = pygame.transform.scale(square, (2400,2400))
    background = new_square
    bg_x = 0

    bg_width = screen.get_width()
    bg_speed = 1

    #sine wave

    frequency = .01
    amplitude = 100
    init_time = 0

    



    screen.fill(pink)
    original  = pygame.image.load("kitty_logo.png")
    scaled_image = pygame.transform.scale(original, (612,612))
    title_logo = scaled_image
    exit_text = button_font.render("Exit", True, white)

    original_start = pygame.image.load("start.png")
    scaled_start = pygame.transform.scale(original_start, (342,342))
    start_logo = scaled_start


    center_x = screen.get_width() / 2
    title_y = screen.get_height() / 100
    start_logo_y = screen.get_height() / 1.5


    # Display title and buttons
    screen.blit(title_logo, (center_x - title_logo.get_width() / 2, title_y))
    screen.blit(start_logo, (center_x - start_logo.get_width() / 2, start_logo_y -100))



    pygame.display.flip()

    while True:
        screen.fill(white)
        
        
        bg_x -= bg_speed
        if bg_x <= -bg_width:
            bg_x = 0
        
        init_time += 0.05

        siny = amplitude * np.sin(2*np.pi * frequency * init_time) +300

        
        #screen.blit(background, (bg_x, 0))
        screen.blit(background, (bg_x, siny-800))

        
        screen.blit(title_logo, (center_x - title_logo.get_width() / 2, title_y))
        screen.blit(start_logo, (center_x - start_logo.get_width() / 2, start_logo_y -100))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check for "Start Game" button click
                start_logo_rect = pygame.Rect(center_x - start_logo.get_width() / 2, start_logo_y, start_logo.get_width(), start_logo.get_height())
                if start_logo_rect.collidepoint(mouse_pos):
                    game_state = "navigate"
                    return True  # Start game
                
                # Check for "Exit" button click
                if (screen.get_width() / 2 - exit_text.get_width() / 2 <= mouse_pos[0] <= screen.get_width() / 2 + exit_text.get_width() / 2 and
                    screen.get_height() / 2 + 60 <= mouse_pos[1] <= screen.get_height() / 2 + 60 + exit_text.get_height()):
                    pygame.quit()
                    return False
        
                


#acrade_plauer 


try:
    sprite_sheet_image = pygame.image.load("sprites.png").convert_alpha()
    sprite_sheet = spritesheet.spriteSheet(sprite_sheet_image)
except pygame.error as e:
    print(f"Unable to load sprites: {e}")
    running = False





def navigate():
    current_frame = 0
    animation_speed = 0.1
    frame_counter = 0
    BG = pygame.image.load("small.png")
    running = True  
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    
    idle0 = sprite_sheet.get_image(0,0,21.25,25.75,3, "black")
    idle1 = sprite_sheet.get_image(0,1,21.25,25.75,3, "black")
    idle2 = sprite_sheet.get_image(0,2,21.25,25.75,3, "black")
    idle3 = sprite_sheet.get_image(0,3,21.25,25.75,3, "black")
    idle_num = idle0
    

    frames = [sprite_sheet.get_image(i, 0, 21.25, 25.75, 3, "black") for i in range(4)]
    frames_up = [sprite_sheet.get_image(i, 1, 21.25, 25.75, 3, "black") for i in range(4)]
    frames_left = [sprite_sheet.get_image(i, 2, 21.25, 25.75, 3, "black") for i in range(4)]
    frames_right = [sprite_sheet.get_image(i, 3, 21.25, 25.75, 3, "black") for i in range(4)]
    
    # Arcade room setup
    screen.fill(purple)
    title_text = font.render("Arcade Room", True, white)
    screen.blit(title_text, (screen.get_width() / 2 - title_text.get_width() / 2, 50))

    # Define machine areas
    claw_machines = [
        pygame.Rect(300, 300, 150, 150),  # Machine 1
        pygame.Rect(600, 300, 150, 150),  # Machine 2
    ]



    # Main loop for the arcade room
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with a background color
        screen.blit(BG,(0,0))
        idle = [idle_num]  

        # Get time delta for consistent movement speed
        dt = clock.tick(60) / 1000

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:  # Move up
            idle_num = idle1
            frame_list = frames_up
            player_pos.y -= 200 * dt
        elif keys[pygame.K_s]:  # Move down
            idle_num = idle0
            frame_list = frames
            player_pos.y += 200 * dt
        elif keys[pygame.K_a]:  # Move left
            idle_num = idle2
            frame_list = frames_left
            player_pos.x -= 200 * dt
        elif keys[pygame.K_d]:  # Move right
            idle_num = idle3
            frame_list = frames_right
            player_pos.x += 200 * dt
        else:
            frame_list = idle  # Default to idle animation

        
        frame_counter += animation_speed
        if frame_counter >= len(frame_list):
            frame_counter = 0
        current_frame = int(frame_counter)

        # Draw the player sprite
        screen.blit(frame_list[current_frame], player_pos)

        for machine_rect in claw_machines:
            pygame.draw.rect(screen, pink, machine_rect)

        # Check if player is over any claw machine and space is pressed
        for machine_rect in claw_machines:
            if machine_rect.collidepoint(player_pos.x, player_pos.y) and keys[pygame.K_SPACE]:
                # Switch to the claw machine game
                return "play_claw_machine" 

        # Flip the display to put your work on the screen
        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False



def chance():
    return 0 

# Drop box
rect_width = 300
rect_height = 200
rect_color = pink

# bottom right corner
rect_x = screen.get_width() - rect_width
rect_y = screen.get_height() - rect_height

if start_screen():
    while running:
        if game_state == "navigate":
            game_state = navigate()
        elif game_state == "play_claw_machine":
            pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(purple)
        screen.blit(player_image, player_pos)
        pygame.draw.rect(screen, rect_color, (rect_x, rect_y, rect_width, rect_height))
        cat.fall()
        

        if is_moving_down:
            player_pos.y += 300 * dt
            if player_pos.distance_to(cat.position) <= collision_distance:
                is_moving_down = False
                grabbed = True
            if player_pos.y >= screen.get_height() - 100:
                player_pos.y = screen.get_height() - 100
                is_moving_down = False

        if not is_moving_down:
            player_pos.y -= 300 * dt
            if player_pos.y <= top:
                player_pos.y = top

        if grabbed:
            cat.position.y = player_pos.y
            is_moving_down = False
            if player_pos.y == top:
                player_pos.x += 300 * dt
                cat.position.x = player_pos.x
                if player_pos.x >= rect_x + 100:
                    player_pos.x = rect_x
                    grabbed = False

        if not grabbed:
            cat.position.y += 300 * dt
            if cat.position.y >= screen.get_height() - 100:
                cat.position.y = screen.get_height() - 100

        pygame.draw.circle(screen, "blue", (int(cat.position.x), int(cat.position.y)), 40)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_s] and not is_moving_down and not grabbed and player_pos.y == top:
            is_moving_down = True
        if keys[pygame.K_a] and player_pos.y == top and not grabbed:
            player_pos.x -= 300 * dt
        if keys[pygame.K_d] and player_pos.y == top and not grabbed:
            player_pos.x += 300 * dt

        pygame.display.flip()

        dt = clock.tick(60) / 1000  # FPS limit to 60, with dt as delta time for framerate independence

pygame.quit()
