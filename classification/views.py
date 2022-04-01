import json
import os
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from numpy import int32
import pandas as pd
from config.settings import BASE_DIR
from core.twitter import Twitter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, plot_confusion_matrix, classification_report, accuracy_score, f1_score, precision_score, recall_score
from django.core.paginator import Paginator
import joblib

from classification.forms import DataLatihForm
from classification.models import Account, Setting, Tweet
from core.classification import Classification

# Create your views here.
def dashboard(request):
    return render(request,'dashboard.html')

def data_latih(request):
    if request.method == "GET":
        details = DataLatihForm(request.GET)
        page = 1
        q_sentiment = request.GET.get('sentiment')
        
        previous_page = 1
        has_next = True
        has_previous = False
        if details.is_valid():
            page = int(details.data.get('page'))
        next_page = page+1
        per_page = 10
        limit = per_page*int(page)
        setting = Setting.objects.filter(id=1).first()
        classification = Classification(test_size=setting.model_type)
        page_count = int(len(classification.pembobotan_tweet)/10)
        

        if int(page) != 1 & int(page) <= int(page_count):
            previous_page = page-1
            has_next = True
            has_previous = True
        elif page > page_count:
            next_page = page_count
            previous_page = page_count-1
            has_next = False
            has_previous = True

        if request.GET.get('sentiment'):
            dataset = classification.pembobotan_tweet[classification.pembobotan_tweet['sentiment'] == q_sentiment][limit-per_page:limit]
        else:
            dataset = classification.pembobotan_tweet[limit-per_page:limit]

        context = {
            'dataset':dataset,
            'current_page':page,
            'next_page':next_page,
            'previous_page':previous_page,
            'has_next':has_next,
            'has_previous':has_previous,
            'page_count': page_count,
        }
        return render(request,'data_latih.html',context)

def preprocessing(request):
    if request.method == "GET":
        details = DataLatihForm(request.GET)
        page = 1
        q_sentiment = request.GET.get('sentiment')
        
        previous_page = 1
        has_next = True
        has_previous = False
        if details.is_valid():
            page = int(details.data.get('page'))
        next_page = page+1
        per_page = 10
        limit = per_page*int(page)
        setting = Setting.objects.filter(id=1).first()
        classification = Classification(test_size=setting.model_type)
        page_count = int(len(classification.pembobotan_tweet)/10)
        

        if int(page) != 1 & int(page) <= int(page_count):
            previous_page = page-1
            has_next = True
            has_previous = True
        elif page > page_count:
            next_page = page_count
            previous_page = page_count-1
            has_next = False
            has_previous = True

        if request.GET.get('sentiment'):
            dataset = classification.pembobotan_tweet[classification.pembobotan_tweet['sentiment'] == q_sentiment][limit-per_page:limit]
        else:
            dataset = classification.pembobotan_tweet[limit-per_page:limit]

        context = {
            'dataset':dataset,
            'current_page':page,
            'next_page':next_page,
            'previous_page':previous_page,
            'has_next':has_next,
            'has_previous':has_previous,
            'page_count': page_count,
        }
        return render(request,'preprocessing.html',context)

def term_frequency(request):
    if request.method == "GET":
        details = DataLatihForm(request.GET)
        setting = Setting.objects.filter(id=1).first()
        classification = Classification(test_size=setting.model_type)
        # Paginator Column
        pageColumn = int(details.data.get('pageColumn',1))
        perPageColumn = 6
        previous_column = 1
        has_previous_column = False
        has_next_column = pageColumn+1
        page_column_count = int(len(classification.pembobotan_tweet)/perPageColumn)
        first_index_column = 1
        last_index_column = perPageColumn
        if int(pageColumn) != 1 & int(pageColumn) <= int(page_column_count):
            previous_column = pageColumn-1
            has_next_column = True
            has_previous_column = True
            first_index_column = (pageColumn*perPageColumn)-(perPageColumn-1)
            last_index_column = pageColumn*perPageColumn
            columnDoc1 = 1
        elif pageColumn > page_column_count:
            messages.add_message(request, messages.WARNING, 'Out of range document.')
            next_page = page_column_count
            previous_page = page_column_count-1
            has_next_column = False
            has_previous_column = True
            first_index_column = (page_column_count*perPageColumn)-(perPageColumn-1)
            last_index_column = page_column_count*perPageColumn

        # Paginator
        page = int(details.data.get('page',1))
        previous_page = 1
        has_next = True
        has_previous = False
        next_page = page+1
        per_page = 10
        limit = per_page*int(page)
        page_count = int(len(classification.pembobotan_tf)/10)
            
        
        if int(page) != 1 & int(page) <= int(page_count):
            previous_page = page-1
            has_next = True
            has_previous = True
        elif page > page_count:
            messages.add_message(request, messages.WARNING, 'Out of range document.')
            next_page = page_count
            previous_page = page_count-1
            has_next = False
            has_previous = True


        context = {
            # 'dataset':classification.dataset[limit-per_page:limit],
            'tfidf':classification.pembobotan_tf[limit-per_page:limit],
            'current_page':page,
            'next_page':next_page,
            'previous_page':previous_page,
            'has_next':has_next,
            'has_previous':has_previous,
            'page_count': page_count,
            'previous_column': previous_column,
            'has_next_column':has_next_column,
            'has_previous_column':has_previous_column,
            'first_index_column':first_index_column,
            'last_index_column':last_index_column
        }
        return render(request,'term_frequency.html',context)

