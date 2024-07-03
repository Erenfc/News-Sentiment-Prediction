import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from textblob import TextBlob

def get_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def classify_sentiment(sentiment_score):
    if sentiment_score > 0:
        return 'Positive'
    elif sentiment_score < 0:
        return 'Negative'
    else:
        return 'Neutral'

def scrape_news(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        texts = []

        headings = soup.find_all('h2')
        for heading in headings:
            if heading.text.strip():
                texts.append(heading.text.strip())

        divheadings = soup.find_all('div')
        for heading in divheadings:
            if heading.text.strip():
                texts.append(heading.text.strip())

        paragraphs = soup.find_all('p')
        for paragraph in paragraphs:
            if paragraph.text.strip():
                texts.append(paragraph.text.strip())

        sentiment_counts = {
            'Positive': 0,
            'Negative': 0,
            'Neutral': 0
        }

        for text in texts:
            sentiment_score = get_sentiment(text)
            sentiment = classify_sentiment(sentiment_score)
            sentiment_counts[sentiment] += 1

        overall_sentiment = max(sentiment_counts, key=sentiment_counts.get)

        print(f"URL: {url}")
        print("Sentiment Counts:")
        for sentiment, count in sentiment_counts.items():
            print(f"{sentiment}: {count}")

        print(f"Overall Sentiment: {overall_sentiment}")
        print()

        # img_tags = soup.find_all('img')        
        # for img_tag in img_tags:
        #     img_url = img_tag.get('src')
        #     if img_url:
        #         img_filename = os.path.basename(urlparse(img_url).path)

        #         img_response = requests.get(img_url)
        #         if img_response.status_code == 200:
        #             with open(img_filename, 'wb') as f:
        #                 f.write(img_response.content)
        #             print(f"Saved {img_filename} from {url}")
        #         else:
        #             print(f"Failed to download image {img_url} from {url}")

    else:
        print(f"Failed to retrieve content from {url}")

urls = [
    "https://timesofindia.indiatimes.com/",
    "https://www.indiatoday.in/",
    "https://www.thehindu.com/",
    "https://indianexpress.com/",
    "https://www.news18.com/",
    "https://www.newsnation.in/",
    "https://www.firstpost.com/",
    "https://www.deccanchronicle.com/"
]

for url in urls:
    scrape_news(url)
    print("-" * 100)
