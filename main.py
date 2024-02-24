import flask
import winsound
import playsound
import pygame.midi as midi
import time
import threading

app = flask.Flask(__name__)

shift = 0
base_shift = 20
base_increment = 1
base_duration = 1

midi.init()
player = midi.Output(0)
player.set_instrument(25)


def play_tone(shift_level):
    player.note_on(base_shift + (base_increment*shift_level) + shift, 127)
    time.sleep(base_duration)
    player.note_off(base_shift + (base_increment*shift_level) + shift, 127)

def play_tone_thread(shift_level):
    threading.Thread(target=play_tone, args=(shift_level,)).start()

@app.route("/keyboard/tone_shift/<shift>")
def keyboard_tone_shift(new_shift):
    global shift
    shift = new_shift

@app.route("/simon/red")
def simon_red():
    play_tone(0)
    return "success"

@app.route("/simon/green")
def simon_green():
    play_tone(1)
    return "success"

@app.route("/simon/blue")
def simon_blue():
    play_tone(2)
    return "success"

@app.route("/simon/yellow")
def simon_yellow():
    play_tone(3)
    return "success"


@app.route("/drums/<drum>")
def drums_bass(drum):
    playsound.playsound(drum + ".mp3", False)
    return "success"

app.run("0.0.0.0", 5000)

del player
midi.quit()