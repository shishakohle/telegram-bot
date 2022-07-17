import types

import requests
from threading import Thread


class TelegramBot:
    bot_telegram_id = None
    token = None
    filepath_log = None
    is_ready = False

    is_running = False
    command_handler = {}

    def __init__(self, bot_telegram_id, filepath_token, filepath_log):
        self.bot_telegram_id = bot_telegram_id
        self.filepath_log = filepath_log
        # load secret token for the telegram bot from file
        with open(filepath_token, "r") as file_token:
            self.token = file_token.readline().rstrip('\n')
            self.log("Loaded token from file.")
            file_token.close()
        if self.token_is_valid():
            self.log("Token is valid.")
            self.is_ready = True
        else:
            self.log("Token is NOT valid.")

    def log(self, logentry):
        print(logentry)
        with open(self.filepath_log, "a") as file_log:
            file_log.write(logentry)
            file_log.write("\n")
            file_log.close()

    def token_is_valid(self):
        botinfo = self.telegram_query("getMe")
        try:
            return botinfo and botinfo['ok'] and botinfo['result']['is_bot'] and botinfo['result']['username'] == self.bot_telegram_id
        except KeyError as e:
            return False

    def telegram_query(self, method: str, args: dict = None, files: dict = None) -> dict:
        if method != "getMe" and not self.is_ready:
            return None
        url = 'https://api.telegram.org/bot' + self.token + '/' + method
        if files:
            files_opened = {parameter: open(filepath, 'rb').read() for (parameter, filepath) in files.items()}
        else:
            files_opened = None
        try:
            response = requests.post(url, data=args, files=files_opened).json()
        except requests.exceptions.RequestException as e:
            response = None
            self.log("Query to Bot API failed.")
        return response

    def register_command_handler(self, command: str, handler: types.FunctionType):
        if command[0] != '/':
            command = '/' + command
        self.command_handler.update({command: handler})

    def start(self):
        if not self.is_running:  # prevent multiple threads to be started
            self.is_running = True
            thread = Thread(target=self.fetch_and_handle_updates)
            thread.start()

    def stop(self):
        self.is_running = False

    def fetch_and_handle_updates(self):
        last_update_id = 0
        while self.is_running:
            updates = self.telegram_query("getUpdates", {'offset': last_update_id + 1})
            if updates and 'ok' in updates and updates['ok']:
                # print("Succesfully fetched updates. There is/are " + str(len(updates['result'])) + " of them.")
                if 'result' in updates:
                    for update in updates['result']:
                        self.handle_update(update)
                        last_update_id = update['update_id']

    def handle_update(self, update: dict):
        if 'message' in update:
            self.handle_message(update['message'])

    def handle_message(self, message: dict):
        # check if message has a key 'text'
        # (messages that are e.g. a gif or e.g. indicate bot has been added to new channel do not have a key 'text')
        if 'text' in message:
            self.handle_textmessage(message)
        else:
            # TODO
            pass

    def handle_textmessage(self, textmessage: dict):
        words = textmessage['text'].split(' ')
        first_word = words[0]
        if first_word[0] == '/':
            # textmessage is a command
            command = first_word.split('@')[0]
            if command in self.command_handler:
                self.command_handler[command](self, textmessage)
            else:
                # unknown command
                msg = "Sorry, I don't know this command: `" + command + "`\n\nI know:"
                for entry in self.command_handler:
                    msg += "\n`" + entry + "`"
                self.telegram_query("sendMessage", {'chat_id': textmessage['chat']['id'], 'text': msg, 'parse_mode': "Markdown"})
        else:
            # textmessage is not a command
            # TOOD
            # textmessage.update({'text': "foo " + textmessage['text']})
            # command_handler['/tts_de'](textmessage)
            pass
