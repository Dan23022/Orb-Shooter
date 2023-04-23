import random
import pygame


pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
running = True
dt = 0

player_position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
projectiles = []
projectile_speed = 700
last_shot_time = 0
shot_cooldown = 0.2

kills = 0

player_health = 10
last_damage_time = 0
damage_interval = 1.0

enemies = []
enemies_spawn_time = 0
enemies_spawn_delay = 1
max_enemies = 25
enemies_respawn_delay = 1.0
last_enemy_death_time = 0

font = pygame.font.SysFont(None, 32)

game_state = "menu"

start_button = pygame.Rect(screen.get_width() // 2 - 100, 300, 200, 50)
quit_button = pygame.Rect(screen.get_width() // 2 - 100, 400, 200, 50)

blue = (106, 159, 181)
red = (191, 39, 33)
green = (100, 200, 100)
black = (0, 0, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)

title_font = pygame.font.SysFont(None, 72)
start_text = font.render("Start Game", True, black)
quit_text = font.render("Quit", True, black)

game_over_title_font = pygame.font.SysFont(None, 72)
game_over_text = game_over_title_font.render("Game Over", True, red)

game_over_restart_button = pygame.Rect(screen.get_width() // 2 - 100, 300, 200, 50)
game_over_quit_button = pygame.Rect(screen.get_width() // 2 - 100, 400, 200, 50)

restart_text = font.render("Restart", True, black)
quit_text = font.render("Quit", True, black)



title_font = pygame.font.SysFont(None, 72)
start_text = font.render("Start Game", True, black)
quit_text = font.render("Quit", True, black)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == "menu":
        screen.fill(blue)
        pygame.draw.rect(screen, white, start_button)
        pygame.draw.rect(screen, white, quit_button)
        title_text = title_font.render("Orb Shooter", True, white)
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 100))
        screen.blit(start_text, (start_button.centerx - start_text.get_width() // 2, start_button.centery - start_text.get_height() // 2))
        screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2, quit_button.centery - quit_text.get_height() // 2))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if start_button.collidepoint(mouse):
            pygame.draw.rect(screen, green, start_button, 3)
            if click[0]:
                game_state = "playing"
        else:
            pygame.draw.rect(screen, white, start_button, 3)

        if quit_button.collidepoint(mouse):
            pygame.draw.rect(screen, red, quit_button, 3)
            if click[0]:
                running = False
        else:
            pygame.draw.rect(screen, white, quit_button, 3)

    elif game_state == "playing":
        screen.fill("blue")

    if game_state == "game_over":
        screen.fill(blue)

        pygame.draw.rect(screen, white, game_over_restart_button)
        pygame.draw.rect(screen, white, game_over_quit_button)

        screen.blit(kills_text, (screen.get_width() // 2 - title_text.get_width() // 2, 100))
        screen.blit(restart_text, (game_over_restart_button.centerx - start_text.get_width() // 2, start_button.centery - start_text.get_height() // 2))
        screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2, quit_button.centery - quit_text.get_height() // 2))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if game_over_restart_button.collidepoint(mouse):
            pygame.draw.rect(screen, green, start_button, 3)
            if click[0]:
                game_state = "playing"
        else:
            pygame.draw.rect(screen, white, start_button, 3)

        if game_over_quit_button.collidepoint(mouse):
            pygame.draw.rect(screen, red, quit_button, 3)
            if click[0]:
                running = False
        else:
            pygame.draw.rect(screen, white, quit_button, 3)

    elif game_state == "playing":
        screen.fill("blue")

    player = pygame.draw.circle(screen, "red", player_position, 40)

    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    mouse_position = pygame.mouse.get_pos()

    if keys[pygame.K_w] and not game_state == "menu":
        player_position.y -= 300 *dt
    if keys[pygame.K_s] and not game_state == "menu":
        player_position.y += 300 *dt
    if keys[pygame.K_a] and not game_state == "menu":
        player_position.x -= 300 * dt
    if keys[pygame.K_d] and not game_state == "menu":
        player_position.x += 300 * dt

    if keys[pygame.K_ESCAPE]:
        pygame.quit()

    time_since_last_shot = pygame.time.get_ticks() - last_shot_time
    if mouse[0] and time_since_last_shot >= shot_cooldown * 1000 and not game_state == "menu":
        projectile_position = pygame.Vector2(player_position)
        direction = pygame.Vector2(mouse_position) - projectile_position
        direction.normalize_ip()
        velocity = direction * projectile_speed
        projectiles.append((projectile_position, velocity))
        last_shot_time = pygame.time.get_ticks()

    time_since_last_enemy = pygame.time.get_ticks() - enemies_spawn_time
    if time_since_last_enemy >= enemies_spawn_delay * 1000 and len(enemies) < max_enemies:
        if pygame.time.get_ticks() - last_enemy_death_time >= enemies_respawn_delay * 1000:
            enemy_position = pygame.Vector2(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))
            enemies.append(enemy_position)
            enemy_spawn_time = pygame.time.get_ticks()

    for projectile in projectiles:
        projectile_position, velocity = projectile
        projectile_position += velocity * dt

        if not screen.get_rect().collidepoint(projectile_position):
            projectiles.remove(projectile)
            continue

        pygame.draw.circle(screen, "green", projectile_position, 10)

        for enemy in enemies:
            if pygame.Vector2(enemy).distance_to(projectile_position) < 25:
                enemies.remove(enemy)
                kills += 1
                last_enemy_death_time = pygame.time.get_ticks()
                try:
                    projectiles.remove(projectile)
                except:
                    pass

    for enemy in enemies:
        if not game_state == "menu":
            direction = player_position - enemy
            direction.normalize_ip()
            enemy += direction * 100 * dt
            pygame.draw.circle(screen,(0, 0, 0), enemy, 29)
            pygame.draw.circle(screen, "yellow", enemy, 25)


        if pygame.math.Vector2.distance_to(player_position, enemy) < 40 :
            time_since_last_damage = pygame.time.get_ticks() - last_damage_time
            if time_since_last_damage >= damage_interval * 1000 and not game_state == "menu":
                player_health -= 1
                last_damage_time = pygame.time.get_ticks()
                if player_health == 0:
                    game_state = "game_over"

    health_text = font.render(f"Health: {player_health}", True, (255, 255, 255))
    kills_text = font.render(f"Kills: {kills}", True, (255, 255, 255))

    screen.blit(health_text, (screen.get_width() -140, 20))
    screen.blit(kills_text, (screen.get_width() - 140, 50))

    pygame.display.flip()

    dt = clock.tick(120)  / 1000

pygame.quit()