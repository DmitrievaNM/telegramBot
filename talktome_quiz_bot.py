"""This script (Telegram bot) prompts a user to check his English level
 using a standard English quiz"""

import json
import telebot
from telebot import types

TOKEN = '839901203:AAEIcAlfKJb39N-ddm3Pe5NEQYwyorX_Zic'
BOT = telebot.TeleBot(TOKEN)

HELLO_STRING = """Hello! I am a bot designed to help you find out at which level of English you are.

You will receive a list of 120 multiple-choice questions, 20 at each level from Starter to Advanced (covering CEFR levels A1 to C1). Choose the best answer for each question.

The first HUNDRED (100) users to send their results to @talktome_agency will receive a gift from TalkToMe Ltd.

Are you ready? Push the "I am ready" button!"""

ADVERT_STRING = """Good job!

A gift from TalkToMe Ltd is a FREE online oral test for the first HUNDRED (100) users.

An oral placement test, designed to be used in conjunction with this test, is available via the TalkToMe Ltd. service.

Send your results to @talktome_agency and we will provide you with a native speaker for an online oral test."""

class TalkToMeQuizBot:
    """The main class"""
    def __init__(self):
        # variable for counting right answers
        self.score = 0

        # variable for counting questions
        self.question_number = 1

        # dictionary with data for quiz from JSON file
        with open("quiz.json", "r") as read_file:
            self.quiz = json.load(read_file)

        self.results = {}
        self.wrong_list = {}

    def user_level(self, score):
        """Checking user level"""
        level = ""
        if 0 <= score <= 15:
            level = "Starter"
        if 15 < score <= 35:
            level = "Elementary"
        if 35 < score <= 55:
            level = "Pre-Intermediate"
        if 55 < score <= 75:
            level = "Intermediate"
        if 75 < score <= 95:
            level = "Upper Intermediate"
        if score > 95:
            level = "Advanced"
        return level

    def checking_answer(self, answer, chat_id, score, question_number):
        """A function for checking right answers"""
        if answer == self.quiz["questions"][str(int(question_number) - 1)]["right"]:
            score += 1
        else:
            question_dic = self.quiz["questions"][str(int(question_number) - 1)]
            self.wrong_list[chat_id].append("Question " + str(int(question_number)-1) + ". " +
                                            question_dic["question"] +
                                            " Right answer: " +
                                            question_dic["right"] +
                                            "\n\n")
        self.results[chat_id] = (score, question_number)

    def next_question(self, number, chat, message):
        """Sending next question from dictionary"""
        if int(number) < int(len(self.quiz["questions"])):
            markup = types.ReplyKeyboardMarkup()
            if len(self.quiz["questions"][number]) == 5:
                markup.row(self.quiz["questions"][number]["A"],
                           self.quiz["questions"][number]["B"])
                markup.row(self.quiz["questions"][number]["C"])
            else:
                if len(self.quiz["questions"][number]) == 6:
                    markup.row(self.quiz["questions"][number]["A"],
                               self.quiz["questions"][number]["B"])
                    markup.row(self.quiz["questions"][number]["C"],
                               self.quiz["questions"][number]["D"])

            BOT.send_message(chat,
                             number + ". " + self.quiz["questions"][number]["question"],
                             reply_markup=markup)
            number = int(number) + 1
            self.results[chat] = (self.results[chat][0], number)
        else:
            del self.wrong_list[chat][0]
            markup = types.ReplyKeyboardRemove(selective=False)
            BOT.send_message(message.chat.id,
                             'Your score is: ' +
                             str(self.results[chat][0]) + '/' +
                             str(len(self.quiz["questions"])-1) +
                             "\nYour level is " + self.user_level(self.results[chat][0]),
                             reply_markup=markup)
            BOT.send_message(message.chat.id, ADVERT_STRING)
            if self.wrong_list[chat]:
                BOT.send_message(message.chat.id,
                                 "This is a list of questions you answered wrong:\n\n")
                for wrong_answer in self.wrong_list[chat]:
                    BOT.send_message(message.chat.id, wrong_answer)
            self.results[chat] = (self.results[chat][0], number)

QUIZ = TalkToMeQuizBot()
@BOT.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """A function for starting a conversation with the bot"""
    QUIZ.results[message.chat.id] = (QUIZ.score, QUIZ.question_number)
    QUIZ.wrong_list[message.chat.id] = []
    ready_markup = types.ReplyKeyboardMarkup()
    start_button = 'I am ready!'
    ready_markup.row(start_button)
    BOT.send_message(message.chat.id, HELLO_STRING, reply_markup=ready_markup)


@BOT.message_handler(content_types=['text'])
def send_question(message):
    """A function for sending questions to a user"""
    chat_id = message.chat.id
    this_question_number = str(QUIZ.results[chat_id][1])

    QUIZ.checking_answer(message.text, chat_id, QUIZ.results[chat_id][0], this_question_number)
    QUIZ.next_question(this_question_number, chat_id, message)

BOT.polling(none_stop=True, interval=0)
