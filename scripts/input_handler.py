from scripts.sounds import *


def _change_selected_option(direction, current_selected_option_menu, MENU_OPTIONS, sounds, audio_on):
    current_selected_option_menu = (current_selected_option_menu + direction) % len(MENU_OPTIONS)
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
        current_selected_option_menu = _change_selected_option(-1, current_selected_option_menu, MENU_OPTIONS, sounds, audio_on)
    elif keyboard.DOWN or keyboard.S:
        current_selected_option_menu = _change_selected_option(1, current_selected_option_menu, MENU_OPTIONS, sounds, audio_on)
    elif keyboard.SPACE:
        current_screen, audio_on = _select_menu_option(current_selected_option_menu, current_screen, audio_on, MENU_OPTIONS, sounds)
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
