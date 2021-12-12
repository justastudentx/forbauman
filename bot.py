import logging
import bot_db
import aiohttp
import asyncio
import async_timeout
from bs4 import BeautifulSoup
from telethon import TelegramClient, events
import datetime
from fpdf import FPDF
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

api_id = 2880033
api_hash = 'b243e497652c02395449fe582477aba2'
bot_token = '2017696690:AAFiPHB_IUt8xKFIAsKjQhiliszwpYvRBFs'

db = bot_db.Db()
db.create()
# data_cal = {} # to create hash

client = TelegramClient('bot_ryan', api_id, api_hash)


async def get_calories(text):
    massive_of_answers = text.split("#")
    result = await check_gender(massive_of_answers[1])
    if result:
        calories = None
        if 'm' in massive_of_answers[1]:
            calories = 10*int(massive_of_answers[3]) + 6.25*int(massive_of_answers[2])-5*int(massive_of_answers[0])+5
        elif 'f' in massive_of_answers[1]:
            calories = 10*int(massive_of_answers[3]) + 6.25*int(massive_of_answers[2])-5*int(massive_of_answers[0])-165
        return "Ваша норма "+str(calories) + " каллорий в день"
    return False

    # url = 'https://www.calculator.net/calorie-calculator.html?ctype=metric&cage='+massive_of_answers[0]+'&csex='+massive_of_answers[1]+'&cheightfeet=5&cheightinch=10&cpound=165&cheightmeter='+massive_of_answers[2]+'&ckg='+massive_of_answers[3]+'&cactivity=1&cmop=0&coutunit=c&cformula=m&cfatpct=20&printit=0&x=16&y=13'
    # print(url)
    # response = await fetch(url)
    # print(response)
    # result = await get_req(response)



