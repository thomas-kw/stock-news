import requests
from twilio.rest import Client

STOCK_API_KEY = "5XINAC27YFHCXE05"
NEWS_API_KEY = "0b49acf3a1c249a0bd3c4cbeef0fbc5a"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

TWILIO_SID = "AC4bc9d655663dcdcdbee672f007fc79d9"
TWILIO_AUTH_TOKEN = "go to twilio website"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [price for (date, price) in data.items()]  # list  comprehension: value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)

up_down = None
if difference > 0:
    up_down = "UP"
else:
    up_down = "DOWN"

diff_percent = round((difference / float(yesterday_closing_price)) * 100)

if abs(diff_percent) > 2:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,

    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

three_articles = articles[:3]

formatted_articles = [
    f"{STOCK_NAME}: {up_down}{diff_percent}%\n Headline: {article['title']}.\n Brief: {article['description']}" for
    article in three_articles]

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

for article in formatted_articles:
    message = client.messages.create(
        body=article,
        from_='+13195058865',
        to='+821046321383'
    )

print(message.status)
