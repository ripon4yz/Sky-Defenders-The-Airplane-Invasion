import pygame
import random

pygame.init()

# Screen dimensions
dis_width = 800
dis_height = 600

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
gray = (169, 169, 169)

# Initialize display
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("Space Invaders")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("bahnschrift", 35)

# Spaceship (airplane) properties
ship_width = 60
ship_height = 40
ship_speed = 6

# Bullet properties
bullet_width = 5
bullet_height = 10
bullet_speed = -10

# Enemy properties
enemy_width = 40
enemy_height = 40
enemy_speed = 2

# Asteroid properties
asteroid_width = 30
asteroid_height = 30
asteroid_speed = 5

def message(msg, color, y_offset=0):
    """Displays a message on the screen."""
    mesg = font.render(msg, True, color)
    dis.blit(mesg, [dis_width / 2 - mesg.get_width() / 2, dis_height / 2 + y_offset])

def create_enemies(rows, cols):
    """Create a grid of enemies."""
    enemies = []
    for row in range(rows):
        for col in range(cols):
            x = col * (enemy_width + 20) + 100
            y = row * (enemy_height + 20) + 50
            enemies.append(pygame.Rect(x, y, enemy_width, enemy_height))
    return enemies

def create_asteroids():
    """Create asteroids."""
    asteroid = pygame.Rect(random.randint(0, dis_width - asteroid_width), 0, asteroid_width, asteroid_height)
    return asteroid

# Main game loop
def game_loop():
    # Spaceship position
    ship_x = dis_width / 2
    ship_y = dis_height - ship_height - 10

    # Bullet list
    bullets = []

    # Enemy list
    enemies = create_enemies(4, 8)

    # Asteroid list
    asteroids = []

    # Enemy direction
    enemy_direction = 1

    # Game state
    running = True
    score = 0

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get pressed keys
        keys = pygame.key.get_pressed()

        # Move the spaceship (airplane)
        if keys[pygame.K_LEFT] and ship_x > 0:
            ship_x -= ship_speed
        if keys[pygame.K_RIGHT] and ship_x < dis_width - ship_width:
            ship_x += ship_speed

        # Fire bullets
        if keys[pygame.K_SPACE]:
            if len(bullets) < 5:  # Limit the number of bullets on screen
                bullets.append(
                    pygame.Rect(ship_x + ship_width // 2 - bullet_width // 2, ship_y, bullet_width, bullet_height)
                )

        # Update bullets
        for bullet in bullets[:]:
            bullet.y += bullet_speed
            if bullet.y < 0:
                bullets.remove(bullet)

        # Move enemies
        for enemy in enemies:
            enemy.x += enemy_speed * enemy_direction

        # Change direction when enemies hit the edge
        if any(enemy.x <= 0 or enemy.x >= dis_width - enemy_width for enemy in enemies):
            enemy_direction *= -1
            for enemy in enemies:
                enemy.y += enemy_height // 2

        # Check collisions between bullets and enemies
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if enemy.colliderect(bullet):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10
                    break

        # Spawn new enemies after some time
        if random.random() < 0.01:  # Adjust the probability for new enemies
            enemies.append(pygame.Rect(random.randint(0, dis_width - enemy_width), random.randint(50, 200), enemy_width, enemy_height))

        # Create asteroids randomly
        if random.random() < 0.05:  # Adjust frequency of asteroid spawn
            asteroids.append(create_asteroids())

        # Move and check for asteroid collisions
        for asteroid in asteroids[:]:
            asteroid.y += asteroid_speed
            if asteroid.y > dis_height:
                asteroids.remove(asteroid)

            # Check if asteroid collides with the spaceship
            if asteroid.colliderect(pygame.Rect(ship_x, ship_y, ship_width, ship_height)):
                message("Game Over! Press R to Restart or Q to Quit", red)
                message("Developed by Ripon R. Rahman", white, 50)  # Added developer message
                pygame.display.update()
                pygame.time.delay(2000)
                return

        # Clear the screen
        dis.fill(black)

        # Draw spaceship (airplane) as a triangle
        airplane_points = [(ship_x, ship_y), (ship_x + ship_width, ship_y), (ship_x + ship_width // 2, ship_y - ship_height)]
        pygame.draw.polygon(dis, blue, airplane_points)

        # Draw bullets
        for bullet in bullets:
            pygame.draw.rect(dis, red, bullet)

        # Draw enemies
        for enemy in enemies:
            pygame.draw.rect(dis, green, enemy)

        # Draw asteroids
        for asteroid in asteroids:
            pygame.draw.rect(dis, (139, 69, 19), asteroid)  # Brown color for asteroids

        # Draw score
        score_text = font.render(f"Score: {score}", True, white)
        dis.blit(score_text, (10, 10))

        # Update display
        pygame.display.update()

        # Control frame rate
        clock.tick(60)

    pygame.quit()
    quit()


# Run the game
game_loop()
