
from django import forms
 
# define the class of a form
class DataLatihForm(forms.Form):
    page = forms.IntegerField(required=True)