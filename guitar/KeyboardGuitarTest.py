from pynput.keyboard import Key, Listener
import threading

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

fret: float = 1

def g_fret(): 
    return fret

def set_fret(n): 
    global fret
    fret = n

def on_press(key):
    try:
        if key.char in fret_mods:
            set_fret(fret_mods.get(key.char))
            print("Pressed on frets", key, g_fret())
    except:
        pass

def on_release(key):
    try:
        print("Released", key, fret_mods.get(key.char))
        if key.char in fret_mods:
            set_fret(1)
        if key == Key.esc:
            # Stop listener
            return False

    except:
        pass

# Collect events until released
listener_thread = threading.Thread(
    target=Listener(
        on_press=on_press, 
        on_release=on_release
    ).start()
)
listener_thread.start()

if __name__ == "__main__":
    listener_thread.join()