def tf_idf(request):
    if request.method == "GET":
        details = DataLatihForm(request.GET)
        setting = Setting.objects.filter(id=1).first()
        classification = Classification(test_size=setting.model_type)
        # Paginator Column
        pageColumn = int(details.data.get('pageColumn',1))
        perPageColumn = 6
        previous_column = 1
        has_previous_column = False
        has_next_column = pageColumn+1
        page_column_count = int(len(classification.pembobotan_tweet)/perPageColumn)
        first_index_column = 1
        last_index_column = perPageColumn
        if int(pageColumn) != 1 & int(pageColumn) <= int(page_column_count):
            previous_column = pageColumn-1
            has_next_column = True
            has_previous_column = True
            first_index_column = (pageColumn*perPageColumn)-(perPageColumn-1)
            last_index_column = pageColumn*perPageColumn
            columnDoc1 = 1
        elif pageColumn > page_column_count:
            messages.add_message(request, messages.WARNING, 'Out of range document.')
            next_page = page_column_count
            previous_page = page_column_count-1
            has_next_column = False
            has_previous_column = True
            first_index_column = (page_column_count*perPageColumn)-(perPageColumn-1)
            last_index_column = page_column_count*perPageColumn

        # Paginator
        page = int(details.data.get('page',1))
        previous_page = 1
        has_next = True
        has_previous = False
        next_page = page+1
        per_page = 10
        limit = per_page*int(page)
        page_count = int(len(classification.pembobotan_tfidf)/10)
            
        
        if int(page) != 1 & int(page) <= int(page_count):
            previous_page = page-1
            has_next = True
            has_previous = True
        elif page > page_count:
            messages.add_message(request, messages.WARNING, 'Out of range document.')
            next_page = page_count
            previous_page = page_count-1
            has_next = False
            has_previous = True


        context = {
            # 'dataset':classification.dataset[limit-per_page:limit],
            'tfidf':classification.pembobotan_tfidf[limit-per_page:limit],
            'current_page':page,
            'next_page':next_page,
            'previous_page':previous_page,
            'has_next':has_next,
            'has_previous':has_previous,
            'page_count': page_count,
            'previous_column': previous_column,
            'has_next_column':has_next_column,
            'has_previous_column':has_previous_column,
            'first_index_column':first_index_column,
            'last_index_column':last_index_column
        }
        return render(request,'tfidf.html',context)

def akun(request):
    if request.method == "GET":
        context = {
            'accounts' : Account.objects.all()
        }
        return render(request,'akun.html',context)
    if request.method == "POST":
        username = request.POST.get("username")

        twitter = Twitter()
        twitter.account(username)
        twitter.search(username)
        
        return redirect('akun')

