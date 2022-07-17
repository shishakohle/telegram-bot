# For these imports, install as:
# pip install --upgrade py-dateutil pytz gTTS pydub pytube
# sudo apt-get install ffmpeg

from TelegramBot import TelegramBot
import GuteFrageNet
import requests
import json
import datetime
import dateutil.parser
import pytz
from gtts import gTTS
from pydub import AudioSegment
import re
from pytube import YouTube

text2speech = gTTS


def frage(bot: TelegramBot, textmessage: dict):
    # handle the /frage command
    question = GuteFrageNet.latest_question()
    filepath_mp3 = './question_audio.mp3'
    filepath_ogg = './question_audio.ogg'
    text2speech(text=question, lang='de', slow=False).save(filepath_mp3)
    AudioSegment.from_mp3(filepath_mp3).export(filepath_ogg, format="ogg")
    bot.telegram_query(
        method="sendVoice",
        args={
            'chat_id': textmessage['chat']['id'],
            'caption': question,
            'parse_mode': "Markdown"
        },
        files={
            'voice': filepath_ogg
        }
    )


def weather(bot: TelegramBot, textmessage: dict):
    words = textmessage['text'].split(' ')
    parameters = words[1:]
    locations = {
        'Vienna': {'latitude': "48.2085", 'longitude': "16.3725"},
        'Ottenöd': {'latitude': "48.5806", 'longitude': "13.2418"}
    }
    if not parameters:  # no parameters provided
        bot.telegram_query("sendMessage", {'chat_id': textmessage['chat']['id'],
                                                 'text': "Please provide a location along this command, like:\n`/weather <location>`",
                                                 'parse_mode': "Markdown"})
        return
    location = parameters[0]
    if location not in locations:
        msg = "Sorry, I've no weather forecast for `" + parameters[0] + "`.\n\n"
        msg += "I could provide you with forecasts for:"
        for location in locations.keys():
            msg += "\n- `" + location + "`"
        bot.telegram_query("sendMessage",
                                 {'chat_id': textmessage['chat']['id'], 'text': msg, 'parse_mode': "Markdown"})
        return
    coordinates = locations[location]
    url = "https://api.open-meteo.com/v1/forecast?latitude=" \
          + coordinates['latitude'] + "&longitude=" + coordinates['longitude'] \
          + "&hourly=temperature_2m,precipitation&current_weather=true&timezone=Europe%2FBerlin"
    try:
        request = requests.get(url)
    except requests.exceptions.RequestException as e:
        bot.telegram_query("sendMessage", {'chat_id': textmessage['chat']['id'],
                                                 'text': "Sorry, my request for weather data failed. Try again later."})
    else:
        request.close()
        response = json.loads(request.text)
        msg = "Currently " + str(response['current_weather']['temperature']) + " °C in " + location + ".\n\n"
        msg += "Temperature and precipitation expected:"
        timestamps = response['hourly']['time']
        temperatures = response['hourly']['temperature_2m']
        precipitations = response['hourly']['precipitation']
        counter = 1
        for i in range(0, len(timestamps)):
            timezone_europeBerlin = pytz.timezone("Europe/Berlin")
            date = timezone_europeBerlin.localize(dateutil.parser.parse(timestamps[i]))
            current = datetime.datetime.now(timezone_europeBerlin)
            if date > current and counter <= 12:
                msg += "\n0" if date.hour < 10 else "\n"
                msg += str(date.hour) + (" am: " if date.hour < 12 else " pm: ") + str(
                    temperatures[i]) + " °C, " + str(precipitations[i]) + " mm"
                counter += 1
        msg += "\n\n[Weather data by Open-Meteo.com](https://open-meteo.com/)\nunder [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)."
        bot.telegram_query("sendMessage",
                                 {'chat_id': textmessage['chat']['id'], 'text': msg, 'parse_mode': "Markdown"})


def play(bot: TelegramBot, textmessage: dict):
    # handle the command /play
    words = textmessage['text'].split(' ')
    parameters = words[1:]
    if not parameters:  # no parameters provided
        bot.telegram_query("sendMessage", {'chat_id': textmessage['chat']['id'],
                                                 'text': "Please provide a song to search for along this command, like:\n`/play Michael Jackson Dirty Diana`",
                                                 'parse_mode': "Markdown"})
        return
    song_query = '+'.join(parameter for parameter in parameters)
    response = requests.get('https://www.youtube.com/results?search_query=' + song_query).text
    video_ids = re.findall(r"watch\?v=(\S{11})", response)
    yt = YouTube("https://www.youtube.com/watch?v=" + video_ids[0])
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path="./yt_audios")
    path_thumbnail = './yt_audios/thumbnail.jpg'
    response = requests.get(yt.thumbnail_url)
    with open(path_thumbnail, "wb") as thumbnail:
        thumbnail.write(response.content)
    bot.telegram_query(
        method="sendAudio",
        args={
            'chat_id': textmessage['chat']['id'],
            'title': yt.title,
        },
        files={
            'audio': str(out_file),
            'thumb': path_thumbnail
        }
    )


def tts_de(bot: TelegramBot, textmessage: dict):
    # handle the command /tts_de
    words = textmessage['text'].split(' ')
    parameters = words[1:]
    if not parameters:  # no parameters provided
        bot.telegram_query("sendMessage", {'chat_id': textmessage['chat']['id'],
                                                 'text': "Please provide some text to be voiced along this command, like:\n`/tts_de Dieser Text wird vorgelesen.`",
                                                 'parse_mode': "Markdown"})
        return
    text = ' '.join(parameter for parameter in parameters)
    filepath_mp3 = './tts_de.mp3'
    filepath_ogg = './tts_de.ogg'
    text2speech(text=text, lang='de', slow=False).save(filepath_mp3)
    AudioSegment.from_mp3(filepath_mp3).export(filepath_ogg, format="ogg")
    bot.telegram_query(
        method="sendVoice",
        args={
            'chat_id': textmessage['chat']['id'],
            # 'caption': text,
            # 'parse_mode': "Markdown"
            },
        files={
            'voice': filepath_ogg
        }
    )
