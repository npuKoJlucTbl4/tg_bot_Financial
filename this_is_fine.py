import telebot
import time
from math import pow
from math import ceil
from telebot import types


token = "7073589577:AAFNOOEwsC6K6CFdaeKBHojUX4RtxAAP2fY"        #https://t.me/MrMonopolyManBot
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("/calcs")
    markup.add(button1)
    button1 = types.KeyboardButton("/games")
    markup.add(button1)
    bot.send_message(message.chat.id,"Привет! Какими услугами желаешь воспользоваться? Они все абсолютно бесплатны, хо-хо!", reply_markup=markup)


@bot.message_handler(commands=['games'])
def games_message_reply(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1=types.KeyboardButton("52 недели богатства")
    markup.add(button1)
    bot.send_message(message.chat.id, 'Замечательно! Во что же тебе хотелось бы сыграть?', reply_markup=markup)


@bot.message_handler(commands=['calcs'])
def games_message_reply(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Кредиты")
    markup.add(button1)
    button2 = types.KeyboardButton("Вклады")
    markup.add(button2)
    bot.send_message(message.chat.id, 'И что же тебе нужно? Помогу вычислить все что нужно!', reply_markup=markup)


def repeat(message):
    bot.register_next_step_handler(message, fifty_two_days)
def repeat_vkl(message):
    bot.register_next_step_handler(message, vklad)
def repeat_cred(message):
    bot.register_next_step_handler(message, cred)
def repeat_cred_dosrok(message):
    bot.register_next_step_handler(message, cred_dosrok)

def vklad (message):
    input = str.split(message.text)
    if len(input) != 3:
        bot.send_message(message.chat.id, "Пожалуйста, напиши срок, ставку и сумму.")
        repeat_vkl(message)
        return
    elif str.isdigit(input[0]) and str.isdigit(input[1]) and str.isdigit(input[2]) is False:
        bot.send_message(message.chat.id, "Отправь мне, пожалуйста, только цифры.")
        repeat_vkl(message)
        return
    for unit in range(len(input)):
        input[unit] = int(input[unit])
    result = input[2]*input[1]/100*input[0]/365
    bot.send_message(message.chat.id, "За " + str(input[0]) + " дней ты заработаешь ≈" + str(result) + "₽")

def fifty_two_days(message):
    value = message.text
    final_sum = 0
    result = ""
    if str.isdigit(value) is True:
        value = int(value)
    else:
        bot.send_message(message.chat.id, "Ты отправил мне не число. Мне буквы складывать что-ли? Давай-ка заново.")
        repeat(message)
        return
    curr_day = int(time.asctime()[8:10])
    curr_month = time.asctime()[4:7]
    match curr_month:
        case "Jan":
            curr_month = 1
        case "Feb":
            curr_month = 2
        case "Mar":
            curr_month = 3
        case "Apr":
            curr_month = 4
        case "May":
            curr_month = 5
        case "Jun":
            curr_month = 6
        case "Jul":
            curr_month = 7
        case "Aug":
            curr_month = 8
        case "Sep":
            curr_month = 9
        case "Oct":
            curr_month = 10
        case "Nov":
            curr_month = 11
        case "Dec":
            curr_month = 12
    for week in range(52):
        curr_day += 7
        if curr_day>30:
            curr_day%=30
            curr_month+=1
            if curr_month == 13:
                curr_month = 1
        result += "Дата: "+str(curr_day)+"/"+str(curr_month)+" | Вклад: "+str(value*(week+1))+"\n"
        final_sum += value*(week+1)
    result += "Итого будет накоплено: " + str(final_sum)
    bot.send_message(message.chat.id, result)
    return


def cred_dosrok(message):
    input = str.split(message.text)
    if len(input) != 3:
        bot.send_message(message.chat.id, "Пожалуйста, напиши сумму, ставку (годовую) и срок кредитования (в месяцах).")
        repeat_cred_dosrok(message)
        return
    elif str.isdigit(input[0]) and str.isdigit(input[1]) and str.isdigit(input[2]) is False:
        bot.send_message(message.chat.id, "Отправь мне, пожалуйста, только цифры.")
        repeat_cred_dosrok(message)
        return
    for unit in range(len(input)):
        if unit != 1:
            input[unit] = int(input[unit])
        else:
            input[unit] = float(input[unit])
    input[1]=input[1]/(100*12)
    result = input[0]*(input[1]/(1-pow(1+input[1],-input[2])))
    overpay = (result*input[2])-input[0]
    bot.send_message(message.chat.id, "Тебе нужно выплачивать "+str(ceil(result))+" каждый месяц, по итогу переплата по процентам составит "+str(ceil(overpay)))


def cred(message):
    input = str.split(message.text)
    if len(input) != 3:
        bot.send_message(message.chat.id, "Пожалуйста, напиши сумму, ставку (годовую) и срок кредитования (в месяцах).")
        repeat_cred(message)
        return
    elif str.isdigit(input[0]) and str.isdigit(input[1]) and str.isdigit(input[2]) is False:
        bot.send_message(message.chat.id, "Отправь мне, пожалуйста, только цифры.")
        repeat_cred(message)
        return
    for unit in range(len(input)):
        if unit != 1:
            input[unit] = int(input[unit])
        else:
            input[unit] = float(input[unit])
    input[1] = input[1] / (100*12)
    start_sum = input[0]
    for month in range(input[2]):
        input[0]+=input[0]*input[1]
    bot.send_message(message.chat.id, "По итогу в конце срока будет долг "+str(ceil(input[0]))+", переплата составит " + str(ceil(input[0]-start_sum)))


@bot.message_handler(content_types=['text'])
def message_reply(message):
    match message.text:
        case "52 недели богатства":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton("Начать")
            markup.add(button1)
            button2 = types.KeyboardButton("Об игре")
            markup.add(button2)
            bot.send_message(message.chat.id, "Это конечно не Монополия, но все равно интересная игра! Ну что, начнем?", reply_markup=markup)
        case "Начать":
            bot.send_message(message.chat.id, "Хорошо! Напиши мне сумму, а я проведу все расчеты за тебя. Только помни, что деньги откладывать будешь именно ты!")
            bot.register_next_step_handler(message, fifty_two_days)
        case "Об игре":
            bot.send_message(message.chat.id, "В этой игре, ты должен откладывать некоторую сумму денег в течении 52 недель, но каждый раз ты должен прибавлять к этой сумме столько, сколько отложил в первую неделю")
        case "Вклады":
            bot.send_message(message.chat.id, "Прекрасно! Напиши мне срок(в днях), ставку и сумму вклада")
            bot.register_next_step_handler(message, vklad)
        case "Кредиты":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton("Досрочное погашение")
            markup.add(button1)
            button2 = types.KeyboardButton("Погашение")
            markup.add(button2)
            bot.send_message(message.chat.id, "Хорошо, сейчас разберемся. Выбери сначала способ погашения.", reply_markup=markup)
        case "Досрочное погашение":
            bot.send_message(message.chat.id, "Хорошо, тогда напиши мне сумму займа, ставку, срок кредитования (в месяцах)")
            bot.register_next_step_handler(message, cred_dosrok)
        case "Погашение":
            bot.send_message(message.chat.id, "Хорошо, тогда напиши мне сумму займа, ставку, срок кредитования (в месяцах)")
            bot.register_next_step_handler(message, cred)
bot.infinity_polling()
