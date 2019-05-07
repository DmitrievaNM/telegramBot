import telebot

from telebot import types
from telebot.types import Message

TOKEN = '839901203:AAEIcAlfKJb39N-ddm3Pe5NEQYwyorX_Zic'

bot = telebot.TeleBot(TOKEN)

# variable for counting right answers
user_right_answ = 0
# variable for counting questions
question_num = 0

# dictionary with data for quiz
dictionary = {"question1" : "bla bla", "question2" : "qqq", "question3" : "fff"}

# functions for replying
ready_markup = types.ReplyKeyboardMarkup()
start_button = 'I am ready!'
ready_markup.row(start_button)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Hello! This is a bot for checking your English level \n\n You will receive list of questions. \n\n If you are ready push Start button', reply_markup=ready_markup)


# data for questions
markup = types.ReplyKeyboardMarkup()
question1 = "Choose right answer: \n \n Q1: Tom _________ English"
answ1_1 = 'is'
answ1_2 = 'am'
answ1_3 = 'are'
answ1_4 = 'be'
markup.row(answ1_1, answ1_2)
markup.row(answ1_3, answ1_4)
    

# question sending function 
for key in dictionary.items():
        @bot.message_handler(content_types=['text'])
        def send_question(message):
                #if 'I am ready!' in message.text:
                bot.reply_to(message, key, reply_markup=markup)
     
# markup = types.ReplyKeyboardRemove(selective=False)





bot.polling()

        



