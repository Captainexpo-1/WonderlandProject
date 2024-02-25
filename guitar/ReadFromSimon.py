import serial
import time
from FLStudioInterface import send_midi_note_on, send_midi_note_off, PitchToFLNote

# kind: 0 = note_on, 1 = note_off
def parse_pitch(inp, kind):
    pitches = {
        'a': 130.81, # C3
        'b': 196.00, # G3
        'c': 293.66, # D4
        'd': 440.00, # A4
    }
    inp = inp.split(" ")
    abcd = []
    abcd.append("a" if inp[0] == "1" else "ao")
    abcd.append("b" if inp[1] == "1" else "bo")
    abcd.append("c" if inp[2] == "1" else "co")
    abcd.append("d" if inp[3] == "1" else "do")

    for s in abcd:
        if len(s) == 1:
            print(s)
            send_midi_note_on(PitchToFLNote(pitches.get(s)), 127)
        else:
            print(s)
            send_midi_note_off(PitchToFLNote(pitches.get(s[0])))
    
    




last = "0 0 0 0"
def read_from_port(port):
    global last
    while True:
        # Read a line of data from the serial port
        data = port.readline()
        # Decode data (assuming it's in UTF-8, adjust if necessary)
        decoded_data = data.decode('utf-8').rstrip()
        #print("Received:", decoded_data)
        k = 0
        if len(decoded_data) != 7:
            continue
        if decoded_data != last:
            if decoded_data == "0 0 0 0":
                k = 1
            else:
                k = 0

            parse_pitch(decoded_data, k)
            last = decoded_data

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
