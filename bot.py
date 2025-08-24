# -*- coding: utf-8 -*-
import json
from openai.error import APIError
from translatepy.translators.google import GoogleTranslate
from datetime import datetime
import telebot
import openai
from apikey import apikeys

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

summ = 300
bot = telebot.TeleBot("5734414480:AAFai7zkBrThR7l89OTLRkosc7lO5FqJivo")
model_id = 'gpt-3.5-turbo'
autorizeaccount = 0  # счётчик

try:
    # база на JSON
    data = {}  # База данных
    date = {}  # дата


    def update_data():
        global data
        try:
            with open('db.json', 'r', encoding='utf-8') as file:  # Заполнение данных в переменную
                d1 = json.load(file)
                data.update(d1)  # Обновление данных
        except json.decoder.JSONDecodeError:
            pass


    def write_data():
        open('db.json', 'w').close()
        with open('db.json', 'w', encoding='utf-8') as file:  # Выгрузка данных в txt файл
            json.dump(data, file, indent=3, ensure_ascii=False)


    def addInDb(message):
        update_data()
        if str(message.from_user.id) in data.keys():
            pass
        else:
            data[str(message.from_user.id)] = {"id": message.from_user.id, "nick": message.from_user.username,
                                               "символы": 5000, "last message": "", "translate": False,
                                               "premium": False, "оплата": "", "дата оплаты": "", "admin": False,
                                               "adminpoints": ""}
        write_data()


    def update_date():
        global data
        try:
            with open('date.json', 'r', encoding='utf-8') as file:  # Заполнение данных в переменную
                d1 = json.load(file)
                date.update(d1)  # Обновление данных
        except json.decoder.JSONDecodeError:
            pass


    def write_date():
        open('date.json', 'w').close()
        with open('date.json', 'w', encoding='utf-8') as file:  # Выгрузка данных в txt файл
            json.dump(date, file, indent=3, ensure_ascii=False)


    ###############

    def UpdateSymbolAll():
        update_date()
        if ((datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d') - datetime.strptime(date["date"],
                                                                                                    '%Y-%m-%d')).days >= 1):
            update_data()
            for key in data:
                update_data()
                data[key]["символы"] = 5000
                write_data()
            update_date()
            date["date"] = datetime.now().strftime('%Y-%m-%d')
            write_date()
            print("Обновлено кол-во символов у всех участников")


    def GenerateLinkPay(message):
        payment_link = ""
        update_data()
        data[str(message.from_user.id)]["оплата"] = payment_link
        write_data()
        return payment_link


    def murkup_menu():
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton("❓ Как пользоваться", callback_data=f"help"),
                   InlineKeyboardButton("🈚 Переводчик", callback_data=f"translate"),
                   # InlineKeyboardButton("🗣️ Реферальная ссылка", callback_data=f""),
                   InlineKeyboardButton("💴 Premium", callback_data=f"premium"),
                   InlineKeyboardButton("☎️Contact With Support", url='https://t.me/andryhalyvaa')
                   )
        return markup


    def murkup_pay():
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton("💵 Оплатить", callback_data="pay"),
                   # InlineKeyboardButton("✅ Проверить оплату", callback_data=f"check_pay"),
                   InlineKeyboardButton("⬅️Назад", callback_data=f"back")
                   )
        return markup


    def murkup_translate():
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton("Включить", callback_data=f"translate_on"),
                   InlineKeyboardButton("Выключить", callback_data=f"translate_off"),
                   InlineKeyboardButton("⬅️Назад", callback_data=f"back")
                   )
        return markup


    def Translate_SetStatus(message, status):
        update_data()
        data[str(message.from_user.id)]["translate"] = status
        write_data()


    def TranslatorText(text, lang):
        translator = GoogleTranslate()
        result = translator.translate(text, lang)
        return result.result


    def InfoAccount(message):
        update_data()
        translate = ""
        premium = ""
        if (data[str(message.from_user.id)]["translate"]):
            translate = "✅ Включен"
        else:
            translate = "❗️Выключен❗️"

        if (data[str(message.from_user.id)]["premium"]):
            premium = "💎Премиум💎"
            dataoffprem = 30 - (datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d') - datetime.strptime(
                data[str(message.from_user.id)]["дата оплаты"], '%Y-%m-%d')).days
            return f'🔹Баланс: {data[str(message.from_user.id)]["символы"]}\n🔹Переводчик: {translate}\n🔹Premium: {premium}\n📅 Истекает через {dataoffprem} дня(й)\n🔹Языковая модель: {model_id}'
        else:
            premium = "Отсутствует"
            return f'🔹Баланс: {data[str(message.from_user.id)]["символы"]}\n🔹Переводчик: {translate}\n🔹Premium: {premium}\n🔹Языковая модель: {model_id}'


    ################
    text_pay = "💎Премиум💎\n-Безлимитный объем запросов на месяц\n-Отсутствие рекламы\n-Отсутствие задержки между запросами\nОплата доступна в течение 40 минут."
    text_noSymbols = "🚫 У вас недостаточно символов\n🆓 Ваш ежедневный лимит составляет: 5000 символов\n✅ Хотите больше? Приобретите 💎Премиум💎, подробнее /pay"
    text_paylink = "💰Премиум стоит 250 рублей на 30 дней, перевод на карту Сбер: 4276320016315088 или Киви: +79125725880. После оплаты скиньте точную дату или квитанцию мне по адресу: @andryhalyvaa"
    text_manual = '''
    Для получения логичных и правильных ответов от ChatGPT рекомендуется следовать нескольким простым советам:

    Сформулируйте свой вопрос четко и ясно, используя корректную грамматику и пунктуацию. Это поможет ChatGPT понять ваш запрос и дать более точный и полезный ответ.

    Постарайтесь сформулировать свой вопрос таким образом, чтобы он был конкретным и точным. Вместо того, чтобы задавать общий вопрос, уточните, что вас интересует или что вы хотите узнать.

    Используйте ключевые слова, чтобы помочь ChatGPT понять, что именно вы ищете. Это может быть название конкретного продукта, термин или фраза, связанные с вашим вопросом.

    Если у вас есть дополнительная информация, которую следует учесть при ответе на вопрос, укажите ее. Это может быть контекст вопроса, ваши предпочтения или ограничения, которые нужно учесть при ответе.

    Постарайтесь задать только один вопрос за раз. Если у вас есть несколько вопросов, разбейте их на несколько запросов. Это поможет ChatGPT сосредоточиться на каждом вопросе и дать наиболее точный ответ.

    Если вы не уверены в правильности ответа или хотите уточнить что-то, задавайте дополнительные вопросы. ChatGPT готов ответить на дополнительные запросы и обеспечить максимально точный и полезный ответ.

    Наконец, будьте вежливы и уважительны в своих запросах. ChatGPT - это инструмент, который разработан, чтобы помочь вам, и мы должны обращаться к нему с уважением.

    '''


    ##########

    def GetIdByUserNick(message, user_name):
        user_id = 0
        update_data()
        for key in data:
            if data[key]["nick"] == user_name:
                return data[key]["id"]
        send_message(message, "❌ Такого пользователя нет в боте")
        return 0


    def ChatGPT(message):
        global autorizeaccount
        if len(apikeys) == 0:
            for key in data:
                if data[key]["admin"]:
                    bot.send_message(data[key]["id"],
                                     "🆙 Внимание закончились ключи OpenAI!!! свяжитесь с разработчиком @rincoder")
            return "🚸 Ведуться технические работы, попробуйте позже"

        elif len(apikeys) == autorizeaccount:
            autorizeaccount = 0
        try:
            openai.api_key = apikeys[autorizeaccount]
            print(f"{autorizeaccount} | {apikeys[autorizeaccount]}")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # The name of the OpenAI chatbot model to use
                messages=[{"role": "user", "content": message}],
                # The conversation history up to this point, as a list of dictionaries
                max_tokens=3800,  # The maximum number of tokens (words or subwords) in the generated response
                stop=None,  # The stopping sequence for the generated response, if any (not used here)
                temperature=0.7,  # The "creativity" of the generated response (higher temperature = more creative)
            )
            autorizeaccount += 1
            return response["choices"][0]["message"]["content"]
        except APIError as e:
            try:
                if e.status_code == 429:
                    del apikeys[autorizeaccount]
                    return "🚫 Произошла ошибка ответа на сервере OpenAI, вомзожно сейчас мы обрабатываем большое кол-во сообщений, попробуйте позже"
                else:
                    bot.send_message(5438856320, f"⬛ Произошла ошибка в боте, текст ошибки:\n\n{e}")
            except Exception as e:
                bot.send_message(5438856320, f"⬛ Произошла ошибка в боте, текст ошибки:\n\n{e}")


    def send_message(message, text):
        bot.send_message(message.from_user.id, text)


    def send_message_reply(message, text, markup):
        bot.send_message(message.from_user.id, text, reply_markup=markup)


    @bot.message_handler(commands=["start"])
    def start_command_handler(message):
        UpdateSymbolAll()
        send_message(message, f'Привет, {message.from_user.first_name}!')
        addInDb(message)
        send_message(message,
                     f'ChatGPT - Это нейросеть, который используется для генерации текста.\n\nИспользовать бота можно для множества целей: он поможет вам в написании курсовой или сочинения, напишет стихотворение и ответит на интересующие Вас вопросы.\nНажмите на /menu чтобы получить больше информации')
        update_data()
        data[str(message.from_user.id)]["last message"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        write_data()


    # Меню
    @bot.message_handler(commands=["menu"])
    def menu_command_handler(message):
        addInDb(message)
        UpdateSymbolAll()
        send_message_reply(message, InfoAccount(message), murkup_menu())


    # обработка кнопок меню
    @bot.callback_query_handler(func=lambda call: True)  # работа на ответы с кнопками
    def callback_query(call):
        addInDb(call)
        UpdateSymbolAll()
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("⬅️Назад", callback_data=f"back"))
        if call.data == "help":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"Полный мануал о том, как пользоваться chatGPT: {text_manual}",
                                  reply_markup=markup)
        elif call.data == "translate":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Перевод включен: запрос переводится на английский, а ответ на язык запроса.\n(Минимальный расход монет, наилучшая генерация текста, наивысшая скорость ответа, возможны ошибки перевода)\n\nПереводчик выключен (по умолчанию): ни запрос, ни ответ не изменяются.\n(Высокий расход монет, медленная генерация, сохранение рифмы и использование имен/названий языка запроса)",
                                  reply_markup=murkup_translate())
        elif call.data == "premium":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text_pay,
                                  reply_markup=murkup_pay())
        elif call.data == "translate_on":
            Translate_SetStatus(call, True)
            bot.answer_callback_query(call.id, text="Перевод включен")
        elif call.data == "translate_off":
            Translate_SetStatus(call, False)
            bot.answer_callback_query(call.id, text="Перевод выключен")
        elif call.data == "pay":
            send_message(call, text_paylink)

        elif call.data == "back":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=InfoAccount(call), reply_markup=murkup_menu())


    @bot.message_handler(commands=["manual"])
    def manual_command_handler(message):
        addInDb(message)
        UpdateSymbolAll()
        send_message(message, f'Полный мануал о том, как пользоваться chatGPT: ')


    @bot.message_handler(commands=["balance"])
    def manual_command_handler(message):
        addInDb(message)
        update_data()
        UpdateSymbolAll()
        send_message(message,
                     f'Ваш баланс составляет {data[str(message.from_user.id)]["символы"]} монет. Баланс обновляется ежедневно в полночь.\n\nYour balance is {data[str(message.from_user.id)]["символы"]} coins. The balance is updated daily at midnight')


    @bot.message_handler(commands=["pay"])
    def payMessage(message):
        addInDb(message)
        send_message_reply(message, text_pay, murkup_pay())


    @bot.message_handler(commands=["ahelp"])
    def ahelp(message):
        addInDb(message)
        update_data()
        UpdateSymbolAll()
        if data[str(message.from_user.id)]["admin"]:
            send_message(message,
                         "💎Список админских команд💎\n/ahelp - Список админских команд\n/addadmin @имяпользователя - добавление админа\n/astats @имяпользователя - получить статистику пользователя\n/all текстсообщения - рассылка всем пользователям\n/addbalance @имяпользователя кол-во - выдача баланса пользователю\n/addprem @имяпользователя - выдача премиума пользователю\n/ainfo - получить кол-во пользователей")


    @bot.message_handler(content_types=['text'])
    def Chats(message):
        UpdateSymbolAll()
        bot.send_chat_action(message.chat.id, 'typing')
        update_data()
        addInDb(message)
        if str(message.from_user.id) in data.keys():
            if data[str(message.from_user.id)]["admin"] and message.text[:2] == "/a":
                try:
                    command = message.text.replace("@", "").split()
                    if command[0] == "/addadmin" and GetIdByUserNick(message, command[1]) != 0:
                        update_data()
                        data[str(GetIdByUserNick(message, command[1]))]["admin"] = True
                        write_data()
                        send_message(message, f"🅰️ @{command[1]} стал администратором")
                    elif command[0] == "/astats":
                        update_data()
                        id = str(GetIdByUserNick(message, command[1]))
                        send_message(message,
                                     f"----Статистика пользователя----\n✅ Имя пользователя: @{data[id]['nick']}\n🔢 Символы: {data[id]['символы']}\n🈚 Переводчик: {data[id]['translate']}\n💎 Премиум: {data[id]['premium']}\n🔗 Ссылка оплаты: {data[id]['оплата']}\n📅 Дата оплаты: {data[id]['дата оплаты']}\n🅰️ Админка: {data[id]['admin']}\n")
                    elif command[0] == "/all" and len(command[1]) > 0:
                        texts = message.text[4:]
                        update_data()
                        try:
                            for key in data:
                                bot.send_message(key, texts)
                        except:
                            pass
                        send_message(message, "🔔 Сообщение разослано всем пользователям")
                    elif command[0] == "/addbalance":
                        update_data()
                        data[str(GetIdByUserNick(message, command[1]))]["символы"] = \
                        data[str(GetIdByUserNick(message, command[1]))]["символы"] + int(command[2])
                        write_data()
                        send_message(message, f"💰 Символы успешно добавлены на аккаунт @{command[1]}")
                    elif command[0] == "/addprem":
                        update_data()
                        id = str(GetIdByUserNick(message, command[1]))
                        data[id]["premium"] = True
                        data[id]["дата оплаты"] = datetime.now().strftime('%Y-%m-%d')
                        data[id]["оплата"] = f"Добавлено администратором @{message.from_user.username}"
                        write_data()
                        send_message(message, f"💎 Премиум успешно выдан на аккаунт @{command[1]}")
                        bot.send_message(id,
                                         f"🔔 Вам выдан статус 💎Премиум💎 на 30 дней администратором @{message.from_user.username}")
                    elif command[0] == "/ainfo":
                        update_data()
                        keys = data.keys()
                        send_message(message, f"🚹 Кол-во пользователей: {len(keys)}")
                except Exception as e:
                    send_message(message, f"❌ Вы не указали один из параметров\n{e}")
            else:
                addInDb(message)
                update_data()
                print(f'{data[str(message.from_user.id)]["last message"]}')
                if data[str(message.from_user.id)]["last message"] != "" and ((datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S') - datetime.strptime(data[str(message.from_user.id)]["last message"], '%Y-%m-%d %H:%M:%S')).seconds >= 10 or (datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S') - datetime.strptime(data[str(message.from_user.id)]["last message"],'%Y-%m-%d %H:%M:%S')).seconds >= 5):
                    if data[str(message.from_user.id)]["premium"] and (data[str(message.from_user.id)]["оплата"] != "Отсутствует" and data[str(message.from_user.id)]["оплата"] != "" and data[str(message.from_user.id)]["premium"] and data[str(message.from_user.id)]["дата оплаты"] != "" and (datetime.strptime(datetime.now().strftime('%Y-%m-%d'),'%Y-%m-%d') - datetime.strptime(data[str(message.from_user.id)]["дата оплаты"], '%Y-%m-%d')).days >= 30):
                        data[str(message.from_user.id)]["premium"] = False
                        data[str(message.from_user.id)]["оплата"] = "Отсутствует"
                        write_data()
                        send_message(message,"🆓 У вас закончился Premium, вам доступно 5000 символов каждый день\n💎 Или можете приобрести 💎Premium💎 /pay")
                    if (data[str(message.from_user.id)]["translate"]):
                        eng = TranslatorText(message.text, "en")
                        update_data()
                        bot.send_chat_action(message.chat.id, 'typing')
                        if (data[str(message.from_user.id)]["символы"] - len(eng) >= 0 or
                                data[str(message.from_user.id)]["premium"]):
                            chatGPT = (ChatGPT(eng))
                            ru = TranslatorText(chatGPT, 'ru')
                            bot.send_chat_action(message.chat.id, 'typing')
                            send_message(message, ru)
                            update_data()
                            data[str(message.from_user.id)]["символы"] = data[str(message.from_user.id)][
                                                                             "символы"] - len(eng)
                            write_data()
                        else:
                            send_message(message, text_noSymbols)
                    else:
                        bot.send_chat_action(message.chat.id, 'typing')
                        update_data()
                        if (data[str(message.from_user.id)]["символы"] - len(message.text) >= 0 or
                                data[str(message.from_user.id)]["premium"]):
                            send_message(message, ChatGPT(message.text))
                            update_data()
                            bot.send_chat_action(message.chat.id, 'typing')
                            data[str(message.from_user.id)]["символы"] = data[str(message.from_user.id)]["символы"] - len(message.text)
                            write_data()
                        else:
                            send_message(message, text_noSymbols)
                    update_data()
                    data[str(message.from_user.id)]["last message"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    write_data()
                else:
                    addInDb(message)
                    update_data()
                    if data[str(message.from_user.id)]["last message"] != "":
                        if data[str(message.from_user.id)]["premium"]:
                            send_message(message,f"⌚ Подождите ещё {5 - ((datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') - datetime.strptime(data[str(message.from_user.id)]['last message'], '%Y-%m-%d %H:%M:%S')).seconds)}c")
                        else:
                            send_message(message,
                                         f"⌚ Подождите ещё {10 - ((datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') - datetime.strptime(data[str(message.from_user.id)]['last message'], '%Y-%m-%d %H:%M:%S')).seconds)}c\n💎С Premium время ожидания уменьшено с 10с до 5с, приобрести /pay")
                    else:
                        data[str(message.from_user.id)]["last message"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        send_message(message, f"⌚ Подождите немного перед отправкой следующего сообщения, если у вас часто вылазит данное сообщение напишите команду /start")


except Exception as e:
    bot.send_message(5438856320, f"⬛ Произошла ошибка в боте, текст ошибки:\n\n{e}")
print("Бот запущен")

try:
    bot.polling(none_stop=True, timeout=50)
except Exception as e:
    bot = telebot.TeleBot("5992027379:AAFrfF4nSAEJc5Ttx_Noci8Zsf0S-WTVbzM")
    bot.send_message(5438856320, f"⬛ Произошла ошибка в боте, текст ошибки:\n\n{e}")
    bot.polling(none_stop=False, timeout=50)