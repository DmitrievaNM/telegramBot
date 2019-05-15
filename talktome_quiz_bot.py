"""This script (Telegram bot) prompts a user to check his English level
 using a standard English quiz"""

import telebot
from telebot import types

TOKEN = '839901203:AAEIcAlfKJb39N-ddm3Pe5NEQYwyorX_Zic'
BOT = telebot.TeleBot(TOKEN)

HELLO_STRING = """Hello! I am a bot for checking your English level.
You will receive a list of questions.
If you are ready push "I am ready" button."""

class TalkToMeQuizBot:
    """The main class"""
    def __init__(self):
        # variable for counting right answers
        self.score = 0

        # variable for counting questions
        self.question_number = 1

        # dictionaries with data for quiz
        self.questions = {1 : "Q1: Tom _________ English",
                          2 : "Q2: _________ there a restaurant near here?",
                          3 : "Q3: I didn't _________ TV last night."}

        self.answers = {1 : ("is", "am", "are", "be"),
                        2 : ("Have", "Is", "Do", "Are"),
                        3 : ("not watched", "watched", "watch", "watching")}

        self.right_answers = {0 : "none", 1 : "is", 2 : "Is", 3 : "watch"}

QUIZ = TalkToMeQuizBot()
@BOT.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """A function for starting a conversation with the bot"""
    ready_markup = types.ReplyKeyboardMarkup()
    start_button = 'I am ready!'
    ready_markup.row(start_button)
    BOT.send_message(message.chat.id, HELLO_STRING, reply_markup=ready_markup)
    QUIZ.score = 0
    QUIZ.question_number = 1

@BOT.message_handler(content_types=['text'])
def send_question(message):
    """A function for sending questions to a user"""
    if QUIZ.question_number <= len(QUIZ.questions):
        markup = types.ReplyKeyboardMarkup()
        markup.row(QUIZ.answers[QUIZ.question_number][0], QUIZ.answers[QUIZ.question_number][1])
        markup.row(QUIZ.answers[QUIZ.question_number][2], QUIZ.answers[QUIZ.question_number][3])
        BOT.send_message(message.chat.id, QUIZ.questions[QUIZ.question_number], reply_markup=markup)
        if message.text == QUIZ.right_answers[QUIZ.question_number - 1]:
            QUIZ.score += 1
        QUIZ.question_number += 1
    else:
        if message.text == QUIZ.right_answers[QUIZ.question_number - 1]:
            QUIZ.score += 1
        markup = types.ReplyKeyboardRemove(selective=False)
        BOT.send_message(message.chat.id,
                         'Your score is: ' + str(QUIZ.score) + '/3',
                         reply_markup=markup)

BOT.polling(none_stop=True, interval=0)
