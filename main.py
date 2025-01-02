import pgzrun
from pygame import Rect

from scripts.constants import *
from scripts.sounds import *
from scripts.animations import *
from scripts.utils import *
from scripts.input_handler import *

current_screen = SCREEN_MENU
current_selected_option_menu = 0
audio_on = True
button_width = 200
button_height = 50
hyper_speed = False
global_speed = 1
min_speed = 1
max_speed = 6
speed_increment = 0.05
animation_interval_player_engine = 20
player = Actor("frigate")
player.x = WIDTH/2
player.y = HEIGHT-TILE_SIZE

player_engine = Actor("frigate_engine-1")
player_engine_animation = setup_animation(player_engine, "frigate_engine", 6)
player_engine.x = WIDTH/2
player_engine.y = HEIGHT-TILE_SIZE
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
    global player
    adjust_speed()
    update_stars(stars, global_speed)
    player = handle_player_input(player, global_speed, keyboard)
    update_animation(player_engine_animation, animation_interval_player_engine)

def draw_menu():
    screen.fill(BACKGROUND_COLOR)
    screen.draw.text("Main Menu", center=(WIDTH // 2, 100), fontsize=50, color=WHITE)

    for i, name in enumerate(MENU_OPTIONS):
        rect = buttons[name]
        color = WHITE if i != current_selected_option_menu else (200, 200, 255)
        screen.draw.filled_rect(rect, color)
        screen.draw.text(name.capitalize(), center=rect.center, fontsize=30, color=BLACK)

def draw_game():
    screen.fill(BACKGROUND_COLOR)
    
    draw_stars(stars, screen)
    player.draw()
    player_engine.x = player.x
    player_engine.draw()

def adjust_speed():
    global global_speed, animation_interval_player_engine
    if hyper_speed:
        global_speed = min(global_speed + speed_increment, max_speed)
        animation_interval_player_engine = max(int(10 - global_speed), 1)
    else:
        global_speed = max(global_speed - speed_increment, min_speed)
        animation_interval_player_engine = 10

def on_key_down(key):
    global current_selected_option_menu, current_screen, audio_on, hyper_speed

    if current_screen == "menu":
        current_selected_option_menu, current_screen, audio_on = handle_menu_input(current_selected_option_menu, current_screen, audio_on, MENU_OPTIONS, sounds, keyboard)
    elif current_screen == "game":
        current_screen = handle_game_input(current_screen, audio_on, sounds, keyboard)
    
    if key in [keys.UP, keys.W]:
        hyper_speed = True

def on_key_up(key):
    global hyper_speed
    if key in [keys.UP, keys.W]:
        hyper_speed = False

play_music_menu(sounds, audio_on)

pgzrun.go()
