from turtle import width
from typing_extensions import final
from telethon.sync import TelegramClient
import datetime
import pandas as pd
from IPython import display 
from time import ctime, time,strftime, gmtime
import matplotlib.pyplot as plt
import numpy as np
import random
import xlsxwriter 

date_of_post = datetime.datetime(2022, 8, 20) # 1: Enter your date in the form of (year, month, day)
api_id = 10248804   # 2: Enter your api_id from telegram 
api_hash = '588f31db7d8df29fa32eab7ccb7a35f0' #3: Enter your api_hash from telegram 

chats=[]
channel_frame = pd.read_excel(r'C:\Users\jayde\Desktop\Test\Channels.xlsx')# 4: enter your telegram channels @'s into Channels.xlsx
for ind in channel_frame.index:
    chats.append(channel_frame["Channel @'s"][ind])

df = pd.DataFrame()
print('Scraping....')

for chat in chats:
    with TelegramClient('Analysis', api_id, api_hash) as client:
        for message in client.iter_messages(chat, offset_date=date_of_post, reverse=True):
            #print(message)
            data = { "group" : chat, "sender" : message.sender_id, "text" : message.text, "date" : message.date, 'views' :message.views
            }
            temp_df = pd.DataFrame(data, index=[1])
            df = df.append(temp_df)

df['date'] = df['date'].dt.tz_localize(None)

ty = strftime('%Y-%m-%d', gmtime()) + str(random.randint(0,100000))
output = "output-" + str(ty) +".xlsx"

excelChoice = input("Would you like to download the messages? y/n")
if excelChoice == "y":
    df.to_excel(r'C:\Users\jayde\Desktop\Test\Outputs'+ r'\\'+ output, index=False, header=True)
    
list_of_words = []
word_count = {}
common_word_list = ['near', 'after', 'more', 'been', 'than','then','also', 'the', 'of', 'to', 'and', 'a', 'in', 'is', 'it', 'you', 'that', 'he', 'was', 'for', 'on', 'are', 'with', 'as', 'I', 'his', 'they', 'be', 'at', 'one', 'have', 'this', 'from', 'or', 'had', 'by', 'not', 'word', 'but', 'what', 'some', 'we', 'can', 'out', 'other', 'were', 'all', 'there', 'when', 'up', 'use', 'your', 'how', 'said', 'an', 'each', 'she', 'which', 'do', 'their', 'time', 'if', 'will', 'way', 'about', 'many', 'then', 'them', 'write', 'would', 'like', 'so', 'these', 'her', 'long', 'make', 'thing']

for i in range(1, len(df.index)):
    post = str(df.iat[i,2])
    split = post.split()
    for word in split:
        w = ''.join(ch for ch in word if ch.isalnum())
        w = w.lower()
        if len(w) > 3 and w not in common_word_list: #prevents words like "and", "or", "but", etc. "
           list_of_words.append(w)

for word in list_of_words:
    count = list_of_words.count(word)
    word_count[word] = count

keys = list(word_count.keys())
values = list(word_count.values())

dfDict = {
    'Count' : values, 'Word': keys
}

df2 = pd.DataFrame(dfDict)
df2.sort_values(by=['Count'], inplace=True)

def plotGraphBar(): #will only show this amount of words  
    rows = int(input("How many words would you like to show?"))
    df2.drop(df2.index[:-rows], inplace=True)
    fig = plt.figure(figsize=(20,10))
    plt.bar(df2['Word'], df2['Count'])
    plt.xticks(rotation=90)
    plt.show()

def plotGraphPie(): #will only show this amount of words  
    rows = int(input("How many words would you like to show?"))
    df2.drop(df2.index[:-rows], inplace=True)
    fig = plt.figure(figsize=(20,10))
    plt.pie(df2['Count'], labels =df2['Word'], autopct='%1.2f%%')
    plt.xticks(rotation=90)
    plt.show()

choice = input("Which type of graph would you like? Options are: bar and pie. If the answer is typed wrong, it will default to bar.")
if choice == "bar":
    plotGraphBar()
elif choice == "pie": 
    plotGraphPie()
else: 
    plotGraphBar()



