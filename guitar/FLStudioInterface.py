import mido
import time
import math

# Name of your virtual MIDI port, adjust as needed
midi_port_name = "IAC Driver Guitar"
p = mido.open_output(midi_port_name)



def PitchToFLNote(pitch: float):
    """pitch is frequency of note"""
    
    # get the midi note number
    note = 69 + 12 * math.log2(pitch / 440)
    return int(note)

# Function to send a MIDI note
def send_midi_note_on(note, velocity, port=p, channel=-1):
    if channel != -1:
        on = mido.Message('note_on', note=int(note), velocity=int(velocity), channel=channel)
    else:
        on = mido.Message('note_on', note=int(note), velocity=int(velocity))
    port.send(on)

def send_midi_note_off(note,port=p,velocity=127,channel=-1):
    if channel != -1:
        off = mido.Message('note_off', note=int(note), velocity=int(velocity), channel=int(channel))
    else:
        off = mido.Message('note_off', note=int(note), velocity=int(velocity))
    port.send(off)


def main():
    # Send a note on message
    send_midi_note_on(60, 127)