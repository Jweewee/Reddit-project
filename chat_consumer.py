import asyncio
import logging
import re
from collections import Counter

import matplotlib.pyplot as plt
from twitchio.ext import commands
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import config

logging.basicConfig(filename='twitch_app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class Bot(commands.Bot):

    def __init__(self, word_freq, **kwargs):
        super().__init__(**kwargs)
        self.word_freq = word_freq
        plt.ion()  # Enable interactive mode

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        logging.info(f'Logged in as {self.nick}')

    async def event_message(self, message):
        print(message.content)
        if message.echo:
            return

        cleaned_text = get_cleaned_text(message.content)
        for word in cleaned_text.split():
            self.word_freq[word] += 1

        draw_wordcloud(self.word_freq)
        logging.info("Word cloud drawn.")

# Replace with your Twitch credentials
bot = Bot(
    word_freq=Counter(),
    irc_token='oauth:YOUR_TWITCH_OAUTH_TOKEN',
    client_id='YOUR_TWITCH_CLIENT_ID',
    nick='YOUR_BOT_NICK',
    prefix='!',
    initial_channels=['YOUR_CHANNEL_NAME']
)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.start())