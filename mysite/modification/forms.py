from django import forms

class BarForm(forms.Form):
    bar = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter a query for Bars Table','class':'form-control'}), error_messages={'required': 'Query in the Other Table'})

class DrinkerForm(forms.Form):
    drinker = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter a query for Drinkers Table','class':'form-control'}), error_messages={'required': 'Query in the Other Table'})

class FrequentForm(forms.Form):
    frequent = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter a query for Frequents Table','class':'form-control'}), error_messages={'required': 'Query in the Other Table'})

class HourForm(forms.Form):
    hour = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter a query for Hours Table','class':'form-control'}), error_messages={'required': 'Query in the Other Table'})

class ItemForm(forms.Form):
    item = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter a query for Items Table','class':'form-control'}), error_messages={'required': 'Query in the Other Table'})

class ItemSoldForm(forms.Form):
    item_sold = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter a query for Items_Sold Table','class':'form-control'}), error_messages={'required': 'Query in the Other Table'})

class LikeForm(forms.Form):
    like = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter a query for Likes Table','class':'form-control'}), error_messages={'required': 'Query in the Other Table'})

class SellForm(forms.Form):
    sell = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter a query for Sells Table','class':'form-control'}), error_messages={'required': 'Query in the Other Table'})

class TransactionForm(forms.Form):
    transaction = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter a query for Transactions Table','class':'form-control'}), error_messages={'required': 'Query in the Other Table'})


