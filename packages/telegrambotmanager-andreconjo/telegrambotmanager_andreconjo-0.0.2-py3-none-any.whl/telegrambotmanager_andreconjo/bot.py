import telegrambotmanager_andreconjo.config as config

bot = config.setup_bot()
keys = config.setup_keys_and_reply()


@bot.message_handler()
def reply(message):
    data = next(filter(lambda key: message.text in key[0], keys), False)
    if data:
        bot.reply_to(message, data[1])


def start():
    print('Iniciado com sucesso!')
    bot.infinity_polling()
