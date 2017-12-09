import logging
import os
from os import path

from flask import Flask, json, render_template, send_file
from flask_ask import Ask, request, session, question, statement, context, audio, current_stream

app = Flask(__name__)
ask = Ask(app, "/")
logger = logging.getLogger()
logging.getLogger('flask_ask').setLevel(logging.INFO)


@ask.launch
def launch():
    card_title = 'Audio Example'
    text = 'Hi Nick and Anna! Here is the demo from a tutorial.'
    prompt = 'You can ask to begin demo, or try asking me to play the sax.'
    return question(text).reprompt(prompt).simple_card(card_title, text)


@ask.intent('DemoIntent')
def demo():
    speech = "Here's one of my favorites"
    stream_url = 'https://www.vintagecomputermusic.com/mp3/s2t9_Computer_Speech_Demonstration.mp3'
    return audio(speech).play(stream_url, offset=93000)


# 'ask audio_skil Play the sax
@ask.intent('SaxIntent')
def george_michael():
    speech = 'yeah!.'
    stream_url = 'https://d6143fb0.ngrok.io/nicktest'
    return audio(speech).play(stream_url)


@app.route('/nicktest')
def view_method():
     path_to_file = "recordings/nicktest2.mp3"

     return send_file(
         path_to_file,
         mimetype="audio/mp3",
         as_attachment=True,
         attachment_filename=path.basename(path_to_file))

@ask.intent('AMAZON.PauseIntent')
def pause():
    return audio('Paused the stream.').stop()


@ask.intent('AMAZON.ResumeIntent')
def resume():
    return audio('Resuming.').resume()

@ask.intent('AMAZON.StopIntent')
def stop():
    return audio('stopping').clear_queue(stop=True)




# optional callbacks
@ask.on_playback_started()
def started(offset, token):
    _infodump('STARTED Audio Stream at {} ms'.format(offset))
    _infodump('Stream holds the token {}'.format(token))
    _infodump('STARTED Audio stream from {}'.format(current_stream.url))


@ask.on_playback_stopped()
def stopped(offset, token):
    _infodump('STOPPED Audio Stream at {} ms'.format(offset))
    _infodump('Stream holds the token {}'.format(token))
    _infodump('Stream stopped playing from {}'.format(current_stream.url))


@ask.on_playback_nearly_finished()
def nearly_finished():
    _infodump('Stream nearly finished from {}'.format(current_stream.url))

@ask.on_playback_finished()
def stream_finished(token):
    _infodump('Playback has finished for stream with token {}'.format(token))

@ask.session_ended
def session_ended():
    return "{}", 200

def _infodump(obj, indent=2):
    msg = json.dumps(obj, indent=indent)
    logger.info(msg)


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)

