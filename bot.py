import telebot
from motivation_generator import write_to_image


bot = telebot.TeleBot('')


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # check if text is in cyrillic
    motivation_quote = write_to_image(message.text, message)
    img = open('result.jpg', 'rb')
    bot.send_photo(message.chat.id, img)


bot.infinity_polling()