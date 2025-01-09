# -*- coding: utf-8 -*-
"""AI_project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iMmChSb5UOpJmagmgs19uEOKS53d14FH
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV
import string, nltk
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')

from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression

nltk.download('punkt')

nltk.download('omw-1.4')

df = pd.read_csv('/content/fake reviews dataset.csv')
df.head()

df.isnull().sum()

df.info()

df.describe()

df['rating'].value_counts()

# Plotting a pie chart to show the proportion of each rating
plt.figure(figsize=(15,8))
labels = df['rating'].value_counts().keys()
values = df['rating'].value_counts().values
explode = (0.1,0,0,0,0)
plt.pie(values, labels=labels, explode=explode, shadow=True, autopct='%1.1f%%')
plt.title('Proportion of each rating', fontweight='bold', fontsize=25, pad=20, color='crimson')
plt.show()

# Defining a function to clean text by removing punctuation and stopwords
def clean_text(text):
    nopunc = [w for w in text if w not in string.punctuation]
    nopunc = ''.join(nopunc)
    return  ' '.join([word for word in nopunc.split() if word.lower() not in stopwords.words('english')])

# Applying the clean_text function to the 'text_' column and displaying the result
df['text_'][0], clean_text(df['text_'][0])

# Applying the clean_text function to the first few rows of the 'text_' column
df['text_'].head().apply(clean_text)

df['text_'] = df['text_'].astype(str)

# Defining a function to preprocess text by tokenizing, removing stopwords, digits, and punctuation
def preprocess(text):
    return ' '.join([word for word in word_tokenize(text) if word not in stopwords.words('english') and not word.isdigit() and word not in string.punctuation])

preprocess(df['text_'][4])

# Applying the preprocess function to different subsets of the 'text_' column
df['text_'][:10000] = df['text_'][:10000].apply(preprocess)

df['text_'][10001:20000] = df['text_'][10001:20000].apply(preprocess)

df['text_'][20001:30000] = df['text_'][20001:30000].apply(preprocess)

df['text_'][30001:40000] = df['text_'][30001:40000].apply(preprocess)

df['text_'][40001:40432] = df['text_'][40001:40432].apply(preprocess)

df['text_'] = df['text_'].str.lower()

# Stemming words in the 'text_' column using PorterStemmer
stemmer = PorterStemmer()
def stem_words(text):
    return ' '.join([stemmer.stem(word) for word in text.split()])
df['text_'] = df['text_'].apply(lambda x: stem_words(x))

# Lemmatizing words in the 'text_' column using WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
def lemmatize_words(text):
    return ' '.join([lemmatizer.lemmatize(word) for word in text.split()])
df["text_"] = df["text_"].apply(lambda text: lemmatize_words(text))

df['text_'].head()

df.to_csv('Preprocessed Fake Reviews Detection Dataset.csv')



df = pd.read_csv('Preprocessed Fake Reviews Detection Dataset.csv')
df.head()

df.drop('Unnamed: 0', axis=1, inplace=True)

df.head()

df.dropna(inplace=True)

df['length'] = df['text_'].apply(len)

df.info()

df.groupby('label').describe()

# Displaying the longest text in the 'text_' column for the 'OR' label
df[df['label']=='OR'][['text_', 'length']].sort_values(by='length', ascending=False).head().iloc[0].text_

df.length.describe()  # Displaying descriptive statistics of the 'length' column

# Defining a function to process text by removing punctuation and stopwords
def text_process(review):
    nopunc = [char for char in review if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]

bow_transformer = CountVectorizer(analyzer=text_process)
bow_transformer

bow_transformer.fit(df['text_'])
print("Total Vocabulary:", len(bow_transformer.vocabulary_))

# Transforming all texts in the 'text_' column into a bag of words representation
bow_reviews = bow_transformer.transform(df['text_'])

print("Shape of Bag of Words Transformer for the entire reviews corpus:",bow_reviews.shape)
print("Amount of non zero values in the bag of words model:",bow_reviews.nnz)

tfidf_transformer = TfidfTransformer().fit(bow_reviews)

# Transforming all texts in the bag of words representation to TF-IDF representation
tfidf_reviews = tfidf_transformer.transform(bow_reviews)
print("Shape:", tfidf_reviews.shape)
print("No. of Dimensions:", tfidf_reviews.ndim)

"""## Creating training and testing data"""

