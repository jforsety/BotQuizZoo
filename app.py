from config import API_TOKEN
from text_bot import (text, text1, text2, text3,
                      text4, text5, text6, text7,
                      text8, text9, animals2, exit, questions, animals)
import logging
from logging.handlers import RotatingFileHandler
import telebot
from telebot import types
import time
import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Устанавливаем уровень логирования

# настроим rfl
handler = RotatingFileHandler('Logs/LogsBot.log', maxBytes=5000000, backupCount=5, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(handler)
bot = telebot.TeleBot(API_TOKEN)
logger.info("Запуск бота")


# Обрабатывается команда /help. Помощь.
@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    key3 = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Вернуться в начало🦈", callback_data='start')
    button2 = types.InlineKeyboardButton(text="К началу викторины😉", callback_data='quiz')
    key3.add(button1)
    key3.add(button2)
    bot.send_message(message.chat.id, text, reply_markup=key3)
    logger.info(f"Пользователь {message.from_user.full_name, message.from_user.username, message.from_user.id} использовал команду help.")


# Функция вывод контактов
def contacts(message):
    key4 = types.InlineKeyboardMarkup()
    but1 = types.InlineKeyboardButton(text="Спасибо❤️", callback_data='menu')
    key4.add(but1)
    bot.send_message(message.chat.id, text4, reply_markup=key4, parse_mode="HTML")
    logger.info(f"Пользователь {message.from_user.full_name, message.from_user.username, message.from_user.id} использовал команду contacts")


# Обрабатываются сообщения, содержащие команды '/start', выводится фотография, приветствие и кнопки.
@bot.message_handler(commands=["start"])
def start(message):
    animals.update({'Манул': 0,
        'Сова': 0,
        'Медведь': 0,
        'Альпака': 0,})
    key = types.InlineKeyboardMarkup()
    but_1 = (types.InlineKeyboardButton(text="Начать викторину🦈",callback_data="quiz"))
    but_2 = types.InlineKeyboardButton(text="Пока не хочу начинать🙈",callback_data="no_quiz")
    key.add(but_1)
    key.add(but_2)
    with open('Pictures/manul_on.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=text1, reply_markup=key, parse_mode="HTML")
        logger.info(f"Пользователь {message.from_user.full_name, message.from_user.username, message.from_user.id} использовал команду start")


# Функция информации о программе опеки
def info(message):
    key5 = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Вернуться к меню🦈", callback_data='menu')
    button2 = types.InlineKeyboardButton(text="Перейти на сайт и узнать больше🌎", url='https://moscowzoo.ru/my-zoo/become-a-guardian/')
    key5.add(button1)
    key5.add(button2)
    with open('Pictures/info.png', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=text2, reply_markup=key5, parse_mode="HTML")
        logger.info(f"Пользователь {message.from_user.full_name, message.from_user.username, message.from_user.id} использовал команду info")


# Функция для фитбека
def feedback(message):
    key_feedback = types.InlineKeyboardMarkup()
    but_feedback = types.InlineKeyboardButton(text="Отлично❤️", callback_data='menu')
    key_feedback.add(but_feedback)
    text = message.text
    logger.warning(f"Пользователь {message.from_user.full_name, message.from_user.username, message.from_user.id} оставил отзыв")
    with open('Feedback/feedback.txt', 'a', encoding='utf-8') as file:
        file.write(f"{datetime.datetime.now()} - Пользователь {message.from_user.full_name, message.from_user.id, message.from_user.username} оставил отзыв: {text}\n")
    bot.reply_to(message, text='Спасибо за ваш отзыв, мы обязательно станем лучше😉',reply_markup=key_feedback)
    time.sleep(0.3)
    os.system('python feedback_email.py')
    logger.warning("На почтовый ящик организации был отправлен файл с обратной связью от пользователя")


# Функция для обратной связи
def callback(message):
    key_callback = types.InlineKeyboardMarkup()
    but_callback = types.InlineKeyboardButton(text="Отлично, буду ждать звонка❤️", callback_data='menu')
    key_callback.add(but_callback)
    text = message.text
    logger.warning(f"Пользователь {message.from_user.full_name, message.from_user.username, message.from_user.id} отправил запрос на обратный звонок")
    with open('Callback/callback.txt', 'a', encoding='utf-8') as file:
        file.write(f"{datetime.datetime.now()} - Пользователь {message.from_user.full_name, message.from_user.id, message.from_user.username} отправил запрос на обратный звонок: {text}\n"
                   f"Результат викторины: {animals2}\n")
    bot.reply_to(message, text='Спасибо за ваше доверие, сотрудник свяжется с вами в ближайшее время😉',reply_markup=key_callback)
    time.sleep(0.3)
    os.system('python callback_email.py')
    logger.warning("На почтовый ящик организации был отправлен файл с обратным звонком")
    animals2.clear()


# Функция проверки неверного ввода
words_list = ['/help', '/start']
@bot.message_handler()
def check_message(message):
    message_text = message.text.lower()
    if message_text not in words_list:
        bot.delete_message(message.chat.id, message.message_id)
        logger.warning(f"Пользователь{message.from_user.full_name, message.from_user.username, message.from_user.id} ввел неверную команду или текст: {message.text}")


@bot.callback_query_handler(func=lambda c: True)
def starts(c):
    question_count = 9
    answer_count = 4
    but = list()
    keys = list()
    but_1 = types.InlineKeyboardButton(text="Начать викторину🦈", callback_data="quiz")
    but_2 = types.InlineKeyboardButton(text="Пока не хочу начинать🙈", callback_data="no_quiz")
    keys.append(types.InlineKeyboardMarkup())
    keys[0].add(but_1)
    keys[0].add(but_2)
    keys.append(types.InlineKeyboardMarkup())
    button = types.InlineKeyboardButton("Ладно, давайте начнём викторину👌", callback_data='quiz')
    keys[1].add(button)

# Объявляем кнопки вопросов
    for i in range(1, question_count+1):
        for j in range(1, answer_count+1):
            but.append(types.InlineKeyboardButton(questions[i-1][f'answer{i}{j}'], callback_data=f'answer{i}{j}'))
        keys.append(types.InlineKeyboardMarkup())
        for k in range(1, answer_count+1):
            keys[i+1].add(but[((i-1)*answer_count+k)-1])

    key11 = types.InlineKeyboardMarkup()
    but100 = types.InlineKeyboardButton('Сохранить результат', callback_data='result')
    but200 = types.InlineKeyboardButton('Поделиться ботом',url='https://vk.com/share.php?url=https://t.me/zoomoscow_bot')
    but300 = types.InlineKeyboardButton('Заказать обратный звонок📞', callback_data='callback')
    key11.add(but100)
    key11.add(but200)
    key11.add(but300)
    menu = types.InlineKeyboardMarkup()
    menu0 = types.InlineKeyboardButton('Клёво, спасибо😉', callback_data='menu')
    menu.add(menu0)
    menu1 = types.InlineKeyboardMarkup()
    menu2 = types.InlineKeyboardButton('Вернуться в начало', callback_data='start')
    menu3 = types.InlineKeyboardButton('Отзыв/Пожелание', callback_data='feedback')
    menu8 = types.InlineKeyboardButton('Контакты', callback_data='contact')
    menu4 = types.InlineKeyboardButton('Перейти на сайт🌎', url='https://moscowzoo.ru/')
    menu5 = types.InlineKeyboardButton('О программе', callback_data='info')
    menu6 = types.InlineKeyboardButton('Поделиться ботом', url='https://vk.com/share.php?url=https://t.me/zoomoscow_bot')
    menu7 = types.InlineKeyboardButton('На сегодня всё', callback_data='exit')
    menu1.add(menu2)
    menu1.add(menu3)
    menu1.add(menu8)
    menu1.add(menu4)
    menu1.add(menu5)
    menu1.add(menu6)
    menu1.add(menu7)


    # Функция выявляет победителя и выводит результат пользователю.
    def result(animals,animals2):
        max_val = max(animals.values())
        global final_animals
        final_animals = {k: v for k, v in animals.items() if v == max_val}
        for animal in final_animals:
            if animal == 'Альпака':
                with open('Pictures/alpaka.jpg', 'rb') as photo:
                    bot.send_photo(c.message.chat.id, photo, caption=text5, reply_markup=key11, parse_mode="HTML")
                    animals2.update({'Альпака': 9})
                    break
            elif animal == 'Сова':
                with open('Pictures/sova.jpeg', 'rb') as photo:
                    bot.send_photo(c.message.chat.id, photo, caption=text6, reply_markup=key11, parse_mode="HTML")
                    animals2.update({'Сова': 9})
                    break
            elif animal == 'Медведь':
                with open('Pictures/medved.jpg', 'rb') as photo:
                    bot.send_photo(c.message.chat.id, photo, caption=text7, reply_markup=key11, parse_mode="HTML")
                    animals2.update({'Медведь': 9})
                    break
            elif animal == 'Манул':
                with open('Pictures/manul_on.jpg', 'rb') as photo:
                    bot.send_photo(c.message.chat.id, photo, caption=text8, reply_markup=key11, parse_mode="HTML")
                    animals2.update({'Манул': 9})
                    break
        animals.update({'Манул': 0,
                            'Сова': 0,
                            'Медведь': 0,
                            'Альпака': 0, })
        final_animals.clear()
# Начинаем викторину
    if c.data == 'quiz':
        bot.send_message(c.message.chat.id, questions[0]['question1'], reply_markup=keys[2], parse_mode="HTML")
        logger.info(f"Пользователь {c.from_user.full_name, c.from_user.username, c.from_user.id} начал викторину.")
# Показываем вопросы и ответы пользователю
    for i in range(1, question_count):
        if c.data == f'answer{i}1':
            animals['Альпака'] += 1
            logger.info(f"Пользователь{c.from_user.username, c.from_user.id} ответил на вопрос, текущий результат: {animals}")
            bot.send_message(c.message.chat.id, questions[i][f'question{i + 1}'], reply_markup=keys[i + 2],parse_mode="HTML")
            bot.delete_message(c.message.chat.id, c.message.message_id)
            time.sleep(0.2)
        elif c.data == f'answer{i}2':
            animals['Сова'] += 1
            logger.info(f"Пользователь{c.from_user.username, c.from_user.id} ответил на вопрос, текущий результат: {animals}")
            bot.send_message(c.message.chat.id, questions[i][f'question{i + 1}'], reply_markup=keys[i + 2],parse_mode="HTML")
            bot.delete_message(c.message.chat.id, c.message.message_id)
            time.sleep(0.2)
        elif c.data == f'answer{i}3':
            animals['Медведь'] += 1
            logger.info(f"Пользователь{c.from_user.username, c.from_user.id} ответил на вопрос, текущий результат: {animals}")
            bot.send_message(c.message.chat.id, questions[i][f'question{i + 1}'], reply_markup=keys[i + 2],parse_mode="HTML")
            bot.delete_message(c.message.chat.id, c.message.message_id)
            time.sleep(0.2)
        elif c.data == f'answer{i}4':
            animals['Манул'] += 1
            logger.info(f"Пользователь{c.from_user.username, c.from_user.id} ответил на вопрос, текущий результат: {animals}")
            bot.send_message(c.message.chat.id, questions[i][f'question{i + 1}'], reply_markup=keys[i + 2],parse_mode="HTML")
            bot.delete_message(c.message.chat.id, c.message.message_id)
            time.sleep(0.2)
# Обработка последних ответов пользователя и вызов функции result
    if c.data == 'answer91':
        animals['Альпака'] += 1
        logger.info(f"Пользователь{c.from_user.username, c.from_user.id} ответил на вопрос, текущий результат: {animals}")
        bot.delete_message(c.message.chat.id, c.message.message_id)
        result(animals, animals2)
    elif c.data == 'answer92':
        animals['Сова'] += 1
        logger.info(f"Пользователь{c.from_user.username, c.from_user.id} ответил на вопрос, текущий результат: {animals}")
        bot.delete_message(c.message.chat.id, c.message.message_id)
        result(animals, animals2)
    elif c.data == 'answer93':
        animals['Медведь'] += 1
        logger.info(f"Пользователь{c.from_user.username, c.from_user.id} ответил на вопрос, текущий результат: {animals}")
        bot.delete_message(c.message.chat.id, c.message.message_id)
        result(animals, animals2)
    elif c.data == 'answer94':
        animals['Манул'] += 1
        logger.info(f"Пользователь{c.from_user.username, c.from_user.id} ответил на вопрос, текущий результат: {animals}")
        bot.delete_message(c.message.chat.id, c.message.message_id)
        result(animals, animals2)
    # Отказ от викторины
    if c.data == 'no_quiz':
        with open('Pictures/manul_off.jpg', 'rb') as photo:
            bot.send_photo(c.message.chat.id, photo, caption=text3, reply_markup=keys[1])
            logger.info(f"Пользователь {c.from_user.full_name, c.from_user.username, c.from_user.id} отказался начинать викторину.")
    # Дублирующий старт
    if c.data == 'start':
        with open('Pictures/manul_on.jpg', 'rb') as photo:
            bot.send_photo(c.message.chat.id, photo, caption=text1, reply_markup=keys[0], parse_mode="HTML")
            logger.info(f"Пользователь {c.from_user.full_name, c.from_user.username, c.from_user.id} использовал команду start")
    # Меню
    if c.data == 'menu':
        bot.send_message(c.message.chat.id, text='Хочешь сделать что-нибудь еще?😊', reply_markup=menu1, parse_mode="HTML")
    # Фидбек
    if c.data == 'feedback':
        bot.send_message(c.message.chat.id, text='Напиши свой отзыв или пожелание😊')
        bot.register_next_step_handler(c.message, feedback)
    # Обратный звонок
    if c.data == 'callback':
        bot.send_message(c.message.chat.id, text='Напиши свой номер телефона для обратного звонка😊')
        bot.register_next_step_handler(c.message, callback)
    # Информация о программе опеки
    if c.data == 'info':
        info(c.message)
    # Контакты
    if c.data == 'contact':
        contacts(c.message)
    # Выход, благодарим пользователя и прощаемся
    if c.data == 'exit':
        with open('Pictures/info.png', 'rb') as photo:
            bot.send_photo(c.message.chat.id, photo, caption=exit)
            logger.info(f"Пользователь {c.from_user.full_name, c.from_user.username, c.from_user.id} вышел")
    # Сохранить результат, выводит пользователю картинку для сохранения
    if c.data == 'result':
        logger.info(f"Пользователь ответил на вопросы и получил результат картинкой.")
        for animal in animals2:
            if animal == 'Альпака':
                with open('Pictures/Я Альпака!.jpg', 'rb') as photo:
                    bot.send_document(c.message.chat.id, photo, caption=text9, reply_markup=menu)
                    animals2.clear()
                    break
            elif animal == 'Сова':
                with open('Pictures/Я Сова!.jpeg', 'rb') as photo:
                    bot.send_document(c.message.chat.id, photo, caption=text9, reply_markup=menu)
                    animals2.clear()
                    break
            elif animal == 'Медведь':
                with open('Pictures/Я Медведь!.jpg', 'rb') as photo:
                    bot.send_document(c.message.chat.id, photo, caption=text9, reply_markup=menu)
                    animals2.clear()
                    break
            elif animal == 'Манул':
                with open('Pictures/Я Манул!.jpg', 'rb') as photo:
                    bot.send_document(c.message.chat.id, photo, caption=text9, reply_markup=menu)
                    animals2.clear()
                    break


if __name__ == '__main__':
    bot.polling(none_stop=True)
    logger.info("Завершена работа бота")
