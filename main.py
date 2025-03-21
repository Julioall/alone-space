import pgzrun
import random
from pygame import Rect
from pgzero.actor import Actor
from scripts.constants import *
from scripts.sounds import *
from scripts.animations import *
from scripts.utils import *

current_screen = SCREEN_MENU
current_selected_option_menu = 0
audio_on = True
global_speed = MIN_SPEED
animation_interval_player_engine = ANIMATION_INTERVAL_PLAYER_ENGINE
player = Actor("frigate", (WIDTH / 2, HEIGHT - TILE_SIZE))
player_engine = Actor("frigate_engine-1", (player.x, player.y))
player_engine_animation = setup_animation(player_engine, "frigate_engine", 6)
player_shield = Actor("shield-1", (player.x, player.y))
player_shield_animation = setup_animation(player_shield, "shield", 40)
accelerating = False
braking = False
shield_active = False
bullets = []
bullet_animations = {}
bullet_animation_frames = BULLET_ANIMATION_FRAMES
shoot_timer = 0
shooting = False
charging = False
charge_timer = 0
energy = MAX_ENERGY
heart = MAX_HEALTH
shield = MAX_SHIELD
energy_regeneration_rate = ENERGY_REGENERATION_RATE
heart_regeneration_rate = HEART_REGENERATION_RATE
shield_regeneration_rate = SHIELD_REGENERATION_RATE
energy_cost_acceleration = ENERGY_COST_ACCELERATION
enemy_spawn_timer = 0
enemies_killed = 0
initial_wave_size = 1
enemies = []
enemy_bullets = []
level = 5
total_enemies_killed = 0


