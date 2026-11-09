import vlc
import time
from flask import Flask, redirect, render_template, url_for
from os import listdir
from os.path import isfile, join

VIDEO_PATH = "./videos/"

# VLC States
# 0: Nothing Special
# 1: Opening
# 2: Buffering
# 3: Playing
# 4: Paused
# 5: Stopped
# 6: Ended
# 7: Error


#--------------- Flask Setup -------------------

app = Flask(__name__)

files = [f for f in listdir(VIDEO_PATH) if isfile(join(VIDEO_PATH, f))]
sources = {}

for file in files:
    sources[file.rsplit(".", 1)[0]] = file

playing = [1,2,3,4]

@app.route("/")
def index():
    state = player.get_state()
    print("State: ", state)

    if player.get_state() not in playing: # if nothing playing/paused
        player.play_item_at_index(0)
    print("Sources:", sources)
    print(sources.keys())
    return render_template("index.html",
                           state=state, 
                           chapter=player.get_media_player().get_chapter(),
                           chapter_counter=player.get_media_player().get_chapter_count(),
                           time=player.get_media_player().get_time(),
                           isMuted=player.get_media_player().audio_get_mute())
@app.route("/pause")
def pause():
    global player
    player.get_media_player().set_pause(1)
    return redirect("/")

@app.route("/play")
def play():
    global player
    player.get_media_player().set_pause(0)
    return redirect("/")

@app.route("/mute")
def mute():
    player.get_media_player().audio_set_mute(True)
    return redirect("/")


@app.route("/unmute")
def unmute():
    player.get_media_player().audio_set_mute(False)
    return redirect("/")

@app.route("/toggle-mute")
def toggle_mute():
    if bool(player.get_media_player().audio_get_mute()): # if already muted
        return redirect(url_for("unmute")) #unmute
    return redirect(url_for("mute")) # otherwise mute


@app.route("/next")
def next():
    player.next()
    return redirect("/")


@app.route("/previous")
def previous():
    player.previous()
    return redirect("/")

@app.route("/sources")
def source_selector():
    return render_template("sources.html", sources=sources.keys())

@app.route("/source/<source_id>")
def source(source_id):
    if source_id in sources:
        player.play_item_at_index(list(sources.keys()).index(source_id))
        player.play()
    return redirect("/")


@app.route("/seek_fw/<num_ms>")
def seek_fw(num_ms):
    if num_ms.isdigit():
        current_time = player.get_media_player().get_time()
        player.get_media_player().set_time(current_time + int(num_ms))
    return redirect("/")

@app.route("/seek_bk/<num_ms>")
def seek_bk(num_ms):
    if num_ms.isdigit():
        current_time = player.get_media_player().get_time()
        player.get_media_player().set_time(current_time - int(num_ms))
    return redirect("/")




if __name__ == "__main__":   
    #--------------- player setup ------------------
    instance = vlc.Instance('--input-repeat=-1', '--no-video-title-show', '--fullscreen', '--mouse-hide-timeout=0')

    player = instance.media_list_player_new()
    media_list = instance.media_list_new()
    for source_id in sources:
        media_list.add_media(instance.media_new(join(VIDEO_PATH, sources[source_id])))
    
    player.get_media_player().toggle_fullscreen()
    player.get_media_player().audio_set_volume(100)
    player.set_playback_mode(vlc.PlaybackMode().loop)
    player.set_media_list(media_list)
    player.play()
    print(player.get_media_player().get_xwindow())
    player.get_media_player().set_xwindow(player.get_media_player().get_xwindow())
    app.run(host="0.0.0.0")
    

