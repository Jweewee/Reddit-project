import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from wordcloud import WordCloud
import time
from collections import Counter
import tkinter as tk
from tkinter import scrolledtext



x_vals = []
y_vals = []

index = count()

test = "Having Porzingis on your team means you’re gonna learn so much about human anatomy. I’m not gonna front like I know where the medial retinaculum is located"

# word_dict= {'gon': 2, 'na': 2, 'Having': 1, 'Porzingis': 1, 'team': 1, 'means': 1, 'youre': 1, 'learn': 1, 'much': 1, 'human': 1, 'anatomy': 1, 'Im': 1, 'front': 1, 'like': 1, 'I': 1, 'know': 1, 'medial': 1, 'retinaculum': 1, 'located': 1}

def animate(i):
    data = pd.read_csv('data.csv')
    x = data['x_value']
    y1 = data['total_1']
    y2 = data['total_2']

    plt.cla()

    plt.plot(x, y1, label='Channel 1')
    plt.plot(x, y2, label='Channel 2')

    plt.legend(loc='upper left')
    plt.tight_layout()

    wc = WordCloud(width=2000, height=1000, max_words=200).generate_from_frequencies(Counter(word_dict))


# ani = FuncAnimation(plt.gcf(), animate, interval=1000)

# plt.tight_layout()
# plt.show()

plt.ion()
# for i in range(100):
#     x = range(i)
#     y = range(i)
#     # plt.gca().cla() # optionally clear axes
#     plt.plot(x, y)
#     plt.title(str(i))
#     plt.draw()
#     plt.pause(2)

# plt.show(block=True)
word_dict = Counter()

def draw_wordcloud(word_freq):
    wc = WordCloud(width=800, height=400, max_words=200).generate_from_frequencies(word_freq)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.draw()
    plt.pause(0.1)  # Small pause to allow the plot to update

def event_stream():
    # plt.ion()

    events = ["click", "hover", "scroll",
            'Sorry equal charm joy her those folly ham',
            'Recommend new contented intention improving bed performed age',
            'considered it precaution an melancholy or',
            'Dissimilar of favourable solicitude if sympathize middletons at',
            'disposing perfectly in an eagerness perceived necessary',
            'extremity yet forfeited prevailed own off',
            'agreed others exeter period myself few yet nature',
            'To an occasional dissimilar impossible sentiments']
    while True:
        x = random.choice(events)
        yield x
        time.sleep(1)  # Simulate real-time interval

        # for word in x.split():
        #     word_dict[word] += 1
        # wc = WordCloud(width=800, height=400, max_words=200).generate_from_frequencies(word_dict)
        # print(word_dict)
        # plt.imshow(wc, interpolation='bilinear')
        # plt.axis('off')
        # plt.draw()
        # plt.pause(1)
message_display = scrolledtext.ScrolledText(tk.Tk(), width=60, height=20)
message_display.pack(padx=10, pady=10)

def display_comment_locally(comment):
    message_display.insert(tk.END, f"Received comment from Kafka: {comment}\n")
    message_display.see(tk.END)  # Scroll to the end of the text

event = event_stream()
for _ in range(25):
    x = next(event)
    print(x)
    # for word in x.split():
        # word_dict[word] += 1
    display_comment_locally(x)
    # draw_wordcloud(word_dict)


plt.ioff()
plt.show()