def setting(request):
    if request.method == "GET":
        setting = Setting.objects.filter(id=1).first()
        classification = Classification(test_size=setting.model_type)
        total_document = len(classification.preprocessing_test)+len(classification.preprocessing_train)
        merge_df = pd.concat([classification.preprocessing_train,classification.preprocessing_test])
        total_positive = len(merge_df[merge_df['sentiment'] == 'positive'])
        total_negative = len(merge_df[merge_df['sentiment'] == 'negative'])
        total_neutral = len(merge_df[merge_df['sentiment'] == 'neutral'])
        context = {
            'setting':setting,
            'total_document':total_document,
            'total_positive':total_positive,
            'total_negative':total_negative,
            'total_neutral':total_neutral,
        }
        return render(request,'setting.html',context)
    
    if request.method == "POST":
        model_type = request.POST.get("model_type",2)
        threshold_min = request.POST.get("threshold_min",1)
        threshold_max = request.POST.get("threshold_max")
        if threshold_max is None or threshold_max == 0:
            threshold_max = 1.0
        else:
            threshold_max = int(threshold_max)
        classification = Classification(test_size=model_type)
        vectorizer = TfidfVectorizer(smooth_idf=True,norm=None,min_df=int(threshold_min),max_df=threshold_max)
        X_train = vectorizer.fit_transform(classification.preprocessing_train['cleaned'])
        y_train = classification.preprocessing_train['sentiment']
        y_test = classification.preprocessing_test['sentiment']
        X_test = vectorizer.transform(classification.preprocessing_test['cleaned'])
        
        classifier = MultinomialNB()
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)
        _confusion = confusion_matrix(y_test, y_pred)
        _accuracy_score = accuracy_score(y_test, y_pred)
        _precision_score = precision_score(y_test, y_pred,average=None)
        _recall_score = recall_score(y_test, y_pred,average=None)
        _f1_score = f1_score(y_test, y_pred,average=None)

        model_dump = {'vectorizer': vectorizer, 'classifier': classifier, 'accuracy_score': _accuracy_score, 'confusion_matrix': _confusion,'precision_score':_precision_score,'recall':_recall_score,'f1':_f1_score}
        joblib.dump(model_dump, open(os.path.join(BASE_DIR, "core/data/dataset_"+model_type)+"/sklearn.model", "wb"))

        data = {
            'model_type':model_type,
            'threshold_min':threshold_min,
            'threshold_max':threshold_max,
            'accuracy_score':round(_accuracy_score,2)*100,
            'precision_score':{'negative':round(float(_precision_score[0]),2),'neutral':round(float(_precision_score[1]),2),'positive':round(float(_precision_score[2]),2)},
            'recall_score':{'negative':round(float(_recall_score[0]),2),'neutral':round(float(_recall_score[1]),2),'positive':round(float(_recall_score[2]),2)},
            'f1_score':{'negative':round(float(_f1_score[0]),2),'neutral':round(float(_f1_score[1]),2),'positive':round(float(_f1_score[2]),2)},
        }
        print(accuracy_score(y_test, y_pred))
        
        setting = Setting.objects.update_or_create(
                        id = 1,
                        defaults=data
                    )
        if setting:
            Setting.objects.filter(id=1).update(is_active=0)
            Setting.objects.filter(model_type=model_type).update(is_active=1)
        return redirect('setting')

def akun_detail(request,username):
    if request.method == "GET":
        details = DataLatihForm(request.GET)
        page = int(details.data.get('page',1))
        q_sentiment = request.GET.get('sentiment')
        
        previous_page = 1
        has_next = True
        has_previous = False
        next_page = page+1
        per_page = 10
        limit = per_page*int(page)
        account = Account.objects.filter(username=username).first()
        tweet = Tweet.objects.filter(mention_to=username)
        page_count = int(tweet.count()/10)

        if q_sentiment is not None:
            if q_sentiment == 'positive':
                tweet = tweet.filter(sentiment=1)
            elif q_sentiment == 'negative':
                tweet = tweet.filter(sentiment=2)
            else:
                tweet = tweet.filter(sentiment=0)
            

        if int(page) != 1 & int(page) <= int(page_count):
            previous_page = page-1
            has_next = True
            has_previous = True
        elif page > page_count:
            next_page = page_count
            previous_page = page_count-1
            has_next = False
            has_previous = True

        paginator = Paginator(tweet.values(), 10)
        results = paginator.page(page)

        total_document = tweet.count()
        total_positive = tweet.filter(sentiment=1).count()
        total_negative = tweet.filter(sentiment=2).count()
        total_neutral = tweet.filter(sentiment=0).count()
        context = {
            'account':account,
            'tweet':results.object_list,
            'current_page':page,
            'next_page':next_page,
            'previous_page':previous_page,
            'has_next':has_next,
            'has_previous':has_previous,
            'page_count': page_count,
            'total_document':total_document,
            'total_positive':total_positive,
            'total_negative':total_negative,
            'total_neutral':total_neutral,
        }
        return render(request,'akun_detail.html',context)

def manual(request):
    if request.method == "GET":
        return render (request,'manual.html')
    if request.method == "POST":
        text = request.POST.get("text","")
        setting = Setting.objects.filter(id=1).first()
        classification = Classification(test_size=setting.model_type)
        tweet_cleaned = classification.clean_text(text)
        sentiment = classification.nb.predict([tweet_cleaned])
        class_priors = classification.nb.class_priors_
        dn_classes = classification.nb.dn_classes_ #document class
        predict_prior = classification.nb.predict_prior
        total_wc = classification.nb.wn_classes_
        total_idf = classification.nb.total_idf
        pc = classification.nb.pc
        wct = classification.nb.wct_
        context = {
            'sentiment':sentiment['sentiment'][0],
            'class_priors':class_priors,
            'predict_prior':predict_prior,
            'total_wc':total_wc,
            'total_idf':total_idf,
            'dn_classes':dn_classes,
            'pc':pc,
            'wct':wct,
            'text':text,
        }
        return render (request,'manual.html',context)