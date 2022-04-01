import numpy as np
import pandas as pd


class MultiNB:
    def __init__(self,alpha=1):
        self.alpha = alpha
        self.wct_ = {}
    
    def _prior(self): # CHECKED
        self.pc = {x:0 for x in self.classes_}
        self.total_w = sum(self.wn_classes_.values())
        self.total_idf = self.df_terms['idf'].sum()
        for i in self.classes_:
            self.pc[i] = np.log(self.dn_classes_[i] / sum(self.dn_classes_.values()))
        return self.pc
    
    def fit(self, df, df_terms): # CHECKED, matches 
        self.df = df
        self.df_terms = df_terms
        self.y = df['sentiment']
        self.n_samples = df['cleaned'].shape
        self.classes_ = np.unique(self.y)
        self.n_classes_ = self.classes_.shape[0]
        self.wn_classes_ = {x:0 for x in self.classes_}
        self.dn_classes_ = {x:0 for x in self.classes_}
        for i in self.classes_:
            self.wn_classes_[i] = df_terms['tfidf_'+i].sum()
            self.dn_classes_[i] = len(df[df['sentiment'] == i])
        self.class_priors_ = self._prior()
        
    def sum_wt_by_class(self,term,y):
        tfidf_c = 0
        index_of = self.df_terms.index[self.df_terms['term']==term].tolist()
        if len(index_of) > 0:
            if isinstance(self.df_terms['tfidf_'+y].iloc[index_of[0]],float):
                tfidf_c += self.df_terms['tfidf_'+y].iloc[index_of[0]]
        return np.log((tfidf_c+1) / (self.wn_classes_[y]+self.total_idf))
        
    def _likelyhood(self):
        self.wct_ = {}
        for i in self.classes_:
            self.predict_prior[i] = {}
            self.wct_[i] = {}
            for x_term in self.X_test.split():
                self.wct_[i][x_term] = self.sum_wt_by_class(x_term,i)
    
    def predict(self, X):
        self.predict_prior = {x:0 for x in self.classes_}
#         preprocess = PreProcessing()
        X_test_list = []
        X_test_proba = []
        
        for index,X_row in enumerate(X):
            self.predict_proba = {x:0 for x in self.classes_}
#             self.X_test = preprocess.callback(X_row)
            self.X_test = X_row
            self._likelyhood()
            
            for i in self.classes_:
                self.predict_prior[i] = self.pc[i]
                for x_term in self.X_test.split():
                    self.predict_prior[i] += self.wct_[i][x_term]
            for i in self.classes_: 
                self.predict_proba[i] = (100/sum(self.predict_prior.values()))*self.predict_prior[i]
            predicted = max(self.predict_prior, key=self.predict_prior.get)
            predict_proba = max(self.predict_proba.values())
            X_test_list.append(predicted)
            X_test_proba.append(predict_proba)
        self.predict_prob = pd.DataFrame(X_test_proba,columns=['proba'])
        return pd.DataFrame(X_test_list,columns=['sentiment'])