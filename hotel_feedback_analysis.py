# -*- coding: utf-8 -*-
"""Hotel Feedback Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12wsEDKO3LbgI2caun1Eu5WAg6fAEyY_F

# **Importing Libraries**
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
pd.set_option('display.max_rows', None)

"""# **Importing Data**"""

sntmnt = pd.read_csv("/content/tripadvisor_hotel_reviews.csv")

"""# **View of the first 5 rows**"""

sntmnt.head()

"""# **View of the last 5 rows**"""

sntmnt.tail()

"""# **Shape of the Dataframe**"""

sntmnt.shape

"""# **Checking for Null values**"""

sntmnt.isna().sum()

"""# **Checking for Blank Values**"""

blank = []
for index in sntmnt["Review"]:
  if index.isspace() == True:
    blank.append(index)

blank

"""# **Distribution of Ratings**"""

sntmnt['Rating'].value_counts().sort_values()

"""# Distributing Rating into two categories"""

def rating(rating):
  if rating > 3 and rating <=5:
    return "Positive"
  if rating > 0 and rating <=3:
    return "Negative"

"""# Create a new column"""

sntmnt['PosorNegRating'] = sntmnt['Rating'].apply(rating)

"""# Viewing new dataframe"""

sntmnt

sntmnt['PosorNegRating'].value_counts()

"""# **Sentiment Analysis** 

---


"""

import nltk
nltk.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer
sentimentAnalyze = SentimentIntensityAnalyzer()

sntmnt['Scores'] = sntmnt['Review'].apply(lambda review: sentimentAnalyze.polarity_scores(review))

sntmnt.tail(25)

sntmnt['Compound'] = sntmnt['Scores'].apply(lambda f:f["compound"])

sntmnt.head()

sntmnt['CompoundPosorNeg'] = sntmnt['Compound'].apply(lambda score:"Positive" if score>0 else "Negative")

"""# Viewing 1st 25 rows of the new data frame after all changes"""

sntmnt.head(25)

sntmnt.head()

example = "I want to know why he HATES me? :("
sentimentAnalyze.polarity_scores(example)

"""# Distribution of CompoundPosorNeg column"""

sns.barplot(x='CompoundPosorNeg',y='Rating', data = sntmnt)

x = sntmnt['CompoundPosorNeg'].value_counts()
labels = ['Positive', 'Negative']
fig, ax = plt.subplots(figsize = (10,10))

ax.pie(x, labels = labels)
plt.show

"""# **Text Classification**

---


"""

X = sntmnt['Review']
y = sntmnt['PosorNegRating']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 2529)

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

Textclf = Pipeline([('tfidf',TfidfVectorizer()),('clf',LinearSVC())])

Textclf.fit(X_train, y_train)

pred = Textclf.predict(X_test)

from sklearn.metrics import accuracy_score

print(accuracy_score(y_test,pred))