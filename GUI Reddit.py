import praw
import matplotlib.pyplot as plt
from textblob import TextBlob
from tkinter import *

def percentage(part, whole):
    return 100 * float(part) / float(whole)

reddit = praw.Reddit(client_id='your credentials',
                     client_secret='your credentials',
                     user_agent='sandeepjaiswar')

root = Tk()
root.geometry("300x150")
root.title("Reddit Analysis")
heading = Label(text = "Welcome User",fg="black",bg="grey",width="400",height="2").pack()
label1 = Label(root, text="Enter the term you want to search :")
E1 = Entry(root, bd =5)

def getE1():
    return E1.get()

def execute():
    getE1()
    if E1.get()=="":
        root1 = Toplevel(root)
        root1.geometry("150x85")
        root1.title("Warning!")
        Label(root1, text="Enter the Field ", fg="red").pack()
    else:
        getData()


def getData():
    getE1()

    subreddit = reddit.subreddit(getE1())

    for comment in subreddit.comments(limit=100):


        try:

            print(comment.body)


        except praw.exceptions.PRAWException as e:
            print(str(e))

    positive = 0
    negative = 0
    neutral = 0
    polarity = 0

    for comm in subreddit.comments(limit=100):
        analysis = TextBlob(comm.body)
        polarity += analysis.sentiment.polarity

        if (analysis.sentiment.polarity == 0):
            neutral += 1

        elif (analysis.sentiment.polarity < 0.00):
            negative += 1

        elif (analysis.sentiment.polarity > 0.00):
            positive += 1

    positive = percentage(positive, 100)
    negative = percentage(negative, 100)
    neutral = percentage(neutral, 100)
    polarity = percentage(polarity, 100)


    positive = format(positive, '.2f')
    negative = format(negative, '.2f')
    neutral = format(neutral, '.2f')



    print("How people are reacting on " + getE1() +
            " By analyzing " + str(100) + " Reddit Comments")

    if (polarity == 0):
        print("Neutral")

    elif (polarity < 0.00):
        print("Negative")

    elif (polarity > 0.00):
        print("Positive")



    labels = ['Positive [' + str(positive) + '%]',
          'Neutral [' + str(neutral) + '%]',
          'Negative [' + str(negative) + '%]']

    sizes = [positive, neutral, negative]
    colors = ['yellowgreen', 'gold', 'red']
    patches, texts = plt.pie(sizes, colors=colors, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.title('How people are reacting on  '
          + getE1() + ' by analyzing '
          + str(100) + ' Reddit Comments ')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

submit = Button(root, text ="Submit", command = execute)
label1.pack()
E1.pack()
submit.pack(side =BOTTOM)
root.mainloop()