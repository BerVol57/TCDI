import requests
import telebot

from code_decode_img import *

with open("API_TOKEN.txt", "r") as f:
    API_TOKEN = f.read()
BOT = telebot.TeleBot(API_TOKEN)

markup = telebot.types.ReplyKeyboardMarkup(selective=False)
item_code = telebot.types.KeyboardButton("/Закодувати")
item_decode = telebot.types.KeyboardButton("/Декодувати")
markup.row(item_code, item_decode)

img = Image()


def reset():
    img.img = None
    img.code, img.decode, img.is_watermark = False, False, False


@BOT.message_handler(commands=['start'])
def send_welcome(message):
    reset()
    markup.selective = True
    BOT.send_message(chat_id=message.chat.id,
                     text="""
                     Привіт, цей бот написаний для закодування чорно-білого зображення як Watermark для іншого.
                     \nТакож декодування зображення для отримання подібного Watermark.
                     \nВиберіть функцію:
                     """,
                     reply_markup=markup)
    # photo_test = open("test/slime.png", "rb")
    # BOT.send_photo(chat_id=message.chat.id, photo=photo_test)
    # photo_test.close()


@BOT.message_handler(commands=['Закодувати'])
def send_welcome(message):
    BOT.send_message(chat_id=message.chat.id,
                     text=""" Надішліть фотографію, що буде закодовано: """,
                     reply_markup=telebot.types.ReplyKeyboardRemove())
    img.code = True


@BOT.message_handler(commands=['Декодувати'])
def send_welcome(message):
    BOT.send_message(chat_id=message.chat.id,
                     text=""" Надішліть фотографію для декодування: """,
                     reply_markup=telebot.types.ReplyKeyboardRemove())
    img.decode = True


@BOT.message_handler(content_types=['photo'])
def handle_image(message):
    print(img.code, img.decode, img.is_watermark)
    # Get the file ID of the photo
    file_id = message.photo[-1].file_id

    # Get the file path using the file ID
    img_info = BOT.get_file(file_id)
    img_path = img_info.file_path

    # Download the image
    image_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{img_path}"
    response = requests.get(image_url)

    if img.code:
        print("Code")
        try:
            img.set_value(response.content)
            BOT.reply_to(message, "Надішліть Watermark(чорно-біле зображення).")
            img.code = False
            img.is_watermark = True
        except Exception as e:
            BOT.send_message(chat_id=message.chat.id,
                             text=f"Помилка: {e}")

    elif img.decode:
        print("Decode")
        try:
            img.decode = False
            BOT.send_photo(chat_id=message.chat.id,
                           photo=img.get_watermark(response.content))
        except Exception as e:
            BOT.send_message(chat_id=message.chat.id,
                             text=f"Помилка: {e}")

    elif img.is_watermark:
        print("Watermark")
        try:
            # text = img.set_watermark(response.content)
            BOT.send_photo(chat_id=message.chat.id,
                           photo=img.set_watermark(response.content))
            img.is_watermark = False
        except Exception as e:
            BOT.send_message(chat_id=message.chat.id,
                             text=f"Помилка: {e}")


if __name__ == "__main__":
    BOT.polling()
