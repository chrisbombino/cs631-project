import keras
from keras.preprocessing.sequence import pad_sequences
# from keras.models import Sequential, load_model
from tensorflow.keras.models import load_model
from keras.preprocessing.text import Tokenizer
import re
import pandas as pd
import numpy as np
import warnings
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
warnings.filterwarnings("ignore")

class SentimentAnalyzer():
    def __init__(self):
        pass
    
    def load_model(self):
        saved_model = load_model('../model/best_model_bilstm.h5')
        return saved_model
    
    def clean(self, text):
        text = re.sub("RT @[\w]*:", "", text)
        text = re.sub("@[\w]*", "", text)
        text = re.sub("https?://[A-Za-z0-9./]*", "", text)
        text = re.sub("\n", "", text)
        text = re.sub("[^a-zA-z\s]", "", text)
        # should return the same datatype as text and format i.e a string of complete text (not a list of words)
        return text.lower().split()

    def preprocess(self, text):
        return self.remove_stopwords(self.clean(text))

    def remove_stopwords(self, tokenized_sentence):
        return [token for token in tokenized_sentence if token not in set(stopwords.words("english"))]

    def token(self):
        data = pd.read_csv('../model/data_cleaned_shuffled.csv', sep=',')
        data['text_cleaned_string'] = data['text_cleaned_string'].astype('str')
        max_fatures = 10000
        tokenizer = Tokenizer(num_words=max_fatures, split=' ')
        tokenizer.fit_on_texts(data['text_cleaned_string'].values)
        return tokenizer

    def predict(self, text_list, tokenizer):
        # call preprocess
        # Make prediction over preprocessed text using loaded model
        saved_model = self.load_model()

        token_list = tokenizer.texts_to_sequences([" ".join(text_list)])
        # made a mistake here before, the input should be text, not list

        text_pad_sequence = pad_sequences(token_list, maxlen=32, )
        prediction = saved_model(text_pad_sequence)[0]
        confidence = np.max(prediction)
        predict_result = int(np.argmax(prediction))
        sentiment_list = ['Negative','Neutral','Positive']
        sentiment_name = sentiment_list[predict_result]
        return sentiment_name, float(confidence)

# # # # # init sentiment analyzer
# sa = SentimentAnalyzer()
# tokenizer = sa.token()
# text = "@iiii @jjjj"
# text_list = sa.preprocess(text)
# print(text_list)
# print(sa.predict(text_list, tokenizer))
