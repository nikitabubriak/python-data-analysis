import json
import tweepy
from tkinter import *
from textblob import TextBlob as textblob
import matplotlib.pyplot as plot
from datetime import datetime

#Twitter API authentication
f = open('auth.json', 'r')
authData = json.load(f)
f.close()

consumerKey         = authData[0]
consumerSecret      = authData[1]
accessToken         = authData[2]
accessTokenSecret   = authData[3]

auth = tweepy.OAuthHandler(
    consumerKey, 
    consumerSecret
)
auth.set_access_token(
    accessToken, 
    accessTokenSecret
)
api = tweepy.API(auth)

#Tweets sentiment analysis
def analyseTweetPolarities(keyword, sampleSize):
    
    polarities = []
    
    for tweet in tweepy.Cursor(api.search_tweets, keyword, lang = "en").items(sampleSize):
        try:
            analysis = textblob(tweet.text)
            analysis = analysis.sentiment
            polarity = analysis.polarity
            polarities.append(polarity)

        except tweepy.TweepError as e:
            print(e.reason)

        except StopIteration:
            break
    
    return polarities

#Data analysis plotting
def getSentimentPlot():
    
    keyword = entrySearchKeyword.get()
    sampleSize = int(entrySampleSize.get())

    polarities = analyseTweetPolarities(keyword, sampleSize)

    axes = plot.gca()
    axes.set_ylim([-1, 2])

    plot.scatter(range(1, sampleSize + 1), polarities)

    averagePolarity = (sum(polarities))/(len(polarities))
    
    averagePolarity = "{0:.0f}%".format(averagePolarity * 100)
    
    time = datetime.now().strftime("At: %H:%M\n" + "On: %m-%d-%y")

    plot.text(1.75, 
              1.25, 
              "Average sentiment: " + str(averagePolarity) + "\n" + time, 
              fontsize = 12, 
              bbox = dict(facecolor = 'none', 
                          edgecolor = 'black', 
                          boxstyle = 'square, pad = 1'
                          )
              )

    plot.title("Sentiment of " + keyword + " on Twitter")
    plot.xlabel("Sample size")
    plot.ylabel("Sentiment")
    plot.show()

#Tkinter GUI
root = Tk()

labelSearchKeyword = Label(root, text = "Search keyword")
entrySearchKeyword = Entry(root, bd = 5)

labelSampleSize = Label(root, text = "Sample size")
entrySampleSize = Entry(root, bd = 5)

submit = Button(root, text = "Submit", command = getSentimentPlot)

labelSearchKeyword.pack()
entrySearchKeyword.pack()
labelSampleSize.pack()
entrySampleSize.pack()
submit.pack(side = BOTTOM)

root.mainloop()