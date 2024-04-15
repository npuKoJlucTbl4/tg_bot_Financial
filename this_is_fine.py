import telebot
import time
from math import pow
from math import ceil
from telebot import types

token = "7073589577:AAFNOOEwsC6K6CFdaeKBHojUX4RtxAAP2fY"        #https://t.me/MrMonopolyManBot
bot = telebot.TeleBot(token)

input_filtered = []

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
def calcs_message_reply(message):
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
    global input_filtered
    for word in input:
        try:
            word = word.replace("%", "")
            word = word.replace("₽", "")
            word = word.replace(",", ".")
            word = float(word)
            input_filtered.append(word)
        except:
            pass
    if len(input_filtered) < 3:
        repeat_vkl(message)
        return
    for i in range(3):
        input_filtered[i] = int(input_filtered[i])
    result = input_filtered[2]*input_filtered[1]/100*input_filtered[0]/365
    bot.send_message(message.chat.id, "За " + str(input_filtered[0]) + " дней ты заработаешь ≈" + str(result) + "₽")

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
    global input_filtered
    for word in input:
        try:
            word = word.replace("%", "")
            word = word.replace("₽", "")
            word = word.replace(",",".")
            word = float(word)
            input_filtered.append(word)
        except:
            pass
    if len(input_filtered) <3:
        repeat_cred_dosrok(message)
        return
    for i in range(3):
        if i != 1:
            input_filtered[i] = int(input_filtered[i])
    input_filtered[1] = input_filtered[1] / (100 * 12)
    result = input_filtered[0] * (input_filtered[1] / (1 - pow(1 + input_filtered[1], -input_filtered[2])))
    overpay = (result * input_filtered[2]) - input_filtered[0]
    bot.send_message(message.chat.id, "Тебе нужно выплачивать " + str(
        ceil(result)) + " каждый месяц, по итогу переплата по процентам составит " + str(ceil(overpay)))
    input_filtered = []

def cred(message):
    input = str.split(message.text)
    global input_filtered
    for word in input:
        try:
            word = word.replace("%", "")
            word = word.replace("₽", "")
            word = word.replace(",",".")
            word = float(word)
            input_filtered.append(word)
        except:
            pass
    if len(input_filtered) <3:
        repeat_cred(message)
        return
    for i in range(3):
        if i != 1:
            input_filtered[i] = int(input_filtered[i])
    input_filtered[1] = input_filtered[1] / (100 * 12)
    start_sum = input_filtered[0]
    for month in range(input_filtered[2]):
        input_filtered[0] += input_filtered[0] * input_filtered[1]
    bot.send_message(message.chat.id,
                     "По итогу в конце срока будет долг " + str(ceil(input_filtered[0])) + ", переплата составит " + str(
                         ceil(input_filtered[0] - start_sum)))
    input_filtered = []

@bot.message_handler(content_types=['text'])
def main_message_reply(message):
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
            bot.send_message(message.chat.id, "Прекрасно! Напиши мне срок(в днях), годовую ставку и сумму вклада")
            bot.register_next_step_handler(message, vklad)
        case "Кредиты":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton("Досрочное погашение")
            markup.add(button1)
            button2 = types.KeyboardButton("Погашение")
            markup.add(button2)
            bot.send_message(message.chat.id, "Хорошо, сейчас разберемся. Выбери сначала способ погашения.", reply_markup=markup)
        case "Досрочное погашение":
            bot.send_message(message.chat.id, "Хорошо, тогда напиши мне сумму займа, процентную ставку и срок кредитования (в месяцах)")
            bot.register_next_step_handler(message, cred_dosrok)
        case "Погашение":
            bot.send_message(message.chat.id, "Хорошо, тогда напиши мне сумму займа, процентную ставку и срок кредитования (в месяцах)")
            bot.register_next_step_handler(message, cred)
bot.infinity_polling()