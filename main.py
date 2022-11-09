import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CursConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Категорически Вас приветсвую! ' \
           '\nДля того, чтоб узнать, что там с курсом, введите следующие данные: ' \
           '\n\n1.Имя валюты, цену которой хотите узнать ' \
           '\n2.Имя валюты, в которой надо узнать цену первой валюты ' \
           '\n3.Количество первой валюты ' \
           '\n\nПРИМЕР ВВОДА: Доллар Рубль 250' \
           '\n\nCписок всех доступных валют - /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['stop'])
def bye(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'Пока-пока, другалёк! Приходи ещё!')

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.lower().split()

        if len(values) > 3:
            raise ConvertionException('Слишком много параметров')

        if len(values) < 3:
            raise ConvertionException('Слишком мало параметров')

        quote, base, amount = values
        total_base = CursConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()