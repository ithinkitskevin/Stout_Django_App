from django import forms

class BeerForm(forms.Form):
    beer = forms.CharField(label = "", widget=forms.TextInput(attrs={'placeholder': 'Enter an item name','class':'form-control','list':'itemNames'})) 
 