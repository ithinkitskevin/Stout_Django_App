from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# def validate_bar_name(value):
#         word_count = len(value.split())
#         print(word_count)
#         if word_count != 3 or word_count != 5:
#             raise ValidationError(_("Invalid Input"), code = "invalid input")


class BarForm(forms.Form):

    bar = forms.CharField(label = "", widget=forms.TextInput(attrs={'placeholder': 'Enter a bar name','class':'form-control barInput', 'list':'barNames'})) 

class TransactionForm(forms.Form):

    bar = forms.CharField(label = "", widget=forms.TextInput(attrs={'placeholder': 'Enter a bar name','class':'form-control barInput', 'list':'barNames'})) 
    total_price = forms.FloatField(label = "", widget=forms.TextInput(attrs={'placeholder': 'Enter the total amount','class':'form-control barInput'})) 
    tip = forms.FloatField(label = "", widget=forms.TextInput(attrs={'placeholder': 'Enter the tip','class':'form-control barInput'})) 
    d_id = forms.CharField(label = "", widget=forms.TextInput(attrs={'placeholder': 'Enter a drinker id','class':'form-control barInput', 'list':'barNames'})) 
