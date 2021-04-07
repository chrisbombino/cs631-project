class SentimentAnalyzer():
    def __init__(self):
        pass
    
    def load_model(self, model_path):
        # TODO: Load saved model from models folder
        pass

    def predict(self, text):
        # TODO: Create preprocess function to clean text (stopwords, punctuations etc)
        # TODO: Make prediction over preprocessed text using loaded model

        # temporary predictions to help me set up kafka
        predicted_sentiment = 1
        return str(predicted_sentiment)