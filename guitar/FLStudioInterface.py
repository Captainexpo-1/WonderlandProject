import mido
import time
import math

# Name of your virtual MIDI port, adjust as needed
midi_port_name = "IAC Driver Bus 1"
p = mido.open_output(midi_port_name)

def PitchToFLNote(pitch: float):
    """pitch is frequency of note"""
    
    # get the midi note number
    note = 69 + 12 * math.log2(pitch / 440)
    return int(note)

# Function to send a MIDI note
def send_midi_note_on(note, velocity, port=p):
    on = mido.Message('note_on', note=note, velocity=velocity)
    port.send(on)

def send_midi_note_off(note,port=p):
    off = mido.Message('note_off', note=note, velocity=127)
    port.send(off)


def main():
    # Send a note on message
    send_midi_note_on(60, 127)