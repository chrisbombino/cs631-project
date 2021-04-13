import keras
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential, load_model
from keras.preprocessing.text import Tokenizer
import re
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore")

class SentimentAnalyzer():
    def __init__(self):
        pass
    
    def load_model(self):
        # TODO: Load saved model from models folder
        saved_model = load_model('../model/best_model_2.h5')
        return saved_model
    
    def preprocess(self, text):
        # TODO: Preprocessing of text
        import re
        text = re.sub("RT @[\w]*:", "", text)
        text = re.sub("@[\w]*", "", text)
        text = re.sub("https?://[A-Za-z0-9./]*", "", text)
        text = re.sub("\n", "", text)
        text = re.sub("[^a-zA-z0-9\s]", "", text)
        # should return the same datatype as text and format i.e a string of complete text (not a list of words)
        return text.lower()

    def token(self):
        tweets = pd.read_csv('../model/Tweets.csv', sep=',')
        data = tweets['text'].apply(lambda x: self.preprocess(x))
        max_fatures = 2000
        tokenizer = Tokenizer(num_words=max_fatures, split=' ')
        tokenizer.fit_on_texts(data.values)
        return tokenizer

    def predict(self, text, tokenizer):
        # TODO: call preprocess
        # TODO: Make prediction over preprocessed text using loaded model

        # temporary predictions to help me set up kafka
        # predicted_sentiment = 1

        saved_model = self.load_model()
        cleaned_text = self.preprocess(text)

        text_pad_sequence = pad_sequences(tokenizer.texts_to_sequences([cleaned_text]), maxlen=32)
        # predict_result = np.argmax(saved_model.predict(text_pad_sequence, batch_size=1)[0])
        predict_result = np.argmax(saved_model(text_pad_sequence)[0])
        return str(predict_result)

# # # init sentiment analyzer
# sa = SentimentAnalyzer()
# # tokenizer = sa.token()
# text = ""
# print(sa.preprocess(text))
# print(sa.predict(text, tokenizer))