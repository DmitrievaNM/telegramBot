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

        self.results = {}

    def checking_answer(self, answer, chat_id, score, question_number):
        """A function for checking right answers"""
        if answer == self.right_answers[question_number - 1]:
            score += 1
        self.results[chat_id] = (score, question_number)

QUIZ = TalkToMeQuizBot()
@BOT.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """A function for starting a conversation with the bot"""
    QUIZ.results[message.chat.id] = (QUIZ.score, QUIZ.question_number)
    ready_markup = types.ReplyKeyboardMarkup()
    start_button = 'I am ready!'
    ready_markup.row(start_button)
    BOT.send_message(message.chat.id, HELLO_STRING, reply_markup=ready_markup)


@BOT.message_handler(content_types=['text'])
def send_question(message):
    """A function for sending questions to a user"""
    chat_id = message.chat.id
    this_question_number = QUIZ.results[chat_id][1]

    QUIZ.checking_answer(message.text, chat_id, QUIZ.results[chat_id][0], this_question_number)
    if this_question_number <= len(QUIZ.questions):
        markup = types.ReplyKeyboardMarkup()
        markup.row(QUIZ.answers[this_question_number][0], QUIZ.answers[this_question_number][1])
        markup.row(QUIZ.answers[this_question_number][2], QUIZ.answers[this_question_number][3])
        BOT.send_message(chat_id, QUIZ.questions[this_question_number], reply_markup=markup)
        this_question_number += 1
        QUIZ.results[chat_id] = (QUIZ.results[chat_id][0], this_question_number)
    else:
        markup = types.ReplyKeyboardRemove(selective=False)
        BOT.send_message(message.chat.id,
                         'Your score is: ' + str(QUIZ.results[chat_id][0]) + '/3',
                         reply_markup=markup)
        QUIZ.results[chat_id] = (QUIZ.results[chat_id][0], this_question_number)

BOT.polling(none_stop=True, interval=0)
