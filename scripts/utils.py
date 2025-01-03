from random import randint, uniform
from pgzero.actor import Actor
from pygame import Rect

from scripts.animations import *
from scripts.constants import *
from scripts.sounds import *


def _change_selected_option(direction, current_selected_option_menu, MENU_OPTIONS, sounds, audio_on):
    current_selected_option_menu = (
        current_selected_option_menu + direction) % len(MENU_OPTIONS)
    play_sound_select(sounds, audio_on)
    return current_selected_option_menu


def _select_menu_option(current_selected_option_menu, current_screen, audio_on, MENU_OPTIONS, sounds):
    selected = MENU_OPTIONS[current_selected_option_menu]
    if selected == "start":
        current_screen = SCREEN_GAME
        play_sound_starting(sounds, audio_on)
        play_sound_running(sounds, audio_on)
    elif selected == "audio":
        audio_on = not audio_on
        play_music_menu(sounds, audio_on)
    elif selected == "exit":
        quit()
    return current_screen, audio_on


def handle_menu_input(current_selected_option_menu, current_screen, audio_on, MENU_OPTIONS, sounds, keyboard):
    if keyboard.UP or keyboard.W:
        current_selected_option_menu = _change_selected_option(
            -1, current_selected_option_menu, MENU_OPTIONS, sounds, audio_on)
    elif keyboard.DOWN or keyboard.S:
        current_selected_option_menu = _change_selected_option(
            1, current_selected_option_menu, MENU_OPTIONS, sounds, audio_on)
    elif keyboard.SPACE:
        current_screen, audio_on = _select_menu_option(
            current_selected_option_menu, current_screen, audio_on, MENU_OPTIONS, sounds)
    return current_selected_option_menu, current_screen, audio_on


def handle_game_input(current_screen, audio_on, sounds, keyboard):
    if keyboard.ESCAPE:
        play_music_menu(sounds, audio_on)
        current_screen = "menu"
    return current_screen


def handle_player_input(player, global_speed, keyboard):
    if keyboard.LEFT or keyboard.A:
        if player.left > 0:
            player.x -= global_speed + 3
    if keyboard.RIGHT or keyboard.D:
        if player.right < WIDTH:
            player.x += global_speed + 3
    return player


def _move_star(star, speed):
    star["y"] += star["speed"] * speed
    if star["y"] > HEIGHT:
        star["y"] = 0
        star["x"] = randint(0, WIDTH)


def _update_star_brightness(star):
    star["brightness"] += star["speed"] * star["direction"]
    if star["brightness"] >= 255:
        star["brightness"] = 255
        star["direction"] = -1
    elif star["brightness"] <= 50:
        star["brightness"] = 50
        star["direction"] = 1


def generate_stars():
    stars = []
    for _ in range(randint(50, 300)):
        x = randint(0, WIDTH)
        y = randint(0, HEIGHT)
        size = randint(1, 3)
        brightness = randint(0, 255)
        speed = uniform(0.5, 3)
        stars.append({"x": x, "y": y, "size": size,
                     "brightness": brightness, "speed": speed, "direction": 1})
    return stars


def update_stars(stars, speed):
    for star in stars:
        _move_star(star, speed)
        _update_star_brightness(star)


def draw_stars(stars, screen):
    for star in stars:
        color = (star["brightness"], star["brightness"], star["brightness"])
        screen.draw.filled_rect(
            Rect((star["x"], star["y"]), (star["size"], star["size"])), color)


def draw_bars(screen, energy, heart, shield, max_energy, max_health, max_shield):
    energy_bar_width = 300
    energy_bar_height = 5

    screen.draw.filled_rect(Rect(10, 10, heart * (energy_bar_width / max_health),
                            energy_bar_height), (255, 0, 0))  # Vermelho para vida
    screen.draw.filled_rect(Rect(10, 20, shield * (energy_bar_width /
                            max_shield), energy_bar_height), (0, 0, 255))  # Azul para escudo
    screen.draw.filled_rect(Rect(10, 30, energy * (energy_bar_width / max_energy),
                            energy_bar_height), (0, 255, 0))  # Verde para energia


def update_energy_health_shield(energy, heart, shield, max_energy, max_health, max_shield, energy_regeneration_rate, heart_regeneration_rate, shield_regeneration_rate, global_speed):
    if energy < max_energy:
        energy += energy_regeneration_rate - (global_speed / 6.5)
    if heart < max_health:
        heart += heart_regeneration_rate
    if shield < max_shield:
        shield += shield_regeneration_rate
    return energy, heart, shield


def handle_acceleration_and_braking(accelerating, braking, energy, global_speed, energy_cost_acceleration, speed_increment, max_speed, min_speed):
    if accelerating:
        if energy >= energy_cost_acceleration:
            global_speed = min(global_speed + speed_increment, max_speed)
        else:
            accelerating = False
    if braking:
        global_speed = max(global_speed - speed_increment, min_speed)
    return global_speed, accelerating, braking


def handle_shooting(shooting, energy, shoot_timer, shoot_interval, bullets, player, bullet_animations, sounds, audio_on, bullet_animation_frames):
    if shooting and energy >= ENERGY_COST_BULLET:
        shoot_timer += 1
        if shoot_timer >= shoot_interval:
            new_bullet = Actor(
                "bullet-1", (player.x, player.y - (TILE_SIZE / 4)))
            new_bullet.damage = 10
            new_bullet.energy_cost = ENERGY_COST_BULLET
            bullets.append(new_bullet)
            bullet_animations[new_bullet] = setup_animation(
                new_bullet, "bullet", bullet_animation_frames)
            shoot_timer = 0
            play_sound_shooting_bullet(sounds, audio_on)
            energy -= new_bullet.energy_cost
    return shoot_timer, energy, bullets, bullet_animations


def update_bullets(bullets, bullet_animations, bullet_animation_frames):
    for bullet in bullets[:]:
        bullet.y -= 10
        update_animation(bullet_animations[bullet], bullet_animation_frames)
        if bullet.y < 0:
            bullets.remove(bullet)
            del bullet_animations[bullet]
