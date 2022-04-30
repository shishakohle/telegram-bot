import requests
import json


class TelegramBot:
    bot_telegram_id = None
    token = None
    filepath_log = None

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
        return botinfo['ok'] and botinfo['result']['is_bot'] and botinfo['result']['username'] == self.bot_telegram_id

    def telegram_query(self, telegram_method: str, args: dict = None) -> list:
        query = telegram_method + "?"
        if args is None:
            args = {}
        for arg, val in args.items():
            query += arg + '=' + str(val) + '&'
        # self.log("Query to Telegram Bot API: " + query)
        response = json.loads(requests.get('https://api.telegram.org/bot' + self.token + '/' + query).text)
        # self.log("Telegram Bot API responded: " + str(response))
        return response
