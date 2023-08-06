import telegrambotmanager_andreconjo.config as config

bot = config.setup_bot()
keys = config.setup_keys_and_replys();

@bot.message_handler()
def reply_about_churras(message):
    tuple = next(filter(lambda key: message.text in key[0], keys), False)
    if tuple:
	    bot.reply_to(message, tuple[1])


def start():
    print('Iniciado com sucesso!')
    bot.infinity_polling()
    