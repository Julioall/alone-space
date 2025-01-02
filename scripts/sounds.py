from scripts.constants import *
def play_music_menu(sounds, audio_on):
    if audio_on:
        sounds.running.stop()
        sounds.menu.play()
    else:
        sounds.menu.stop()

def play_sound_select(sounds, audio_on):
    if audio_on:
        sounds.click.play()

def play_sound_running(sounds, audio_on):
    if audio_on:
        sounds.menu.stop()
        sounds.running.play()

def play_sound_starting(sounds, audio_on):
    if audio_on:
        sounds.menu.stop()
        sounds.starting.play()

