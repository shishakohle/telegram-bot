#!/usr/bin/env python3

from TelegramBot import TelegramBot
import command_handlers


mahue_bot = TelegramBot("MaHueWG_bot", "./token.txt", "./telegram-bot.log")

mahue_bot.register_command_handler('frage'  , command_handlers.frage  )
mahue_bot.register_command_handler('weather', command_handlers.weather)
mahue_bot.register_command_handler('play'   , command_handlers.play   )
mahue_bot.register_command_handler('tts_de' , command_handlers.tts_de )

mahue_bot.start()
