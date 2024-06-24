import json
import logging
from twitchio.ext import commands
from confluent_kafka import Consumer, KafkaException, KafkaError

import config

logging.basicConfig(filename='twitchapp.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

CLIENT_ID = config.CLIENT_ID
TOKEN = config.TMI_TOKEN
BOT_NICK = "jweewee"
CHANNEL = "jweewee"

topic = "reddit_nba"

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=TOKEN, client_id=CLIENT_ID, nick=BOT_NICK, prefix='!', initial_channels=[CHANNEL])

        configuration = config.read_config()
        configuration["group.id"] = "python-group-1"
        configuration["auto.offset.reset"] = "earliest"
        self.consumer = Consumer(configuration)
        self.consumer.subscribe([topic])
        self.loop.create_task(self.consume_kafka_messages())

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        
        # Send a message to the chat when the bot is ready
        await self.get_channel(CHANNEL).send("HELLO CHAT! Reddit_Bot is online!")

    async def consume_kafka_messages(self):
        while True:
            msg = self.consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    raise KafkaException(msg.error())
            key = msg.key().decode("utf-8")
            value = msg.value().decode("utf-8")
            comment_data = json.loads(value)
            comment_body = comment_data['body']
            logging.info(f"Consumed message from topic: {topic}: Key/Comment_id-> {key} Value-> Comment_data of id: {key}")
            self.send_comment_to_chat(comment_body)
            
    async def send_comment_to_chat(self, comment):
        channel = self.get_channel(CHANNEL)
        if channel:
            channel.send(comment)
        else:
            logging.error("Channel not found or bot not connected to channel.")

if __name__ == "__main__":
    bot = Bot()
    bot.run()