@client.on(events.NewMessage)
async def my_event_handler(event):
    if '/start' == event.raw_text:
        await client.send_message(event.chat_id,"Нажмите 1 для предложения времени сна\nНажмите 2 для подсчета каллорий")
        if await db.check(event.chat_id)==False:
            await db.insert(event.chat_id,"Нажмите 1 для предложения времени сна\nНажмите 2 для подсчета каллорий","")
        else:
            await db.update(event.chat_id,"Нажмите 1 для предложения времени сна\nНажмите 2 для подсчета каллорий","")
            # delete 34 line

    elif await db.check(event.chat_id)!=False:
        previous = (await db.check(event.chat_id))[1]

        if  "Нажмите 1 для предложения времени сна\nНажмите 2 для подсчета каллорий" in previous:
            if event.raw_text == "1":
                await db.update(event.chat_id,"В какое время вам нужно быть на работе/университете?","")
                await event.reply('''
                В какое время вам нужно быть на работе/университете?
                \n(Пример ответа: 8:30)
                ''')
            elif event.raw_text=="2":
                # await second_option(event.chat_id)
                await db.update(event.chat_id,"Введите свой возраст","")
                await event.reply("Введите свой возраст(лет)\nПример : 20")
            else:
                 await event.reply("Введите в правильном формате как указано в примере")
                 await db.update(event.chat_id,
                 '''
                 Нажмите 1 для предложения времени сна\nНажмите 2 для подсчета каллорий
                 '''
                 ,""
                 )
                 await client.send_message(event.chat_id,"Нажмите 1 для предложения времени сна\nНажмите 2 для подсчета каллорий")


        elif "Введите свой возраст" in previous:

            text_db = event.raw_text
            if await check(text_db):
                await db.update(event.chat_id,"Укажите пол",text_db+"#")
                await event.reply("Укажите пол (если мужчина введите m, если женщина f)")
            else:
                await event.reply("Введите в правильном формате как указано в примере")
                await db.update(event.chat_id,
                '''
                Нажмите 1 для предложения времени сна\nНажмите 2 для подсчета каллорий
                '''
                ,""
                )
                await client.send_message(event.chat_id,"Нажмите 1 для предложения времени сна\nНажмите 2 для подсчета каллорий")

        elif "Укажите пол" in previous:
            text_db = event.raw_text
            res_answer_gender = await check_gender(text_db)
            if res_answer_gender!=False:
                result_db = (await db.check(event.chat_id))[2]
                await db.update(event.chat_id,"Укажите свой рост",result_db+text_db+"#")
                await event.reply("Укажите свой рост(см)\nПример : 180")
            else:
                await db.update(event.chat_id,
                '''
                Нажмите 1 для предложения времени сна\nНажмите 2 для подсчета каллорий
                '''
                ,""
                )
                await event.reply("Введите в правильном формате как указано в примере")
                await client.send_message(event.chat_id,"Нажмите 1 для предложения времени сна\nНажмите 2 для подсчета каллорий")

        elif "Укажите свой рост" in previous:
            text_db = event.raw_text
            if await check(text_db):
                result_db = (await db.check(event.chat_id))[2]
                await db.update(event.chat_id,"Укажите свой вес",result_db+text_db+"#")
                await event.reply("Укажите свой вес(кг)\nПример : 70")

            else:
                await event.reply("Введите в правильном формате как указано в примере")
                await db.update(event.chat_id,
                '''
                Нажмите 1 для предложения времени сна\nНажмите 2 для подсчета каллорий
                '''
                ,""
                )
                await client.send_message(event.chat_id,"Нажмите 1 для предложения времени сна\nНажмите 2 для подсчета каллорий")

        elif "Укажите свой вес" in previous:
            text_db = event.raw_text
            if await check(text_db):
                result_db = (await db.check(event.chat_id))[2]
                await db.update(event.chat_id,
                '''
                Нажмите 1 для предложения времени сна\nНажмите 2 для подсчета каллорий
                '''
                ,""
                )
                result_text = await get_calories(result_db+event.raw_text)
                if result_text!=False:
                    await event.reply(result_text)
                    await client.send_message(event.chat_id,"Нажмите 1 для предложения времени сна\nНажмите 2 для подсчета каллорий")
                else:
                    await event.reply("Введите в правильном формате как указано в примере")
                    await db.update(event.chat_id,
                    '''
                    Нажмите 1 для предложения времени сна\nНажмите 2 для подсчета каллорий
                    '''
                    ,""
                    )
                    await client.send_message(event.chat_id,"Нажмите 1 для предложения времени сна\nНажмите 2 для подсчета каллорий")

            else:
                await event.reply("Введите в правильном формате как указано в примере")
                await db.update(event.chat_id,
                '''
                Нажмите 1 для предложения времени сна\nНажмите 2 для подсчета каллорий
                '''
                ,""
                )
                await client.send_message(event.chat_id,"Нажмите 1 для предложения времени сна\nНажмите 2 для подсчета каллорий")

        elif "В какое время вам нужно быть на работе/университете?" in previous :
            convert = await check_time(event.raw_text)

            if convert:
                await db.update(event.chat_id,
                '''
                Как долго вам добираться до пункта назначения?
                '''
                ,event.raw_text)
                await event.reply('''
                Как долго вам добираться до пункта назначения?
                \n(Пример ответа в минутах : 40 мин)
                ''')
            else:
                await event.reply("Введите в правильном формате как указано в примере")
                await db.update(event.chat_id,
                '''
                Нажмите 1 для предложения времени сна\nНажмите 2 для подсчета каллорий
                '''
                ,""
                )
                await client.send_message(event.chat_id,"Нажмите 1 для предложения времени сна\nНажмите 2 для подсчета каллорий")

        elif "Как долго вам добираться до пункта назначения?" in previous:
            convert = await check(event.raw_text)
            if convert:
                result = await db.check(event.chat_id)
                result = result[2]
                await db.update(event.chat_id,
                '''
                Сколько времени вам надо приготовится после того как вы встали?
                '''
                ,(result +" "+ event.raw_text)
                )
                await event.reply('''
                Сколько времени вам надо приготовится после того как вы встали?
                \n(Пример ответа в минутах : 40 мин)
                ''')
            else:
                await event.reply("Введите в правильном формате как указано в примере")
                await db.update(event.chat_id,
                '''
                Нажмите 1 для предложения времени сна\nНажмите 2 для подсчета каллорий
                '''
                ,""
                )
                await client.send_message(event.chat_id,"Нажмите 1 для предложения времени сна\nНажмите 2 для подсчета каллорий")

        elif "Сколько времени вам надо приготовится после того как вы встали?" in previous:
            convert = await check(event.raw_text)
            if convert:
                result_answer_new = await result_answer(event.chat_id,event.raw_text)
                await event.reply(result_answer_new)
                await client.send_message(event.chat_id,"Хотите узнать погоду?\nПример ответа: Да\нет")
                await db.update(event.chat_id,
                '''
                Хотите узнать погоду?
                '''
                ,result_answer_new
                )
            else:
                await event.reply("Введите в правильном формате как указано в примере")
                await db.update(event.chat_id,
                '''
                Нажмите 1 для предложения времени сна\nНажмите 2 для подсчета каллорий
                '''
                ,""
                )
                await client.send_message(event.chat_id,"Нажмите 1 для предложения времени сна\nНажмите 2 для подсчета каллорий")

        elif "Хотите узнать погоду?" in previous:
            if "Да" in event.raw_text or "да" in event.raw_text or "yes" in event.raw_text or "Yes" in event.raw_text:
                response = await fetch("https://pogoda.mail.ru/prognoz/moskva/")
                weather = await extract_text(response)
                await event.reply(weather)
            await client.send_message(event.chat_id,"Хотите pdf файл с рекомендованным временем для сна ?\nПример ответа: Да\нет")
            await db.update(event.chat_id,
            '''
            Хотите pdf файл с рекомендованным временем для сна ?
            '''
            ,(await db.check(event.chat_id))[2]
            )
        elif "Хотите pdf файл с рекомендованным временем для сна ?" in previous:
            if "Да" in event.raw_text or "да" in event.raw_text or "yes" in event.raw_text or "Yes" in event.raw_text:
                text = (await db.check(event.chat_id))[2]
                await pdf_file(text)
                await client.send_file(event.chat_id,"dreams.pdf")
            await db.update(event.chat_id,
            '''
            Нажмите 1 для предложения времени сна\nНажмите 2 для подсчета каллорий
            '''
            ,""
            )
            await client.send_message(event.chat_id,"Нажмите 1 для предложения времени сна\nНажмите 2 для подсчета каллорий")

