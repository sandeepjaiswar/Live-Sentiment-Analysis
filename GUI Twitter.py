from textblob import TextBlob
import tweepy
import matplotlib.pyplot as plt
from tkinter import *

def percentage(part, whole):
    return 100 * float(part) / float(whole)

consumerKey = "your credentials"
consumerSecret = "your credentials"
accessToken = "your credentials"
accessTokenSecret = "your credentials"

auth = tweepy.OAuthHandler(consumerKey,consumerSecret)
auth.set_access_token(accessToken,accessTokenSecret)
api = tweepy.API(auth)

root = Tk()
root.geometry("300x170")
root.title("Twitter Analysis")
heading = Label(text ="Welcome User",fg="black",bg="grey",width="400",height="2").pack()
label1 = Label(root, text="Enter the term you want to search")

E1 = Entry(root,bd =5)

label2 = Label(root, text="Enter the no. of tweets")
E2 = Entry(root,bd =5)

def getE1():
    return E1.get()

def getE2():
    return E2.get()

def execute():
    getE1()
    getE2()
    if E1.get() == "" and E2.get() == "":
        root1=Toplevel(root)
        root1.geometry("150x85")
        root1.title("Warning!")
        Label(root1,text="All Fields Required",fg="red").pack()
    elif E1.get() == "" or E2.get() == "":
        root2 = Toplevel(root)
        root2.geometry("150x85")
        root2.title("Warning!")
        Label(root2, text="All Fields Required", fg="red").pack()
    elif E2.get().isdigit():
        getData()

    else:
        root3 = Toplevel(root)
        root3.geometry("150x85")
        root3.title("Warning!")
        Label(root3, text="No. of tweets should be integer", fg="red").pack()


def getData():
    getE1()
    searchTerm = getE1()

    getE2()
    NoOfTerms = getE2()
    NoOfTerms = int(NoOfTerms)

    tweets = tweepy.Cursor(api.search, q=searchTerm).items(NoOfTerms)


    positive = 0
    negative = 0
    neutral = 0
    polarity = 0

    for tweet in tweets:
        try:
            print(tweet.text)
            analysis = TextBlob(tweet.text)
            polarity += analysis.sentiment.polarity

            if (analysis.sentiment.polarity == 0):
                neutral += 1

            elif (analysis.sentiment.polarity < 0.00):
                negative += 1

            elif (analysis.sentiment.polarity > 0.00):
                positive += 1

        except tweepy.TweepError as e:
                print(e.reason)

        except StopIteration:
                break


    positive = percentage(positive, NoOfTerms)
    negative = percentage(negative, NoOfTerms)
    neutral = percentage(neutral, NoOfTerms)
    polarity = percentage(polarity, NoOfTerms)


    positive = format(positive, '.2f')
    negative = format(negative, '.2f')
    neutral = format(neutral, '.2f')


    print("How people are reacting on " + searchTerm +
        " By analyzing " + str(NoOfTerms) + " Tweets ")

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
               + searchTerm + ' by analyzing '
               + str(NoOfTerms) + ' Tweets ')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

submit = Button(root, text ="Submit", command = execute)
label1.pack()
E1.pack()
label2.pack()
E2.pack()
submit.pack(side =BOTTOM)
root.mainloop()
