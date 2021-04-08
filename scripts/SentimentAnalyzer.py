class SentimentAnalyzer():
    def __init__(self):
        pass
    
    def load_model(self, model_path):
        # TODO: Load saved model from models folder
        pass
    
    def preprocess(self, text):
        # TODO: Preprocessing of text

        # should return the same datatype as text and format i.e a string of complete text (not a list of words)
        return text

    def predict(self, text):
        # TODO: call preprocess
        # TODO: Make prediction over preprocessed text using loaded model

        # temporary predictions to help me set up kafka
        predicted_sentiment = 1
        return str(predicted_sentiment)