import re
import time
import unicodedata
import mysql.connector
import telebot
import telegram

from mysql.connector import errorcode

bot = telebot.TeleBot("457208338:AAEL14z3z5eM1wKqV4Gp9Fknt5bd5zsCJjI")
global passou
global  btn
class Object(object):
    pass


user = Object()

def key_words():  # verificar se funciona com o filterString
    keywordslist = []
    query = "SELECT nome_ling FROM linguagens"
    cursor.execute(query)
    for keyword in cursor:
        keyword = str(keyword)
        keyword.rpartition("'")
        keyword = keyword[2:-3]
        keywordslist.append(keyword)
    return keywordslist

def key_words2():  # verificar se funciona com o filterString
    keywordslist2 = []
    query = "SELECT nome_mat FROM materia"
    cursor.execute(query)
    for keyword in cursor:
        keyword = str(keyword)
        keyword.rpartition("'")
        keyword = keyword[2:-3]
        print(keyword)
        keywordslist2.append(keyword)
    return keywordslist2

def filter_string(string):
    l = unicodedata.normalize('NFKD', string)
    newstring = u"".join([c for c in l if not unicodedata.combining(c)])
    substring = re.sub('[^a-zA-Z0-9 \\\]', '', newstring)

    return substring

def find_key_word(string):
    string = filter_string(string)
    string = string.split(' ')
    count = 0
    for word in string:
        count += 1
        if(word=="c"):
            word="C";
        if word in currentkeywords:
            key = string[count - 1]
            send_msg(key)
            break
        else:
            continue

def send_msg(key):
        query = "SELECT nome_mat, desc_mat, link_mat FROM materia WHERE nome_ling='{}'".format(key)
        cursor.execute(query)
        l = []
        for word in cursor:
            word=str(word)
            word=word.split("'")
            l.append(word[1])
            l.append(word[3])
            l.append(word[5])
            print(len(l))
        aux=0
      #  bot.send_message(user.id,"Oque voce deseja aprender hoje?\n")
      #  while aux< len(l):
      #      word = str(l[aux])
    #        aux+=3
     #       bot.send_message(user.id,word)
        while aux< len(l):
            word = str(l[aux])
            word2=str(l[aux+1])
            word3=str(l[aux+2])
            aux+=3
            bot.send_message(user.id, "Nome da matéria:"+word+"\n e a descricao é:"+word2+"\n e o link é:"+word3)
            print('materia enviada!')

@bot.message_handler(commands=['teste'])
def btn(message):
        msg = "Hello!\n"
        msg += "What would you like to do?\n\n"
        msg += "/support - Opens a new support ticket\n"
        msg += "/settings - Settings of your account\n\n"

        main_menu_keyboard = [[telegram.KeyboardButton('/support')],
                              [telegram.KeyboardButton('/settings')]]
        reply_kb_markup = telegram.ReplyKeyboardMarkup(main_menu_keyboard,
                                                       resize_keyboard=True,
                                                       one_time_keyboard=True)

        bot.send_message(chat_id=message.chat_id,
                         text=msg,
                         reply_markup=reply_kb_markup)

@bot.message_handler(commands=['search.'])
def send_search(message):
    user.id = message.from_user.id
    handler=str(message.text)
    handler=handler.split('.')
    hand=handler[1]
    hand = hand[1:-1]+hand[-1]
    print(hand)
    if hand in currentkeywords2:
        print("aki")
        key = hand
        query = "SELECT nome_mat, desc_mat, link_mat FROM materia WHERE nome_mat='{}'".format(key)
        cursor.execute(query)
        l = []
        for word in cursor:
            word = str(word)
            word = word.split("'")
            l.append(word[1])
            l.append(word[3])
            l.append(word[5])
            print(len(l))
        aux = 0
        while aux < len(l):
            word = str(l[aux])
            word2 = str(l[aux + 1])
            word3 = str(l[aux + 2])
            aux += 3
            bot.send_message(user.id,
                                "Nome da matéria:" + word + "\n e a descricao é:" + word2 + "\n e o link é:" + word3)
            print('materia enviada!')
    else:
        bot.send_message(user.id,"Nao foi encontrado nenhuma matéria com EXATAMENTE esse nome." )

@bot.message_handler(commands=['start'])
def send_start(message):
    global passou
    user.first_name = message.from_user.first_name
    user.id = message.from_user.id
    print("{} conectou.".format(user.first_name))

    bot.send_message(user.id, ('Saudações: ' + user.first_name + '!' + '\n\nBem vindo ao '
                                                                                                   'HelperBot,  '
                                                                                                   'nesta janela voce  '
                                                                                                   'tera toda ajuda em  '
                                                                                                   'progamacao que '
                                                                                                   'precisar!!'
                                                                                                   'para mais inf /help'))
    if passou:
        time.sleep(2)
        bot.send_message(user.id, 'Já que voce é novo aki la vai, eu o HelperBot quero ajudar voe a estura, mas para isso'
                                  'voce prescisa me falar qual matéria voce quer estudar, e depois se quer estudar por '
                                  'video ou texto. Escolhendo as etapas anteriores voce pode escolher qual matéria se'
                                  'encaixa melhor no seu aprendizado.')
        passou = False


@bot.message_handler(commands=['help'])
def send_help(message):
    user.first_name = message.from_user.first_name
    user.id = message.from_user.id
    bot.send_message(user.id, 'Nao sabe oque fazer ' + user.first_name + '?'"\n\n sem problemas, aki no HelperBot as"
                                                                         "Coisas funcionam assim:"
                                                                         "\n1-Escolha a linguagem"
                                                                         "\n2-Escolha texto ou video"
                                                                         "\n3-Escolha a matéria."
                                                                         "\n E caso queira voltar /back"
                                                                         "\n Existe tambem o /search.exemplo para pesquisar")

@bot.message_handler(commands=['back'])
def send_help(message):
    user.first_name = message.from_user.first_name
    user.id = message.from_user.id



@bot.message_handler(func=lambda message: True)
def all_mesages(message):
        user.first_name = message.from_user.first_name
        user.id = message.from_user.id
        message = str(message)
        message = message.lower()
        find_key_word(message)
        print("achou")

try:
    cnx = mysql.connector.connect(user='root', database='helpperbot')
    print('successfully connected with the database')
    cursor = cnx.cursor()
    currentkeywords = key_words()
    currentkeywords2 = key_words2()
    passou = True
    bot.polling()



except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cnx.close()
