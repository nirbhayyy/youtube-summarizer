from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
sia=SentimentIntensityAnalyzer()

def summary_sentiments(summary_text):
    sentences=sent_tokenize(summary_text)
    result=[]

    for sentence in sentences:
        score=sia.polarity_scores(sentence)
        compound = score["compound"]

        if compound >= 0.05:
                sentiment = "Positive"
        elif compound <= -0.05:
                sentiment = "Negative"
        else:
                sentiment = "Neutral"

        result.append( {
                    "sentence": sentence,
                    "sentiment": sentiment,
                    "positive": score["pos"],
                    "neutral": score["neu"],
                    "negative": score["neg"],
                    "compound": compound,
                })
            

    

    
    return result


from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

def overall_sentiment(text):

    score = sia.polarity_scores(text)

    compound = score["compound"]

    if compound >= 0.05:
        sentiment = "Positive"
    elif compound <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "sentiment": sentiment,
        "positive": score["pos"],
        "neutral": score["neu"],
        "negative": score["neg"],
        "compound": compound,
    }