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

buttons = {
    "start": Rect((WIDTH // 2 - BUTTON_WIDTH // 2, 150), (BUTTON_WIDTH, BUTTON_HEIGHT)),
    "instructions": Rect((WIDTH // 2 - BUTTON_WIDTH // 2, 250), (BUTTON_WIDTH, BUTTON_HEIGHT)),
    "audio": Rect((WIDTH // 2 - BUTTON_WIDTH // 2, 350), (BUTTON_WIDTH, BUTTON_HEIGHT)),
    "exit": Rect((WIDTH // 2 - BUTTON_WIDTH // 2, 450), (BUTTON_WIDTH, BUTTON_HEIGHT))
}


stars = generate_stars()


def draw():
    screen.clear()
    if current_screen == SCREEN_MENU:
        draw_menu()
    elif current_screen == SCREEN_GAME:
        draw_game()
    elif current_screen == SCREEN_INSTRUCTIONS:
        draw_instructions()



def update():
    global player, global_speed, animation_interval_player_engine, shoot_timer, charging, charge_timer, accelerating, braking, bullets, energy, heart, shield, bullet_animations, player_shield_animation, shield_active

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
    screen.draw.text("Instruções", center=(WIDTH // 2, 50), fontsize=40, color=WHITE)

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
        screen.draw.text(line, center=(WIDTH // 2, y), fontsize=25, color=WHITE)
        y += 30


def draw_game():
    global energy, heart, shield, shield_active
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


play_music_menu(sounds, audio_on)

pgzrun.go()
