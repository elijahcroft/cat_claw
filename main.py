import pygame
import random

from cat import Cat

# pygame setup
pygame.init()
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
def navigate():
    screen.fill(purple)
    title_text = font.render("Arcade Room", True, white)
    screen.blit(title_text, (screen.get_width() / 2 - title_text.get_width() / 2, 50))

    # Draw machine areas (rectangles here as placeholders)
    machine1_rect = pygame.Rect(300, 300, 150, 150)
    machine2_rect = pygame.Rect(600, 300, 150, 150)

    pygame.draw.rect(screen, pink, machine1_rect)  # Machine 1
    pygame.draw.rect(screen, pink, machine2_rect)  # Machine 2 (add more as needed)

    # Display machine labels
    machine1_text = button_font.render("Claw Machine", True, white)
    screen.blit(machine1_text, (machine1_rect.x + 10, machine1_rect.y + machine1_rect.height + 10))

    pygame.display.flip()

    # Wait for user to click on a machine
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check if the player clicked on the claw machine
                if machine1_rect.collidepoint(mouse_pos):
                    return "claw_machine"  # Start the claw machine game

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

        # fill the screen with a color to wipe away anything from last frame
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
