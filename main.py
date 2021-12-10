import random
import string
import time

from flask import Flask, request, abort
import markovify
import telebot
import dotenv

dotenv.load_dotenv()

from config import Config

telebot.logger.setLevel(telebot.logging.WARNING)

with open("input/result.txt", "r", encoding="utf-8") as fp:
    model = markovify.NewlineText(fp.read())

app = Flask(__name__)
app.config.from_object(Config)
bot = telebot.TeleBot(app.config["TELEGRAM_BOT_TOKEN"])

@app.route(f"/{app.config['TELEGRAM_BOT_TOKEN']}", methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)

@bot.message_handler(content_types=["text"])
def text_handler(message: telebot.types.Message):
    text_in = None
    if message.content_type == "text":
        if message.chat.type == "private":
            text_in = [x.lower() for x in message.text.split()]
        else:
            if message.text.lower().startswith("волод") or message.text.lower().startswith("вов"):
                text_in = [x.lower() for x in message.text.split()][1:]
    if text_in:
        print(message.chat.username, "->", message.text)
        try:
            sentence = model.make_sentence_with_start(random.choice([x.strip(string.punctuation) for x in text_in]), strict=False)
        except markovify.text.ParamError:
            sentence = model.make_short_sentence(300)
        bot.send_message(message.chat.id, sentence)
        print(message.chat.username, "<-", sentence)


bot.remove_webhook()
time.sleep(0.1)
bot.set_webhook("https://" + app.config["SERVER_NAME"] + f"/{app.config['TELEGRAM_BOT_TOKEN']}")
