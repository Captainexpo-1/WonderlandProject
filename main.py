from bleak import BleakClient
import flask
import playsound

app = flask.Flask(__name__)

midi.init()
player = midi.Output(0)
player.set_instrument(25)

notes_playing = {}

@app.route("/drums/<drum>")
def drums_bass(drum):
    playsound.playsound(drum + ".mp3", False)
    return "success"

def kbd_bt_callback(sender: str, data: bytearray):
    for instruction in data.split(0):
        if len(instruction) < 2:
            continue
        if instruction.startswith(1): # start playing a tone
            notes_playing[instruction[1]] = 0 if len(instruction) == 2 else int.from_bytes(instruction[2:], byteorder="big", signed=False)
            player.note_on(notes_playing[instruction[1]])
        else: # ends playing a note
            player.note_off(notes_playing[instruction[1]])
            del notes_playing[instruction[1]]

def kbd_bt_main(address):
    with BleakClient(address) as client:
        if not client.is_connected():
            while not client.connect():
                time.sleep(250)
        client.start_notify(address, kbd_bt_callback)

kbd_address = "XX:XX:XX:XX:XX:XX"

threading.Thread(
    target=kbd_bt_main,
    args=(kbd_address,)
)

app.run("0.0.0.0", 5000)

del player
midi.quit()
