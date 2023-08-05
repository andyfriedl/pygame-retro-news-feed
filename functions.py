import requests
import re
import os
import json
import datetime

from bs4 import BeautifulSoup


def fetch_news(url):

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print(f"HTTP error occurred: {error}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    headlines = soup.select('a[data-testid="Heading"] > span, a[data-testid="Link"]')

    # Extract headline text and filter out unwanted headlines
    headlines_text = [headline.text.strip()
                      for headline in headlines if ', article' not in headline.text]

    # Join the headlines together into a single string seperated by '\n'
    text = '\n'.join(f"\\  >> {headline_text}" for headline_text in headlines_text)

    # Split the text into a list of sentences using a special character
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
                    # Less than an hour. Using stored news.
                    news = stored_news
                else:
                    # More than an hour. Stored latest news and date in file.
                    news = fetch_news(url)
                    with open(news_file, "w") as f:
                        f.write(json.dumps({"date": now.strftime(
                            "%Y-%m-%d %H:%M:%S"), "news": news}))

            except (json.JSONDecodeError, KeyError, ValueError, TypeError):
                # Re-created file and added current time and news.
                os.remove(news_file)
                with open(news_file, "w") as f:
                    now = datetime.datetime.now()
                    news = fetch_news(url)
                    f.write(json.dumps({"date": now.strftime(
                        "%Y-%m-%d %H:%M:%S"), "news": news}))
    else:
        # if file does not exist, create it and add current time and news to file
        with open(news_file, "w") as f:
            now = datetime.datetime.now()
            news = fetch_news(url)
            f.write(json.dumps({"date": now.strftime(
                "%Y-%m-%d %H:%M:%S"), "news": news}))

    return news
