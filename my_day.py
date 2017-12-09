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
    card_title = 'Message in a Bottle'
    text = 'Hi Anna! How are you doing?'
    prompt = 'You can ask to record a message, hear a random message, or check your inbox.'
    return question(text).reprompt(prompt).simple_card(card_title, text)


@app.route('/hear/random')
def view_method():
     path_to_file = "recordings/nicktest2.mp3"
     return send_file(path_to_file, mimetype="audio/mp3", as_attachment=True, attachment_filename='random.mp3')


@ask.intent('BrowseRandomIntent')
def listen_to_random():
    speech = "Nick from Munich says,"
    stream_url = 'https://d6143fb0.ngrok.io/hear/random'
    return audio(speech).play(stream_url)


# 'ask audio_skil Play the sax
@ask.intent('CheckMessagesIntent')
def check_messages():
    speech = 'You have two messages, one from Samantha and one from Nick.'
    return statement(speech)


@ask.intent('RecordMessageIntent')
def record_message():
    speech = '<speak>Starting recording.  How was your day?   <break time="3s"/> </speak>'
    return question(speech)


@ask.intent('EndMessageIntent')
def end_recording():
    speech = 'Recording saved.  Would you like me to send it to the community?'
    prompt = "I didn't catch that.  Should I send your message?"
    return question(speech).reprompt(prompt)

@ask.intent('AMAZON.YesIntent')
def end_recording():
    speech = 'Recording sent.'
    return statement(speech)


@ask.intent('AMAZON.NoIntent')
def end_recording():
    speech = 'Message not sent.  Recording deleted.'
    return statement(speech)

# @ask.intent('ListenMessageIntent')
# def listen_to_(user):
#     speech = "{{user}} from Munich says,"
#     stream_url = 'https://d6143fb0.ngrok.io/hear/random'
#     return audio(speech).play(stream_url, offset=93000)
#
#
# @ask.intent('ReplyIntent')
# def reply_to_message():
#     speech = 'yeah you got it! This is an audio stream from a web server.'
#     stream_url = 'https://ia800203.us.archive.org/27/items/CarelessWhisper_435/CarelessWhisper.ogg'
#     return audio(speech).play(stream_url)


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