# Creating training and testing data
review_train, review_test, label_train, label_test = train_test_split(df['text_'], df['label'], test_size=0.35)

# Creating a pipeline for Multinomial Naive Bayes classification
pipeline = Pipeline([
    ('bow', CountVectorizer(analyzer=text_process)),
    ('tfidf', TfidfTransformer()),
    ('classifier', MultinomialNB())
])

"""## Training and testing Multinomial Naive Bayes Algorithm on the preprocessed data"""

# Training the Multinomial Naive Bayes model
pipeline.fit(review_train, label_train)

predictions = pipeline.predict(review_test)
predictions

print('Model Prediction Accuracy:',str(np.round(accuracy_score(label_test,predictions)*100,2)) + '%')

pipeline = Pipeline([
    ('bow',CountVectorizer(analyzer=text_process)),
    ('tfidf',TfidfTransformer()),
    ('classifier',RandomForestClassifier())
])

pipeline.fit(review_train,label_train)

rfc_pred = pipeline.predict(review_test)
rfc_pred

print('Random Forests Classifier Prediction Accuracy:', str(np.round(accuracy_score(label_test, rfc_pred) * 100, 2)) + '%')

pipeline = Pipeline([
    ('bow',CountVectorizer(analyzer=text_process)),
    ('tfidf',TfidfTransformer()),
    ('classifier',DecisionTreeClassifier())
])

pipeline.fit(review_train,label_train)

dtree_pred = pipeline.predict(review_test)
dtree_pred

print('Model Prediction Accuracy:',str(np.round(accuracy_score(label_test,dtree_pred)*100,2)) + '%')

pipeline = Pipeline([
    ('bow',CountVectorizer(analyzer=text_process)),
    ('tfidf',TfidfTransformer()),
    ('classifier',KNeighborsClassifier(n_neighbors=2))
])

pipeline.fit(review_train,label_train)

knn_pred = pipeline.predict(review_test)
knn_pred

print('Model Prediction Accuracy:',str(np.round(accuracy_score(label_test,knn_pred)*100,2)) + '%')

pipeline = Pipeline([
    ('bow',CountVectorizer(analyzer=text_process)),
    ('tfidf',TfidfTransformer()),
    ('classifier',SVC())
])

pipeline.fit(review_train,label_train)

svc_pred = pipeline.predict(review_test)
svc_pred

print('Model Prediction Accuracy:',str(np.round(accuracy_score(label_test,svc_pred)*100,2)) + '%')

pipeline = Pipeline([
    ('bow',CountVectorizer(analyzer=text_process)),
    ('tfidf',TfidfTransformer()),
    ('classifier',LogisticRegression())
])

pipeline.fit(review_train,label_train)

lr_pred = pipeline.predict(review_test)
lr_pred

print('Model Prediction Accuracy:',str(np.round(accuracy_score(label_test,lr_pred)*100,2)) + '%')

"""# Conclusion"""

print('Logistic Regression Prediction Accuracy:', str(np.round(accuracy_score(label_test, lr_pred) * 100, 2)) + '%')
print('K Nearest Neighbors Prediction Accuracy:', str(np.round(accuracy_score(label_test, knn_pred) * 100, 2)) + '%')
print('Decision Tree Classifier Prediction Accuracy:', str(np.round(accuracy_score(label_test, dtree_pred) * 100, 2)) + '%')
print('Random Forests Classifier Prediction Accuracy:', str(np.round(accuracy_score(label_test, rfc_pred) * 100, 2)) + '%')
print('Support Vector Machines Prediction Accuracy:', str(np.round(accuracy_score(label_test, svc_pred) * 100, 2)) + '%')
print('Multinomial Naive Bayes Prediction Accuracy:', str(np.round(accuracy_score(label_test, predictions) * 100, 2)) + '%')