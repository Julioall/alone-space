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

def play_sound_shooting_bullet(sounds, audio_on):
    if audio_on:
        sounds.bullet.play()

def play_sound_big_bullet(sounds, audio_on):
    if audio_on:
        sounds.big_bullet.play()

def play_sound_charging(sounds, audio_on):
    if audio_on:
        sounds.charging.play()