import serial
from FLStudioInterface import send_midi_note_on, send_midi_note_off, PitchToFLNote
from KeyboardGuitarTest import g_fret
# kind: 0 = note_on, 1 = note_off

cur = {
    'a': 440,
    'b': 440,
    'c': 440,
    'd': 440
}
def parse_pitch(inp):
    #print("FRET:",g_fret())
    pitches = {
        'c': 261.6255653005986,
        'a': 391.99543598174927,
        'b': 440.0,
        'd': 587.3295358348151,
    }
    inp = inp.split(" ")
    abcd = []
    abcd.append("a" if inp[0] == "1" else "ao")
    abcd.append("b" if inp[1] == "1" else "bo")
    abcd.append("c" if inp[2] == "1" else "co")
    abcd.append("d" if inp[3] == "1" else "do")

    for s in abcd:
        if len(s) == 1:
            #print(s)
            cur[s] = pitches.get(s)*g_fret()
            send_midi_note_on(PitchToFLNote(cur[s]), 127)
        else:
            #print(s)
            send_midi_note_off(PitchToFLNote(cur[s[0]]))
    




last = "0 0 0 0"
last_fret = 1
def read_from_port(port):
    global last, last_fret
    while True:

        # Read a line of data from the serial port
        data = port.readline()
        # Decode data (assuming it's in UTF-8, adjust if necessary)
        decoded_data = data.decode('utf-8').rstrip()
        #print(decoded_data)
        #print("Received:", decoded_data)
        if len(decoded_data) != 7:
            continue
        if last_fret != g_fret():
            last_fret = g_fret()
            parse_pitch("0 0 0 0")
            last = "9 9 9 9"
            print("QUICK CHANGE!")
        if decoded_data != last:

            parse_pitch(decoded_data)
            last = decoded_data
        last_fret = g_fret()

def main():
    try:
        # Configure serial port settings
        # '/dev/tty.usbserial-110' is the port name
        # 9600 is the baud rate, adjust if your device uses a different rate
        ser = serial.Serial('/dev/tty.usbserial-110', 9600, timeout=1)

        # Call the function to continuously read data
        read_from_port(ser)

    except serial.SerialException as e:
        print("Error opening serial port: ", e)

    except KeyboardInterrupt:
        print("Exiting...")
        if ser:
            ser.close()

if __name__ == '__main__':
    main()
