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



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("blue")

    player = pygame.draw.circle(screen, "red", player_position, 40)

    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    mouse_position = pygame.mouse.get_pos()

    if keys[pygame.K_w]:
        player_position.y -= 300 *dt
    if keys[pygame.K_s]:
        player_position.y += 300 *dt
    if keys[pygame.K_a]:
        player_position.x -= 300 * dt
    if keys[pygame.K_d]:
        player_position.x += 300 * dt

    if keys[pygame.K_ESCAPE]:
        pygame.quit()

    time_since_last_shot = pygame.time.get_ticks() - last_shot_time
    if mouse[0] and time_since_last_shot >= shot_cooldown * 1000:
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
        direction = player_position - enemy
        direction.normalize_ip()
        enemy += direction * 100 * dt
        pygame.draw.circle(screen,(0, 0, 0), enemy, 29)
        pygame.draw.circle(screen, "yellow", enemy, 25)


        if pygame.math.Vector2.distance_to(player_position, enemy) < 40:
            time_since_last_damage = pygame.time.get_ticks() - last_damage_time
            if time_since_last_damage>= damage_interval * 1000:
                player_health -= 1
                last_damage_time = pygame.time.get_ticks()

    health_text = font.render(f"Health: {player_health}", True, (255, 255, 255))
    kills_text = font.render(f"Kills: {kills}", True, (255, 255, 255))

    screen.blit(health_text, (screen.get_width() -140, 20))
    screen.blit(kills_text, (screen.get_width() - 140, 50))

    pygame.display.flip()

    dt = clock.tick(120)  / 1000

pygame.quit()