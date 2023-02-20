import requests
import re
import os
import json
import datetime

from bs4 import BeautifulSoup


def fetch_news(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    headlines = soup.select('a[data-testid="Heading"] > span')

    typero = ''

    for headline in headlines:
        headline_text = headline.text.strip()
        if not (re.search(', article', headline_text)):
            typero += "\\  >> " + headline_text

    text = typero

    # Split the text into a list of sentences based on the special character
    sentences = text.split('\\')

    return sentences


def return_news(url):
    # set up file name
    news_file = "news.txt"

    # check if file exists and has valid data
    if os.path.exists(news_file):
        with open(news_file, "r") as f:
            try:
                data = json.load(f)
                stored_date = datetime.datetime.strptime(
                    data["date"], "%Y-%m-%d %H:%M:%S")
                stored_news = data["news"]
                now = datetime.datetime.now()
                time_difference = now - stored_date
                seconds_difference = time_difference.total_seconds()

                if seconds_difference < 3600:
                    # use stored news
                    news = stored_news
                    print("Less than an hour. Using stored news.")
                else:
                    # fetch latest news
                    news = fetch_news(url)
                    with open(news_file, "w") as f:
                        f.write(json.dumps({"date": now.strftime(
                            "%Y-%m-%d %H:%M:%S"), "news": news}))
                        print(
                            "More than an hour. Stored latest news and date in file.")
            except (json.JSONDecodeError, KeyError, ValueError, TypeError):
                # re-create file if it is not valid
                os.remove(news_file)
                with open(news_file, "w") as f:
                    now = datetime.datetime.now()
                    news = fetch_news(url)
                    f.write(json.dumps({"date": now.strftime(
                        "%Y-%m-%d %H:%M:%S"), "news": news}))
                    print("Re-created file and added current time and news.")
    else:
        # if file does not exist, create it and add current time and news to file
        with open(news_file, "w") as f:
            now = datetime.datetime.now()
            news = fetch_news(url)
            f.write(json.dumps({"date": now.strftime(
                "%Y-%m-%d %H:%M:%S"), "news": news}))
            print("Created file and added current time and news.")

    return news
