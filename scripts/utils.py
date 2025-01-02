from random import randint, uniform
from scripts.constants import *
from pygame import Rect

def _move_star(star,speed):
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
    for _ in range(randint(50,300)):
        x = randint(0, WIDTH)
        y = randint(0, HEIGHT)
        size = randint(1, 3)
        brightness = randint(0, 255)
        speed = uniform(0.5, 3)
        stars.append({"x": x, "y": y, "size": size, "brightness": brightness, "speed": speed, "direction": 1})
    return stars


def update_stars(stars, speed):
    for star in stars:
        _move_star(star, speed)
        _update_star_brightness(star)

def draw_stars(stars, screen):
    for star in stars:
        color = (star["brightness"], star["brightness"], star["brightness"])
        screen.draw.filled_rect(Rect((star["x"], star["y"]), (star["size"], star["size"])), color)
