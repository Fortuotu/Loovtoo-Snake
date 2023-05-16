from pygame import mixer

channels = {
    'sound_effect': 2
}

current_song = None

def play_sound_effect(path):
    sound_effect = mixer.Sound(path)
    mixer.Channel(channels['sound_effect']).play(sound_effect)

def set_song(path, force=False):
    global current_song
    if current_song != path or force:
        mixer.music.load(path)
        mixer.music.play(loops=-1)
        current_song = path

paused = False

def pause_song(force=False):
    global paused
    if not paused or force:
        mixer.music.pause()
        paused = True

def end_song():
    mixer.music.unload()

def unpause_song(force=False):
    global paused
    if paused or force:
        mixer.music.unpause()
        paused = False
