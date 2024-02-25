from pynput.keyboard import Key, Listener
from pysine import sine
sine(frequency=440.0, duration=1.0)  # plays a 1s sine wave at 440 Hz

fret_mods = {
    'a': 2 ** (1/12),
    's': 2 ** (2/12),
    'd': 2 ** (3/12),
    'f': 2 ** (4/12),
    'g': 2 ** (5/12),
    'h': 2 ** (6/12),
    'j': 2 ** (7/12),
    'k': 2 ** (8/12),
    'l': 2 ** (9/12),
    
}
string_freqs = {
    '-': 130.81, # C3
    '[': 196.00, # G3
    ';': 293.66, # D4
    '/': 440.00, # A4
}

fret = 0
string = 0

def on_press(key):
    global fret, string
    #print('{0} pressed'.format(key))
    try:
        if key.char in string_freqs:
            string = string_freqs.get(key.char)
            #print(fret, string)
            sine(frequency=string * fret, duration=2)
        elif key.char in fret_mods:
            fret = fret_mods.get(key.char)
        print(" "*2, end="\r")
    except:
        pass

def on_release(key):
    try:
        global fret, string
        if key.char in string_freqs:
            string = 0
        else:
            fret = 0
        if key == Key.esc:
            # Stop listener
            return False
        #print(fret, string)
    except:
        pass

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()