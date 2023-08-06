def setup_config_file(file):
    import telegrambotmanager_andreconjo.config as config
    config.ini_config = file

def start_bot():
    import telegrambotmanager_andreconjo.bot as bot
    bot.start();