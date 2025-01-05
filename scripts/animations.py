from scripts.constants import *


def setup_animation(actor, image_prefix, num_frames, start_frame=0):
    animation_frames = [f"{image_prefix}-{i+1}" for i in range(num_frames)]
    actor.image = animation_frames[start_frame]
    return {
        "actor": actor,
        "frames": animation_frames,
        "current_frame": start_frame,
        "frame_counter": 0,
    }


def update_animation(animation_data, frame_interval):
    animation_data["frame_counter"] += 1
    if animation_data["frame_counter"] >= frame_interval:
        animation_data["frame_counter"] = 0
        _advance_animation_frame(animation_data)


def _advance_animation_frame(animation_data):
    animation_data["current_frame"] = (
        animation_data["current_frame"] + 1) % len(animation_data["frames"])
    animation_data["actor"].image = animation_data["frames"][animation_data["current_frame"]]
