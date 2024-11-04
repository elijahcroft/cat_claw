import pygame
import random
import spritesheet

from cat import Cat

# pygame setup
pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((1280, 920))
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
    screen.fill(purple)
    title_text = font.render("Kitty Claw-Machine", True, white)
    start_text = button_font.render("Start Game", True, white)
    exit_text = button_font.render("Exit", True, white)

    # Displaying title and buttons
    screen.blit(title_text, (screen.get_width() / 2 - title_text.get_width() / 2, screen.get_height() / 4))
    screen.blit(start_text, (screen.get_width() / 2 - start_text.get_width() / 2, screen.get_height() / 2))
    screen.blit(exit_text, (screen.get_width() / 2 - exit_text.get_width() / 2, screen.get_height() / 2 + 60))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check for "Start Game" button click
                if (screen.get_width() / 2 - start_text.get_width() / 2 <= mouse_pos[0] <= screen.get_width() / 2 + start_text.get_width() / 2 and
                    screen.get_height() / 2 <= mouse_pos[1] <= screen.get_height() / 2 + start_text.get_height()):
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
    BG = (50, 50, 50)
    running = True
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    frames = [sprite_sheet.get_image(i, 0, 21.25, 25.75, 3, "black") for i in range(4)]
    frames_up = [sprite_sheet.get_image(i, 1, 21.25, 25.75, 3, "black") for i in range(4)]
    frames_left = [sprite_sheet.get_image(i, 2, 21.25, 25.75, 3, "black") for i in range(4)]
    frames_right = [sprite_sheet.get_image(i, 3, 21.25, 25.75, 3, "black") for i in range(4)]
    
    # Arcade room setup
    screen.fill(purple)
    title_text = font.render("Arcade Room", True, white)
    screen.blit(title_text, (screen.get_width() / 2 - title_text.get_width() / 2, 50))

    # Define machine areas
    machine1_rect = pygame.Rect(300, 300, 150, 150)
    machine2_rect = pygame.Rect(600, 300, 150, 150)


    # Main loop for the arcade room
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with a background color
        screen.fill(BG)

        # Get time delta for consistent movement speed
        dt = clock.tick(60) / 1000

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:  # Move up
            frame_list = frames_up
            player_pos.y -= 300 * dt
        elif keys[pygame.K_s]:  # Move down
            frame_list = frames
            player_pos.y += 300 * dt
        elif keys[pygame.K_a]:  # Move left
            frame_list = frames_left
            player_pos.x -= 300 * dt
        elif keys[pygame.K_d]:  # Move right
            frame_list = frames_right
            player_pos.x += 300 * dt
        else:
            frame_list = frames  # Default to idle animation

        
        frame_counter += animation_speed
        if frame_counter >= len(frame_list):
            frame_counter = 0
        current_frame = int(frame_counter)

        # Draw the player sprite
        screen.blit(frame_list[current_frame], player_pos)

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
