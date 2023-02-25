from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import datetime
import pandas as pd
import telebot
import time
import os
from settings import *

bot = telebot.TeleBot(API_TOKEN)

df = pd.DataFrame(columns=['Заголовок', 'Ссылка'])

def getYesterday():
    """Get the date that we insert into the link"""
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = (today - oneday)
    return ''.join(str(yesterday).split('-'))

def parser():
    """The function parses the dzen.ru news page for a date before today"""
    global headings
    global links
    date = getYesterday()
    options = webdriver.ChromeOptions()
    options.add_argument('headless') #Turn on the mode without launching Chrome
    options.add_argument('--no-sandbox')
    browser = webdriver.Chrome(options=options)
    browser.get(f"https://dzen.ru/news/search?issue_tld=ru&text={THEME}+date%3A{date}")

    try:
        headings = browser.find_elements(By.CLASS_NAME, 'news-search-story__title')
        links = browser.find_elements(By.CLASS_NAME, 'news-search-story__title-link')
    except NoSuchElementException:
        pass

    for i in range(len(headings)):
        df.loc[len(df.index)] = [headings[i].text, links[i].get_attribute("href")] #Packing everything into a table

    df.to_csv('news.csv', index=False, encoding="utf-8")

while True:
    now = datetime.datetime.now()
    if now.hour == HOUR and now.minute == MIN: #Hours and minutes from settings.py
        parser()
        for i in range(len(headings)):
            bot.send_message(CHAT_ID, f'{headings[i].text}\n{links[i].get_attribute("href")}')
        bot.send_document(chat_id=CHAT_ID, document=open('news.csv', 'rb'))
        os.remove('news.csv')
        time.sleep(60) #Don't let the bot spam for a full minute



browser.quit()
bot.polling(none_stop=True)