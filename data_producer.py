import time
import csv
import json
import logging
from datetime import datetime  
from collections import Counter

import praw
from confluent_kafka import Producer, Consumer, KafkaError
from wordcloud import WordCloud
import matplotlib.pyplot as plt

import config

# Set up logging
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def bot_login():
    """Log in to Reddit using the praw library.
    Returns: praw.Reddit: A Reddit instance."""
    reddit = praw.Reddit(
        username = config.username,
        password = config.password,
        client_id = config.client_id,
        client_secret = config.client_secret,
        user_agent = "joshua's data project")
    return reddit

def check_rate_limit(r):
    """Check the rate limit of the Reddit API.
    Parameters: r (praw.Reddit): A Reddit instance.
    Returns: Tuple[float, float, float]: A tuple containing the number of used tokens, remaining tokens, and the reset time."""
    headers = r.auth.limits
    used = headers['used']
    remaining = headers['remaining']
    reset = headers['reset_timestamp']
    return used, remaining, reset

def get_time_to_reset(reset_time):
    """Calculate the time difference until rate limit reset.
    Parameters: reset_time (timestamp): The time at which the rate limit will reset.
    Returns: [float]The time difference in seconds until the rate limit resets."""
    current_time = time.time()
    return reset_time - current_time

def is_above_rate_limit(reddit_instance, token_min):
    """Check if the rate limit is above the specified minimum tokens.
    Parameters: reddit_instance (praw.Reddit): A Reddit instance.
                token_min (int): The minimum number of tokens to check against.
    Returns: bool: True if the remaining tokens are above the minimum, False otherwise."""
    _, remaining, _ = check_rate_limit(reddit_instance)
    return remaining > token_min

def wait_for_rate_limit_reset(reddit_instance):
    """Wait until the rate limit resets.
    Parameters: reddit_instance (praw.Reddit): A Reddit instance.
    Returns: None"""
    _, _, reset = check_rate_limit(reddit_instance)
    time_difference = get_time_to_reset(reset)
    if time_difference > 5:
        print(f"Rate limit exceeded. Waiting for {time_difference + 5} seconds...")
        time.sleep(time_difference + 5)

def generate_comment_data(comment):
    '''Generate a dictionary containing the comment data.
    Parameters: comment (praw.models.Comment): A Reddit comment object.
    Returns: dict: A dictionary containing the comment data.'''
    return {
        'body': comment.body,
        'created_utc': comment.created_utc,
        'author': comment.author.name,
        'id': comment.id
    }

def delivery_report(err, msg):
    """Delivery report callback called once for each message produced.
    Reports the message delivery status.
    Parameters: err (KafkaError): The error that occurred on None if no error.
                    msg (Message): The message that was produced or failed.
    Returns: None"""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def produce_comments(r, topic, sreddit_title, token_min=200):
    '''Produce comments from a subreddit to a Kafka topic.
    Parameters: r (praw.Reddit): A Reddit instance.
                sreddit_title (str): The title of the subreddit to produce comments from.
                token_min (int): The minimum number of tokens to check against.
    Returns: None'''
    sbreddit_instance = r.subreddit(sreddit_title)
    comment_stream = sbreddit_instance.stream.comments(skip_existing=True)

    i = 0 

    producer = Producer(configuration)

    for top_level_comment in comment_stream:
            body = top_level_comment.body
            comment_time = datetime.fromtimestamp(top_level_comment.created_utc)
            comment_data = generate_comment_data(top_level_comment)

            if is_above_rate_limit(r, token_min):
                producer.produce('reddit_nba', key=str(top_level_comment.id), value=json.dumps(comment_data), callback=delivery_report)
                producer.poll(0)
                logging.info(f"Produced message to topic: {topic}: Key/Comment_id-> {top_level_comment.id} Value-> Comment_data of id: {top_level_comment.id}")


            else:
                wait_for_rate_limit_reset(r)
                # logging.info(f"Comment no: {i} -> {body}")

                producer.produce('reddit_nba', key=str(top_level_comment.id), value=json.dumps(comment_data), callback=delivery_report)
                producer.poll(0)
                logging.info(f"Produced message to topic: {topic}: Key/Comment_id-> {top_level_comment.id} Value-> Comment_data of id: {top_level_comment.id}")


if __name__ == "__main__":
    subreddit_title = 'nba'
    r = bot_login()
    logging.info("LOGGED IN")  
    configuration = config.read_config()
    topic = "reddit_nba"
    produce_comments(r, topic, subreddit_title)