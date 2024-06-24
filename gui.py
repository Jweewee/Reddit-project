import tkinter as tk
from tkinter import scrolledtext
from confluent_kafka import Consumer, KafkaException, KafkaError
import json
import config
import time

CLIENT_ID = config.CLIENT_ID
TOKEN = config.TMI_TOKEN
BOT_NICK = "jweewee"
CHANNEL = "jweewee"
topic = "reddit_nba"

class KafkaGuiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kafka Message Viewer")

        # Create a scrolled text widget to display messages
        self.message_display = scrolledtext.ScrolledText(self.root, width=60, height=20)
        self.message_display.pack(padx=10, pady=10)

        # Kafka consumer setup
        configuration = config.read_config()
        configuration["group.id"] = "python-group-1"
        configuration["auto.offset.reset"] = "earliest"
        self.consumer = Consumer(configuration)
        self.consumer.subscribe([topic])
        self.consume_kafka_messages()

    def consume_kafka_messages(self):
        try:
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
                self.display_comment_locally(comment_body)
        except KeyboardInterrupt:
            pass
        finally:
            self.consumer.close()

    def display_comment_locally(self, comment):
        self.message_display.insert(tk.END, f"Received comment from Kafka: {comment}\n")
        self.message_display.see(tk.END)  # Scroll to the end of the text


class Example(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.text = tk.Text(self, height=6, width=40)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)

        self.add_timestamp()

    def add_timestamp(self):
        self.text.insert("end", time.ctime() + "\n")
        self.text.see("end")
        self.after(1000, self.add_timestamp)

if __name__ == "__main__":
    # root = tk.Tk()
    # # app = KafkaGuiApp(root)
    # root.mainloop()
    root =tk.Tk()
    frame = Example(root)
    frame.pack(fill="both", expand=True)
    root.mainloop()