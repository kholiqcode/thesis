from django.shortcuts import render

from classification.forms import DataLatihForm

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
        page_count = int(len(classification.dataset)/10)
        

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
            'dataset':classification.dataset[limit-per_page:limit],
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
        page_count = int(len(classification.dataset)/10)
        

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
            'dataset':classification.dataset[limit-per_page:limit],
            'current_page':page,
            'next_page':next_page,
            'previous_page':previous_page,
            'has_next':has_next,
            'has_previous':has_previous,
            'page_count': page_count,
        }
        return render(request,'preprocessing.html',context)