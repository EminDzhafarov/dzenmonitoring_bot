<H1>DzenMonitoring_bot </H1>
DzenMonitoring - is a Telegram bot for receiving daily mentions of a topic of interest to you in Russian news. The bot collects Dzen.ru titles and links and generates the csv table. May be useful for media monitoring in the press office. 

<h2>Install dependencies</H2>

<code>pip3 install -r requirements.txt</code>

<a href="https://skolo.online/documents/webscrapping/#step-3-test-installation">Install Google Chrome and ChromeDriver on your VPS</a>

<h2>Setup Bot</h2>

Create settings.py with your token from @BotFather:

<code>API_TOKEN = 'Your token'
THEME = 'News topic'
CHAT_ID = 'Telegram chat id'
HOUR = 0
MIN = 0 #ex: use 7 not 07
</code>

You can get chat id in Telegram web version. Add -100 before the code from the link

https://web.telegram.org/k/#- !your_chat_id!

Start bot with:

<code>python3 main.py</code>
