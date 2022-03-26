from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from core.twitter import Twitter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, plot_confusion_matrix, classification_report, accuracy_score, f1_score, precision_score, recall_score
from django.core.paginator import Paginator

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
        
        previous_page = 1
        has_next = True
        has_previous = False
        if details.is_valid():
            page = int(details.data.get('page'))
        next_page = page+1
        per_page = 10
        limit = per_page*int(page)
        classification = Classification()
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


        context = {
            'dataset':classification.pembobotan_tweet[limit-per_page:limit],
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
        
        previous_page = 1
        has_next = True
        has_previous = False
        if details.is_valid():
            page = int(details.data.get('page'))
        next_page = page+1
        per_page = 10
        limit = per_page*int(page)
        classification = Classification()
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


        context = {
            'dataset':classification.pembobotan_tweet[limit-per_page:limit],
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
        classification = Classification()
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
        classification = Classification()
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
        
        return render(request,'setting.html')
    
    if request.method == "POST":
        classification = Classification(test_size=request.POST.get("model_type"))
        vectorizer = TfidfVectorizer(smooth_idf=True,norm=None,min_df=int(request.POST.get("threshold_min",1)),max_df=int(request.POST.get("threshold_max",10000)))
        X_vect = vectorizer.fit_transform(classification.preprocessing_train['cleaned'])
        
        classifier = MultinomialNB()
        classifier.fit(X_vect, classification.preprocessing_train['sentiment'])
        y_test = classification.preprocessing_test['cleaned']
        X_test_vect = vectorizer.transform(y_test)
        y_pred = classifier.predict(X_test_vect) 
        acc = accuracy_score(y_test, y_pred)

        data = {
            'model_type':request.POST.get("model_type"),
            'threshold_min':request.POST.get("threshold_min"),
            'threshold_max':request.POST.get("threshold_max"),
            'accuracy_score':acc*100,
        }
        
        setting = Setting.objects.update_or_create(
                        model_type = request.POST.get("model_type"),
                        defaults=data
                    )
        if setting:
            Setting.objects.filter(is_active=1).update(is_active=0)
            Setting.objects.filter(model_type=request.POST.get("model_type")).update(is_active=1)
        return redirect('setting')

def akun_detail(request,username):
    if request.method == "GET":
        details = DataLatihForm(request.GET)
        page = page = int(details.data.get('page',1))
        
        previous_page = 1
        has_next = True
        has_previous = False
        next_page = page+1
        per_page = 10
        limit = per_page*int(page)
        tweet = Tweet.objects
        page_count = int(tweet.count()/10)

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
        context = {
            'tweet':results.object_list,
            'current_page':page,
            'next_page':next_page,
            'previous_page':previous_page,
            'has_next':has_next,
            'has_previous':has_previous,
            'page_count': page_count,
        }
        return render(request,'akun_detail.html',context)