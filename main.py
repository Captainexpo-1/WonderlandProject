import flask
import playsound

app = flask.Flask(__name__)

@app.route("/drums/<drum>")
def drums_bass(drum):
    playsound.playsound(drum + ".mp3", False)
    return "success"

app.run("0.0.0.0", 5000)

del player
midi.quit()