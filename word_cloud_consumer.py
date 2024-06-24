import time
import json
from datetime import datetime  
from collections import Counter
import logging
import re

from confluent_kafka import Producer, Consumer, KafkaError
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob

import config

# consumer = Consumer({
#     'bootstrap.servers': 'your_kafka_bootstrap_server',
#     'group.id': 'wordcloud_group',
#     'auto.offset.reset': 'earliest'
# })

# consumer.subscribe(['reddit_comments'])

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def remove_special_characters(text):
    '''Removes special characters from the text.
    Parameters: text (str): The text from which to remove special characters.
    Returns: str: The text with special characters removed.'''
    text = re.sub(r'[^A-Za-z0-9\s]+', '', text)  # Remove special characters
    return text

def remove_stopwords(text):
    '''Removes stopwords from the text.
    Parameters: text (str): The text from which to remove stopwords.
    Returns: str: The text with stopwords removed.'''
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word not in stop_words]
    return ' '.join(filtered_text)

def get_cleaned_text(text):
    '''Returns cleaned text by removing special characters and stopwords.
    Parameters: text (str): The text to be cleaned.
    Returns: str: The cleaned text.'''
    return remove_stopwords(remove_special_characters(text))

def draw_wordcloud(word_freq):
    '''Draws a word cloud based on the word frequency.
    Parameters: word_freq (dict): A dictionary containing the frequency of each word.
    Returns: None'''
    wc = WordCloud(width=800, height=400, max_words=200).generate_from_frequencies(word_freq)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.draw()
    plt.pause(0.5)  # Small pause to allow the plot to update

def update_word_freq_consume(word_freq, topic, configuration):
    '''Consumes messages from a Kafka topic and updates the word frequency and draws a live wordcloud.
    Parameters: word_freq (dict): A dictionary containing the frequency of each word.
                topic (str): The Kafka topic to consume messages from.
                configuration (dict): A dictionary containing the Kafka configuration.
    Returns: None'''
    configuration["group.id"] = "python-group-1"
    configuration["auto.offset.reset"] = "earliest"

    consumer = Consumer(configuration)
    consumer.subscribe([topic])

    word_freq["Start"] = 1
    i = 0
    plt.ion()
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is not None and msg.error() is None:
                key = msg.key().decode("utf-8")
                value = msg.value().decode("utf-8")

                comment_data = json.loads(msg.value().decode('utf-8'))
                comment_body = comment_data['body']
                logging.info(f"Consumed message from topic: {topic}: Key/Comment_id-> {key} Value-> Comment_data of id: {key}")

                words = get_cleaned_text(comment_body).split()
                for word in words:
                    word_freq[word] += 1
                # logging.info(f"Updated word frequency: {word_freq}")
                draw_wordcloud(word_freq)
                logging.info("Word cloud drawn.")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
        logging.info("Consumer closed.")

if __name__ == "__main__":
    word_freq = Counter()
    configuration = config.read_config()
    topic = "reddit_nba"
    update_word_freq_consume(word_freq, topic, configuration)
