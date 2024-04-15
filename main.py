import cv2
import telebot
import requests
import cv2 as cv
import numpy as np

with open("API_TOKEN.txt", "r") as f:
    API_TOKEN = f.read()
bot = telebot.TeleBot(API_TOKEN)

markup = telebot.types.ReplyKeyboardMarkup(selective=False)
item_code = telebot.types.KeyboardButton("Закодувати")
item_decode = telebot.types.KeyboardButton("Декодувати")
markup.row(item_code, item_decode)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup.selective = True
    bot.send_message(chat_id=message.chat.id,
                     text="""
                     Привіт, цей бот написаний для закодування чорно-білого зображення як Watermark для іншого.
                     \nТакож декодування зображення для отримання подібного Watermark.
                     \nВиберіть функцію:
                     """,
                     reply_markup=markup)


@bot.message_handler(commands=['Декодувати'])
def send_welcome(message):
    bot.send_message(chat_id=message.chat.id,
                     text=""" Надішліть фотографію, що буде закодовано """,
                     reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(content_types=['photo'])
def handle_image(message):
    # Get the file ID of the photo
    file_id = message.photo[-1].file_id

    # Get the file path using the file ID
    img_info = bot.get_file(file_id)
    img_path = img_info.file_path

    # Download the image
    image_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{img_path}"
    response = requests.get(image_url)
    pre_img = np.frombuffer(response.content, dtype=np.uint8)
    img = cv2.imdecode(pre_img, cv.IMREAD_UNCHANGED)
    cv.imshow("test", img)
    k = cv.waitKey(0)

    # Reply to the user
    bot.reply_to(message, "Зображення збережено.")


if __name__ == "__main__":
    bot.polling()
