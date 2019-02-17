from django import forms

class DrinkerForm(forms.Form):
    drinker = forms.CharField(label = "", widget=forms.TextInput(attrs={'placeholder': 'Enter a drinker name','class':'form-control', 'list':'drinkerNames'}))
