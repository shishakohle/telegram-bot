import requests
import json


class TelegramBot:
    bot_telegram_id = None
    token = None
    filepath_log = None
    is_ready = False

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

    """
    def telegram_query(self, telegram_method: str, args: dict = None) -> list:  # TODO: isn't it -> dict ??
        query = telegram_method + "?"
        if args is None:
            args = {}
        for arg, val in args.items():
            query += arg + '=' + str(val) + '&'
        # self.log("Query to Telegram Bot API: " + query)
        # TODO: https://stackoverflow.com/questions/16511337/correct-way-to-try-except-using-python-requests-module
        response = json.loads(requests.get('https://api.telegram.org/bot' + self.token + '/' + query).text)
        # self.log("Telegram Bot API responded: " + str(response))
        return response
    """
