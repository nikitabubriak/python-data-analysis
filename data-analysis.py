import json
import tweepy
from tkinter import *
from textblob import TextBlob as textblob
import matplotlib.pyplot as plot
from datetime import datetime

#Twitter API authenticator
def getOAuthHandler():
    
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
    
    return auth

#Data analysis plotting
def getSentimentPlot():

    #Data
    keyword = entrySearchKeyword.get()
    sampleSize = int(entrySampleSize.get())

    polarities = analyseTweetPolarities(keyword, sampleSize)
    averagePolarity = (sum(polarities))/(len(polarities)) * 100
    
    sentiment = str(concludeSentiment(averagePolarity))
    
    time = datetime.now().strftime("\nAt: %H:%M" + "\nOn: %m-%d-%y")
    averagePolarity = "{0:.0f}%".format(averagePolarity)
    
    #Plot
    axes = plot.gca()
    axes.set_ylim([-1, 2])

    plot.scatter(range(1, sampleSize + 1), polarities)
    
    plot.text(1.75, 
              1.25, 
              "Average sentiment: " + averagePolarity + sentiment + time, 
              fontsize = 12, 
              bbox = dict(facecolor = 'none', 
                          edgecolor = 'black', 
                          boxstyle  = 'square, pad = 1'
                          )
              )

    plot.title("Sentiment of " + keyword + " on Twitter")
    plot.xlabel("Sample size")
    plot.ylabel("Sentiment")
    
    plot.show()

#Tweets polarity analysis
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

#Conclude overall sentiment based on average tweet polarity
def concludeSentiment(p):
    
    sentiment = " Unknown"
    
    if  -100 <= p < -50:
        sentiment = " Very Negative"
    elif -50 <= p < -10:
        sentiment = " Negative"
    elif -10 <= p <= 10:
        sentiment = " Neutral"
    elif  10 <  p <= 50:
        sentiment = " Positive"
    elif  50 <  p <= 100:
        sentiment = " Very Positive"
    else:
        sentiment = " Out of range"
    
    return sentiment

#API Setup
api = tweepy.API(getOAuthHandler())

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