buttons = {
    "start": Rect((WIDTH // 2 - BUTTON_WIDTH // 2, 150), (BUTTON_WIDTH, BUTTON_HEIGHT)),
    "instructions": Rect((WIDTH // 2 - BUTTON_WIDTH // 2, 250), (BUTTON_WIDTH, BUTTON_HEIGHT)),
    "audio": Rect((WIDTH // 2 - BUTTON_WIDTH // 2, 350), (BUTTON_WIDTH, BUTTON_HEIGHT)),
    "exit": Rect((WIDTH // 2 - BUTTON_WIDTH // 2, 450), (BUTTON_WIDTH, BUTTON_HEIGHT))
}

stars = generate_stars()


def create_enemy(x, y):
    return {
        "x": x,
        "y": y,
        "health": 30,
        "target_y": 100,
        "side_move_direction": random.choice([-1, 1]),
        "side_move_speed": 2,
        "attack_initiated": False,
        "vertical_move_speed": 1,
        "amplitude": 20,
    }


def move_sideways_random(enemy):
    enemy["x"] += enemy["side_move_direction"] * enemy["side_move_speed"]
    if random.random() < 0.01:
        enemy["side_move_direction"] *= -1


def enemy_attack(enemy):
    if random.random() < 0.02:
        bullet = Rect((enemy["x"], enemy["y"] + TILE_SIZE), (5, 10))
        enemy_bullets.append(bullet)


def update_enemy(enemy):
    if not enemy["attack_initiated"]:
        if enemy["y"] > enemy["target_y"]:
            enemy["attack_initiated"] = True
        enemy["y"] += ENEMY_SPEED

    move_sideways_random(enemy)

    if enemy["x"] < 0 or enemy["x"] > WIDTH:
        enemy["side_move_direction"] *= -1

    enemy_attack(enemy)


def draw_enemies():
    for enemy in enemies:
        enemy_actor = Actor("scout", (enemy["x"], enemy["y"]))
        enemy_actor.draw()

    for bullet in enemy_bullets:
        screen.draw.filled_rect(bullet, (255, 0, 0))


def update_enemies():
    global enemy_spawn_timer, enemies_killed, initial_wave_size
    enemy_spawn_timer += 1
    if enemy_spawn_timer >= ENEMY_SPAWN_RATE and len(enemies) < initial_wave_size:
        for _ in range(initial_wave_size):
            x = random.randint(0, WIDTH)
            y = -TILE_SIZE
            enemies.append(create_enemy(x, y))
        enemy_spawn_timer = 0

    for enemy in enemies[:]:
        update_enemy(enemy)
        if enemy["y"] > HEIGHT:
            enemies.remove(enemy)
        if enemy["health"] <= 0:
            enemies_killed += 1
            enemies.remove(enemy)

    increase_enemy_wave_size()


def increase_enemy_wave_size():
    global initial_wave_size, enemies_killed, level
    if enemies_killed >= initial_wave_size*level:
        initial_wave_size += 1
        level += 1
        enemies_killed = 0


def spawn_enemy_wave():
    global initial_wave_size
    for _ in range(initial_wave_size):
        x = random.randint(0, WIDTH)
        y = -TILE_SIZE
        enemy = Enemy(x, y)
        enemies.append(enemy)


def update_enemy_bullets():
    for bullet in enemy_bullets[:]:
        bullet.y += ENEMY_BULLET_SPEED
        if bullet.y > HEIGHT:
            enemy_bullets.remove(bullet)


def check_collision_bullets_enemies():
    global bullets, enemies, enemies_killed, total_enemies_killed

    for bullet in bullets[:]:
        bullet_rect = Rect((bullet.x - bullet.width // 2, bullet.y - bullet.height // 2), (bullet.width, bullet.height))

        for enemy in enemies[:]:
            enemy_rect = Rect((enemy["x"] - TILE_SIZE // 2, enemy["y"] - TILE_SIZE // 2), (TILE_SIZE, TILE_SIZE))

            if bullet_rect.colliderect(enemy_rect):
                damage = DAMAGE_BULLET if "big_bullet" not in bullet.image else DAMAGE_BULLET_BIG
                enemy["health"] -= damage

                if "big_bullet" not in bullet.image:
                    bullets.remove(bullet)

                if enemy["health"] <= 0:
                    enemies_killed += 1
                    total_enemies_killed += 1
                    enemies.remove(enemy)
                break


def check_collision_player_with_enemy_bullets():
    global heart, current_screen, level, total_enemies_killed, enemies_killed, initial_wave_size
    for bullet in enemy_bullets[:]:
        if player.colliderect(bullet) and not shield_active:
            heart -= DAMAGE_ENEMY_BULLET
            enemy_bullets.remove(bullet)
            if heart <= 0:
                heart = 0
                current_screen = SCREEN_GAME_OVER


def draw_game_over():
    screen.fill(BACKGROUND_COLOR)
    screen.draw.text(
        "GAME OVER", center=(WIDTH // 2, HEIGHT // 4), fontsize=60, color=WHITE
    )
    screen.draw.text(
        f"Level reached: {level - 4}",
        center=(WIDTH // 2, HEIGHT // 2 - 50),
        fontsize=30,
        color=WHITE,
    )
    screen.draw.text(
        f"Enemies defeated: {total_enemies_killed}",
        center=(WIDTH // 2, HEIGHT // 2),
        fontsize=30,
        color=WHITE,
    )
    screen.draw.text(
        "Press ESC to return to the menu",
        center=(WIDTH // 2, HEIGHT - HEIGHT // 4),
        fontsize=25,
        color=WHITE,
    )


def draw():
    screen.clear()
    if current_screen == SCREEN_MENU:
        draw_menu()
    elif current_screen == SCREEN_GAME:
        draw_game()
    elif current_screen == SCREEN_INSTRUCTIONS:
        draw_instructions()
    elif current_screen == SCREEN_GAME_OVER:
        draw_game_over()


def update():
    global player, global_speed, animation_interval_player_engine, shoot_timer, charging, charge_timer, accelerating, braking, bullets, energy, heart, shield, bullet_animations, player_shield_animation, shield_active, current_screen

    if current_screen == SCREEN_GAME:
        update_stars(stars, global_speed)
        player = handle_player_input(player, global_speed, keyboard)
        adjust_speed()
        update_animation(player_engine_animation, animation_interval_player_engine)

        if shield_active and shield >= ENERGY_COST_SHIELD:
            play_sound_shields(sounds, audio_on)
            shield -= ENERGY_COST_SHIELD
            update_animation(player_shield_animation, 1)

        if shield_active and shield <= 0:
            shield_active = False

        if not shield_active:
            stop_sound_shields(sounds, audio_on)

        energy, heart, shield = update_energy_health_shield(
            energy, heart, shield, global_speed)
        global_speed, accelerating, braking = handle_acceleration_and_braking(
            accelerating, braking, energy, global_speed)

        if charging:
            charge_timer -= 1
            if charge_timer <= 0:
                new_bullet = Actor("big_bullet-1", (player.x, player.y - 12))
                new_bullet.damage = DAMAGE_BULLET_BIG
                new_bullet.energy_cost = ENERGY_COST_BIG_BULLET
                bullets.append(new_bullet)
                bullet_animations[new_bullet] = setup_animation(
                    new_bullet, "big_bullet", bullet_animation_frames)
                play_sound_big_bullet(sounds, audio_on)
                energy -= new_bullet.energy_cost
                charging = False

        shoot_timer, energy, bullets, bullet_animations = handle_shooting(
            shooting, energy, shoot_timer, bullets, player, bullet_animations, sounds, audio_on)
        update_bullets(bullets, bullet_animations)
        update_enemies()
        update_enemy_bullets()
        check_collision_bullets_enemies()
        check_collision_player_with_enemy_bullets()

def draw_menu():
    screen.fill(BACKGROUND_COLOR)
    screen.draw.text(TITLE, center=(WIDTH // 2, 100), fontsize=30, color=WHITE)

    for i, name in enumerate(MENU_OPTIONS):
        rect = buttons[name]
        color = WHITE if i != current_selected_option_menu else (200, 200, 255)
        screen.draw.filled_rect(rect, color)
        screen.draw.text(name.capitalize(), center=rect.center,
                         fontsize=25, color=BLACK)


def draw_instructions():
    screen.fill(BACKGROUND_COLOR)
    screen.draw.text("Instruções", center=(
        WIDTH // 2, 50), fontsize=40, color=WHITE)

    instructions_text = [
        "Game Instructions:",
        "W - Accelerate | S - Brake | A and D - Move sideways",
        "",
        "Attacks:",
        "Q - Heavy attack (high energy cost, greater damage)",
        "E - Light attack (lower energy cost, less damage)",
        "",
        "Shield:",
        "F - Activate/deactivate shield (consumes shield energy)",
        "",
        "Objective:",
        "Eliminate as many enemies as possible before being defeated!",
        "",
        "Press ESC to return to the menu."
    ]

    y = 100
    for line in instructions_text:
        screen.draw.text(line, center=(WIDTH // 2, y),
                         fontsize=25, color=WHITE)
        y += 30


def draw_game():
    global energy, heart, shield, shield_active, level, total_enemies_killed

    screen.fill(BACKGROUND_COLOR)
    draw_stars(stars, screen)
    player.draw()
    player_engine.x = player.x
    player_engine.draw()

    if shield_active and shield > ENERGY_COST_SHIELD:
        player_shield.x = player.x
        player_shield.draw()
    else:
        shield_active = False

    for bullet in bullets:
        bullet.draw()

    draw_bars(screen, energy, heart, shield)
    draw_enemies()

    screen.draw.text(
        f"Level: {level-4}", topright=(WIDTH - 10, 10), fontsize=25, color=WHITE)
    screen.draw.text(f"Enemies Killed: {total_enemies_killed}", topright=(
        WIDTH - 10, 40), fontsize=25, color=WHITE)


def on_key_down(key):
    global current_selected_option_menu, current_screen, audio_on, shooting, charging, charge_timer, global_speed, accelerating, braking, shield_active

    if current_screen == SCREEN_MENU:
        current_selected_option_menu, current_screen, audio_on = handle_menu_input(
            current_selected_option_menu, current_screen, audio_on, MENU_OPTIONS, sounds, keyboard)

    elif current_screen == SCREEN_INSTRUCTIONS:
        current_screen = handle_instructions_input(
            current_screen, audio_on, sounds, keyboard)

    elif current_screen == SCREEN_GAME:
        current_screen = handle_game_input(
            current_screen, audio_on, sounds, keyboard)

    elif current_screen == SCREEN_GAME_OVER:
        global level, total_enemies_killed, enemies_killed, initial_wave_size
        current_screen = handle_game_input(
            current_screen, audio_on, sounds, keyboard)
        if current_screen == SCREEN_MENU:
            reset_game()

    if key == keys.E and energy >= ENERGY_COST_BULLET and not shield_active:
        shooting = True

    if key == keys.Q and not charging and energy >= ENERGY_COST_BIG_BULLET and not shield_active:
        charging = True
        charge_timer = CHARGE_DURATION
        play_sound_charging(sounds, audio_on)

    if key == keys.W:
        accelerating = True

    if key == keys.S:
        braking = True

    if key == keys.F and shield > ENERGY_COST_SHIELD:
        shield_active = not shield_active


def on_key_up(key):
    global shooting, accelerating, braking
    if key == keys.E:
        shooting = False
    if key == keys.W:
        accelerating = False
    if key == keys.S:
        braking = False


def adjust_speed():
    global global_speed, animation_interval_player_engine
    if accelerating:
        global_speed = min(global_speed + SPEED_INCREMENT, MAX_SPEED)
    elif braking:
        global_speed = max(global_speed - SPEED_INCREMENT, MIN_SPEED)

    animation_interval_player_engine = max(int(10 - global_speed), 1)


def reset_game():
    global enemies, enemy_bullets, bullets, player, level, total_enemies_killed, enemies_killed, initial_wave_size, heart, energy, shield

    enemies = []
    enemy_bullets = []
    bullets = []
    level = 5
    total_enemies_killed = 0
    enemies_killed = 0
    initial_wave_size = 1

    player.x = WIDTH / 2
    player.y = HEIGHT - TILE_SIZE
    heart = MAX_HEALTH
    energy = MAX_ENERGY
    shield = MAX_SHIELD


play_music_menu(sounds, audio_on)

pgzrun.go()
