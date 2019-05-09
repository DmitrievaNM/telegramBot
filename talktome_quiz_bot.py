import telebot

from telebot import types
from telebot.types import Message

TOKEN = '839901203:AAEIcAlfKJb39N-ddm3Pe5NEQYwyorX_Zic'

bot = telebot.TeleBot(TOKEN)

# variable for counting right answers
score = 0
# variable for counting questions
question_number = 1

# dictionaries with data for quiz
questions = {   1 : "Q1: Tom _________ English", 
                2 : "Q2: _________ there a restaurant near here?", 
                3 : "Q3: I didn't _________ TV last night."}

answers = { 1 : ("is", "am", "are", "be"),
            2 : ("Have", "Is", "Do", "Are"),
            3 : ("not watched", "watched", "watch", "watching")}

right_answers = {   1 : "is",
                    2 : "Is",
                    3 : "watch"}

# functions for replying
ready_markup = types.ReplyKeyboardMarkup()
start_button = 'I am ready!'
ready_markup.row(start_button)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Hello! This is a bot for checking your English level \n\n You will receive a list of questions. \n\n If you are ready push "I am ready" button', reply_markup=ready_markup)
    

# question sending function 
@bot.message_handler(content_types=['text'])
def send_question(message):
    global question_number
    global score

    if question_number <= len(questions):
        markup = types.ReplyKeyboardMarkup()
        markup.row(answers[question_number][0], answers[question_number][1])
        markup.row(answers[question_number][2], answers[question_number][3])
        
        bot.send_message(message.chat.id, questions[question_number], reply_markup=markup)

        if message.text == right_answers[question_number]:
            score += 1

        question_number += 1
        bot.register_next_step_handler(message, send_question)
    else:
        bot.send_message(message.chat.id, 'Your score is: ' + str(score))





bot.polling()
