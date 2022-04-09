from TelegramBot import TelegramBot
from time import sleep
import GuteFrageNet

mahue_bot = TelegramBot("MaHueWG_bot", "./token.txt", "./telegram-bot.log")

mahue_bot.telegram_query("getUpdates", None)

while True:
    question = GuteFrageNet.latest_question()
    msg = "The latest question on gutefrage.net is: " + question
    mahue_bot.telegram_query("sendMessage", {'chat_id': '-648065929', 'text': msg})
    sleep(3600)
