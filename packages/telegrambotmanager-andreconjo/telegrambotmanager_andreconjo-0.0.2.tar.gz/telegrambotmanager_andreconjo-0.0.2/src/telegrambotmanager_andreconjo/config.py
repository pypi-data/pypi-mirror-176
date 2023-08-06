import configparser

parser = configparser.ConfigParser()


def prepare_keywords(words):
    return [word.strip() for word in words.split(',')]


ini_config = ''


def setup_bot():
    config_file = open(ini_config, encoding='utf-8').read()
    parser.read_string(config_file)
    bot_token = parser[parser.default_section]['bot_token']
    import telebot
    return telebot.TeleBot(bot_token, parse_mode=None)


def setup_keys_and_reply():
    active_sections = prepare_keywords(parser[parser.default_section]['active_sections'])
    all_tuples = []
    for item in active_sections:
        all_tuples.append((prepare_keywords(parser[item]['keywords']), parser[item]['reply']))
    return all_tuples
