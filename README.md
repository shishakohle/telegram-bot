# TelegramBot

Customizable Telegram chatbot as a Python Class.

## Get started
First, checkout the [Telegram documentation on creating a new bot with *@BotFather*](https://core.telegram.org/bots#6-botfather).

To get started with an implementation of a chatbot in your Python script, import as

`from TelegramBot import TelegramBot`

whilst having the `TelegramBot.py` in the same directory as your script.

Instantiate and initialize your bot with the `TelegramBot` constructor:

`myBot = TelegramBot(<username_bot>, <path_token>, <path_logfile>)`

Replace `<username_bot>` with the actual username of the bot, as determined with *@BotFather* before. *@BotFather* would also have provided you with a token as a secret key to control and run the bot. Put the token in a simple text file and replace `<path_token>` with the path of this file. Replace `<path_logfile>` with a path to a file where you want to have the log messages of `myBot` pushed to.

To enhance the bot with a command, create a Python function that takes the arguments `bot: TelegramBot` and `textmessage: dict` and register it as a command handler with the bot:

```
def handler_my_command(bot: TelegramBot, textmessage: dict):
    # TODO: Handle the command /my_command .
    pass

myBot.register_command_handler('my_command', handler_my_command)
```

Once the bot is set and ready, get it running:

`myBot.start()`

The bot then will listen for and handle any commands which it receives from Telegram users. As this process will be started in a new Python thread, you're free to do different things with your Python script after invoking `myBot.start()`. You may terminate active operation of the bot with `myBot.stop()`.

## Sample implementation
This git repository contains an example on how to implement a chatbot with *TelegramBot*:

[![@MaHueWG_bot on t.me](doc/MaHueWG_bot.png)](https://t.me/MaHueWG_bot)

Give it a try and have a chat with [@MaHueWG_bot](https://t.me/MaHueWG_bot).

It supports four commands:
* `/weather <location>` - Weather forecast for `<location>`.
* `/frage` - Latest question on *gutefrage.net* as text and audio (voice message).
* `/tts_de <text>` - Text-to-speech audio of a German `<text>`.
* `/play <artist(s) and title>` - Play a song.

`main.py` sets up and runs WG Mariahilf-Bot (@MaHueWG_bot). It references `command_handlers.py`, which covers each bot command with an appropriate handler.

Written by Ingo Weigel, April 2022 - July 2022.

Find this project on GitHub: https://github.com/shishakohle/telegram-bot