async def pdf_file(text):
    pdf = FPDF()
    pdf.add_font("DejaVuSans", "", "font/DejaVuSans.ttf", uni=True)
    pdf.add_page()
    pdf.set_font('DejaVuSans', '', 14)
    pdf.cell(200, 10, txt = text,
             ln = 1, align = 'C')
    pdf.output("dreams.pdf")

async def check_time(user_time):

    try:
        if len(user_time.split(":")[1])==2:
            datetime_object = datetime.datetime.strptime(user_time, '%H:%M')
            return True
        return False
    except Exception as e:
        return False


async def result_answer(id,answer_user):
    row = await db.check(id)
    print(row)
    result_text = (row[2] +" "+answer_user).split(" ")

    needed_time = int(result_text[1])+int(result_text[2])

    d1 = datetime.datetime.strptime(result_text[0], "%H:%M")
    d2 = datetime.datetime.strptime("06:00", "%H:%M")
    d3 = datetime.datetime.strptime("07:30", "%H:%M")
    d4 = datetime.datetime.strptime("09:00", "%H:%M")
    d5 = datetime.timedelta(minutes = needed_time)
    result = "Рекомендованное время для сна : " + str(d1-d2-d5).split('day,')[-1]+", "+str(d1-d3-d5).split('day,')[-1]+", "+str(d1-d4-d5).split('day,')[-1]
    return result

async def check(answer):
    try:
        respond = int(answer)
        if respond>0:
            return True
    except Exception as e:
        return False

async def check_gender(answer):
    if answer == "f" or answer == "m" or answer == "F" or answer == "M":
        return True
    return False

#
async def fetch(url):
 async with aiohttp.ClientSession() as session:
     async with async_timeout.timeout(20):
         async with session.get(url) as response:
             return await response.text()

async def soup_d(html):
 soup = BeautifulSoup(html, 'html.parser')
 return soup

async def get_req(response):
 soup = BeautifulSoup(response, 'html.parser')
 return soup.find(class_='verybigtext').find("b").get_text()

async def extract_text(html):
 soup = await soup_d(html)
 day = soup.find(class_='day__temperature').get_text().replace("\t","").split("\n")
 result = "Днём "+ day[0] + "\nВечером "+day[1]
 return result


client.start()
client.run_until_disconnected()
