from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import datetime
import pandas as pd
import telebot
import time
from settings import *

bot = telebot.TeleBot(API_TOKEN)

df = pd.DataFrame(columns=['Заголовок', 'Ссылка'])

def getYesterday():
    """Get a"""
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = (today - oneday)
    return ''.join(str(yesterday).split('-'))

def parser():
    """The function parses the dzen.ru news page for a date before today"""
    date = getYesterday()
    options = webdriver.ChromeOptions()
    options.add_argument('headless') #Turn on the mode without launching Chrome
    browser = webdriver.Chrome(options=options)
    browser.get(f"https://dzen.ru/news/search?issue_tld=ru&text={THEME}+date%3A{date}")

    try:
        headings = browser.find_elements(By.CLASS_NAME, 'news-search-story__title')
        links = browser.find_elements(By.CLASS_NAME, 'news-search-story__title-link')
    except NoSuchElementException:
        pass

    try:
        for i in range(100):
            df.loc[len(df.index)] = [headings[i].text, links[i].get_attribute("href")]
    except IndexError:
        pass

    browser.quit()
    df.to_csv('news.csv')

while True:
    now = datetime.datetime.now()
    if now.hour == HOUR and now.minute == MIN: #Hours and minutes from settings.py
        parser()
        bot.send_document(chat_id=CHAT_ID, document=open('news.csv', 'rb'))
        time.sleep(60) #Don't let the bot spam for a full minute

bot.polling(none_stop=True)