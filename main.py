import pgzrun
from pygame import Rect
from pgzero.actor import Actor

from scripts.constants import *
from scripts.sounds import *
from scripts.animations import *
from scripts.utils import *

current_screen = SCREEN_MENU
current_selected_option_menu = 0
audio_on = True
button_width = 200
button_height = 50
global_speed = 1
min_speed = 1
max_speed = 6
speed_increment = 0.05
animation_interval_player_engine = 20
player = Actor("frigate")
player.x = WIDTH / 2
player.y = HEIGHT - TILE_SIZE

player_engine = Actor("frigate_engine-1")
player_engine_animation = setup_animation(player_engine, "frigate_engine", 6)
player_engine.x = WIDTH / 2
player_engine.y = HEIGHT - TILE_SIZE
accelerating = False
braking = False
bullets = []
bullet_animation_frames = 4
bullet_interval = 5
bullet_animations = {}

shooting = False
shoot_interval = 15
shoot_timer = 0
reload_time = 60
is_reloading = False
reload_timer = 0
charging = False
charge_timer = 0
charge_duration = 60

energy = 100
max_energy = 100

heart = 100
max_health = 100

shield = 100
max_shield = 100

energy_regeneration_rate = 1
heart_regeneration_rate = 1
shield_regeneration_rate = 1

energy_cost_acceleration = 1

buttons = {
    "start": Rect((WIDTH // 2 - button_width // 2, 200), (button_width, button_height)),
    "audio": Rect((WIDTH // 2 - button_width // 2, 300), (button_width, button_height)),
    "exit": Rect((WIDTH // 2 - button_width // 2, 400), (button_width, button_height))
}

stars = generate_stars()


def draw():
    screen.clear()
    if current_screen == "menu":
        draw_menu()
    elif current_screen == "game":
        draw_game()


def update():
    global player, global_speed, animation_interval_player_engine, shoot_timer, charging, charge_timer, accelerating, braking, bullets, energy, heart, shield, energy_regeneration_rate, heart_regeneration_rate, shield_regeneration_rate, bullet_animations

    update_stars(stars, global_speed)
    player = handle_player_input(player, global_speed, keyboard)
    update_animation(player_engine_animation, animation_interval_player_engine)

    # Atualização de energia, vida e escudo
    energy, heart, shield = update_energy_health_shield(
        energy, heart, shield, max_energy, max_health, max_shield, energy_regeneration_rate, heart_regeneration_rate, shield_regeneration_rate, global_speed)

    # Atualização de energia, vida e escudo
    energy, heart, shield = update_energy_health_shield(
        energy, heart, shield, max_energy, max_health, max_shield, energy_regeneration_rate, heart_regeneration_rate, shield_regeneration_rate, global_speed)

    # Aceleração e desaceleração
    global_speed, accelerating, braking = handle_acceleration_and_braking(
        accelerating, braking, energy, global_speed, energy_cost_acceleration, speed_increment, max_speed, min_speed)

    # Carregamento e tiro especial
    if charging:
        charge_timer -= 1
        if charge_timer <= 0:
            new_bullet = Actor("big_bullet-1", (player.x, player.y - 12))
            new_bullet.damage = 50
            new_bullet.energy_cost = ENERGY_COST_BIG_BULLET
            bullets.append(new_bullet)
            bullet_animations[new_bullet] = setup_animation(
                new_bullet, "big_bullet", bullet_animation_frames)
            play_sound_big_bullet(sounds, audio_on)
            energy -= new_bullet.energy_cost
            charging = False
    # Tiro comum
    shoot_timer, energy, bullets, bullet_animations = handle_shooting(
        shooting, energy, shoot_timer, shoot_interval, bullets, player, bullet_animations, sounds, audio_on, bullet_animation_frames)

    # Atualização das balas
    update_bullets(bullets, bullet_animations, bullet_animation_frames)


def draw_menu():
    screen.fill(BACKGROUND_COLOR)
    screen.draw.text("Alone Space", center=(
        WIDTH // 2, 100), fontsize=50, color=WHITE)

    for i, name in enumerate(MENU_OPTIONS):
        rect = buttons[name]
        color = WHITE if i != current_selected_option_menu else (200, 200, 255)
        screen.draw.filled_rect(rect, color)
        screen.draw.text(name.capitalize(), center=rect.center,
                         fontsize=30, color=BLACK)


def draw_game():
    screen.fill(BACKGROUND_COLOR)
    draw_stars(stars, screen)
    player.draw()
    player_engine.x = player.x
    player_engine.draw()

    for bullet in bullets:
        bullet.draw()

    draw_bars(screen, energy, heart, shield,
              max_energy, max_health, max_shield)


def on_key_down(key):
    global current_selected_option_menu, current_screen, audio_on, shooting, charging, charge_timer, global_speed, accelerating, braking

    if current_screen == "menu":
        current_selected_option_menu, current_screen, audio_on = handle_menu_input(
            current_selected_option_menu, current_screen, audio_on, MENU_OPTIONS, sounds, keyboard)
    elif current_screen == "game":
        current_screen = handle_game_input(
            current_screen, audio_on, sounds, keyboard)

    if key == keys.E and energy >= ENERGY_COST_BULLET:
        shooting = True

    if key == keys.Q and not charging and energy >= ENERGY_COST_BIG_BULLET:
        charging = True
        charge_timer = charge_duration
        play_sound_charging(sounds, audio_on)

    if key == keys.W:
        accelerating = True

    if key == keys.S:
        braking = True


def on_key_up(key):
    global shooting, accelerating, braking
    if key == keys.E:
        shooting = False
    if key == keys.W:
        accelerating = False
    if key == keys.S:
        braking = False


play_music_menu(sounds, audio_on)

pgzrun.go()
