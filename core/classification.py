import pandas as pd
import os
from config.settings import BASE_DIR
import joblib
import numpy as np

from core.preprocessing import PreProcessing

class Classification():
    def __init__(self,test_size=2) -> None:
        self.test_size = test_size
        self._load_dataset(os.path.join(BASE_DIR, "core/data"))
        pass

    def _load_dataset(self, corpus_path):
        model_preprocessing = None
        model_pembobotan = None

        model_preprocessing = joblib.load(corpus_path+"/dataset_"+str(self.test_size)+"/preprocessing.model")
        model_pembobotan = joblib.load(corpus_path+"/dataset_"+str(self.test_size)+"/pembobotan.model")
        model_sklearn = joblib.load(corpus_path+"/dataset_"+str(self.test_size)+"/sklearn.model")
        
        self.preprocessing_train = model_preprocessing['train']
        self.preprocessing_test = model_preprocessing['test']
        self.pembobotan_tweet = model_pembobotan['train']
        self.pembobotan_tf = model_pembobotan['tf']
        self.pembobotan_tfidf = model_pembobotan['tfidf']
        self.vectorizer = model_sklearn['vectorizer']
        self.classifier = model_sklearn['classifier']

    def clean_text(self, text):
        preprocess = PreProcessing()
        text_cleaned = preprocess.callback(text)
        return text_cleaned

    def predict(self, text):
        text = self.clean_text(text)
        vector_data = self.vectorizer.transform([text])
        pred = self.classifier.predict(vector_data)
        prob = self.classifier.predict_proba(vector_data)
        prob = np.max(prob[0])

        if pred[0] == 'positive':
            pred = 1
        elif pred[0] == 'negative':
            pred = 2
        else:
            pred = 0
        # prob = np.max(prob[0])

        if (pred == 1):
            if prob >= 0.8:
                result = 1
            else:
                result = 0
        elif (pred == 2):
            if prob >= 0.8:
                result = 2
            else:
                result = 0
        else:
            result = 0
            
        return result