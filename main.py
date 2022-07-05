#!/usr/bin/env python3

from TelegramBot import TelegramBot
import GuteFrageNet
import requests
import json
import datetime
import dateutil.parser
import pytz
# For these imports, install as:
# pip install --upgrade py-dateutil pytz


def handle_message(message: dict):
    # check if message has a key 'text' (messages that indicates bot has been added to new channel does not have a text)
    if 'text' in message:
        # seperate message/command into single ordered words
        words = message['text'].split(' ')
        command = words[0]
        parameters = words[1:]
        # handle the /frage command
        if command == "/frage" or command == "/frage@MaHueWG_bot":
            question = GuteFrageNet.latest_question()
            msg = "The latest question on gutefrage.net is:\n\n" + question
            mahue_bot.telegram_query("sendMessage", {'chat_id': message['chat']['id'], 'text': msg})
        # handle the /weather command
        elif command == "/weather" or command == "/weather@MaHueWG_bot":
            locations = {
                'Vienna':  {'latitude': "48.2085", 'longitude': "16.3725"},
                'Ottenöd': {'latitude': "48.5806", 'longitude': "13.2418"}
                }
            if not parameters:  # no parameters provided
                mahue_bot.telegram_query("sendMessage", {'chat_id': message['chat']['id'], 'text': "Please provide a location along this command, like:\n`/weather <location>`", 'parse_mode': "Markdown"})
                return
            elif parameters[0] not in locations:
                msg  = "Sorry, I've no weather forecast for " + parameters[0] + ".\n\n"
                msg += "I could provide you with forecasts for:"
                for location in locations.keys():
                    msg += "\n- `" + location + "`"
                mahue_bot.telegram_query("sendMessage", {'chat_id': message['chat']['id'], 'text': msg, 'parse_mode': "Markdown"})
                return
            else:
                location = parameters[0]
                coordinates = locations[location]
            url = "https://api.open-meteo.com/v1/forecast?latitude="\
                  + coordinates['latitude'] + "&longitude=" + coordinates['longitude'] \
                  + "&hourly=temperature_2m,precipitation&current_weather=true&timezone=Europe%2FBerlin"
            try:
                request = requests.get(url)
            except requests.exceptions.RequestException as e:
                mahue_bot.telegram_query("sendMessage", {'chat_id': message['chat']['id'], 'text': "Sorry, my request for weather data failed. Try again later."})
            else:
                request.close()
                response = json.loads(request.text)
                msg  = "Currently " + str(response['current_weather']['temperature']) + " °C in " + location + ".\n\n"
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
                        msg += str(date.hour) + (" am: " if date.hour < 12 else " pm: ") + str(temperatures[i]) + " °C, " + str(precipitations[i]) + " mm"
                        counter += 1
                msg += "\n\n[Weather data by Open-Meteo.com](https://open-meteo.com/)\nunder [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)."
                mahue_bot.telegram_query("sendMessage", {'chat_id': message['chat']['id'], 'text': msg, 'parse_mode': "Markdown"})
        # unknown command
        else:
            msg = "Sorry, I don't know this command: " + command + "\n\nI know:\n/frage\n/weather"
            mahue_bot.telegram_query("sendMessage", {'chat_id': message['chat']['id'], 'text': msg})


def handle_update(update: dict):
    if 'message' in update:
        handle_message(update['message'])


mahue_bot = TelegramBot("MaHueWG_bot", "./token.txt", "./telegram-bot.log")
last_update_id = 0

while True:
    updates = mahue_bot.telegram_query("getUpdates", {'offset': last_update_id+1})
    if 'ok' in updates and updates['ok']:
        # print("Succesfully fetched updates. There is/are " + str(len(updates['result'])) + " of them.")
        if 'result' in updates:
            for update in updates['result']:
                handle_update(update)
                last_update_id = update['update_id']
