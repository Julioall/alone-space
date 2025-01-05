from scripts.constants import *


def play_music_menu(sounds, audio_on):
    if audio_on:
        sounds.running.stop()
        sounds.menu.play(-1)
    else:
        sounds.menu.stop()


def play_sound_select(sounds, audio_on):
    if audio_on:
        sounds.click.play()


def play_sound_running(sounds, audio_on):
    if audio_on:
        sounds.menu.stop()
        sounds.running.play(-1)


def play_sound_start(sounds, audio_on):
    if audio_on:
        sounds.menu.stop()
        sounds.start.play()


def play_sound_shooting_bullet(sounds, audio_on):
    if audio_on:
        sounds.bullet.play()


def play_sound_big_bullet(sounds, audio_on):
    if audio_on:
        sounds.big_bullet.play()


def play_sound_charging(sounds, audio_on):
    if audio_on:
        sounds.charging.play()


def play_sound_shields(sounds, audio_on):
    if audio_on:
        sounds.shields.play()


def stop_sound_shields(sounds, audio_on):
    if audio_on:
        sounds.shields.stop()
