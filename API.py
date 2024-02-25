from flask import Flask, request
import guitar.FLStudioInterface as FL
import time

app = Flask(__name__)

@app.route('/drums/snare')
def snare():
    FL.send_midi_note_on(60, 127, channel=3)
    return 'Hello, Snare!'

@app.route('/drums/bass')
def bass():
    FL.send_midi_note_on(60, 127, channel=0)
    return 'Hello, Bass!'

@app.route('/drums/crash')
def crash():
    FL.send_midi_note_on(60, 127, channel=1)
    return 'Hello, Crash!'

@app.route('/drums/tom')
def tom():
    FL.send_midi_note_on(60, 127, channel=2)
    return 'Hello, Tom!'

theremin_note = [None,None]

@app.route('/theremin/on')
def theremin():
    global theremin_note
    theremin_off()
    volume = request.args.get('volume')
    pitch = request.args.get('pitch')
    pitch = FL.PitchToFLNote(float(pitch))
    # Use volume and pitch parameters lllllkkaasasdfghjjkl;'hto perform theremin actions
    FL.send_midi_note_on(pitch, int(volume), channel=5)
    theremin_note = [pitch, int(volume)]
    return 'Hello, Theremin!'
@app.route('/theremin/off')
def theremin_off():
    # Use volume and pitch parameters lllllkkaasasdfghjjkl;'hto perform theremin actions
    FL.send_midi_note_off(theremin_note[0],velocity=theremin_note[1],channel=5)
    return 'Bye, Theremin!'

if __name__ == '__main__':
    app.run()