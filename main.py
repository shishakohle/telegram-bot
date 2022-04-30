from TelegramBot import TelegramBot
import GuteFrageNet


def handle_message(message: dict):
    # extract first word in the message
    first_word = message['text'].split(' ', 1)[0]
    # handle the /frage command
    if first_word == "/frage" or first_word == "/frage@MaHueWG_bot":
        question = GuteFrageNet.latest_question()
        msg = "The latest question on gutefrage.net is: " + question
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
