from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from modification.modQuery import getResultFromQuery
from modification.forms import DrinkerForm, TransactionForm, BarForm, FrequentForm, HourForm, ItemForm, ItemSoldForm, LikeForm, SellForm
import re

def ModView(request):
    template_name = 'modification/index.html'
    template = loader.get_template(template_name)

    if request.method == 'GET':
        bar = BarForm()
        drinker = DrinkerForm()
        frequent = FrequentForm()
        hour = HourForm()
        item = ItemForm()
        item_sold = ItemSoldForm()
        like = LikeForm()
        sell = SellForm()
        transaction = TransactionForm()
        
        return render(request, template_name, {'bar':bar, 'drinker':drinker, 'frequent':frequent, 'hour':hour, 'item':item,  'item_sold':item_sold,'like':like, 'sell':sell, 'transaction':transaction})
    if request.method == 'POST':
        bar = BarForm(request.POST)
        drinker = DrinkerForm(request.POST)
        frequent = FrequentForm(request.POST)
        hour = HourForm(request.POST)
        item = ItemForm(request.POST)
        item_sold = ItemSoldForm(request.POST)
        like = LikeForm(request.POST)
        sell = SellForm(request.POST)
        transaction = TransactionForm(request.POST)

        args = {'bar':bar, 'drinker':drinker, 'frequent':frequent, 'hour':hour, 'item':item,  'item_sold':item_sold,'like':like, 'sell':sell, 'transaction':transaction,'query': 'No Query'}

        if bar.is_valid():
            query = bar.cleaned_data['bar']
            query_result = ""
            tmp_query = query.replace(';',' ')
            if 'Bars' in tmp_query.split():
                query_result = getResultFromQuery(query)
            else:
                query_result = "Invalid Bars Table"
            args = {'bar':bar, 'drinker':drinker.save(), 'frequent':frequent, 'hour':hour, 'item':item,  'item_sold':item_sold,'like':like, 'sell':sell, 'transaction':transaction,'query': query, 'query_result_bar':query_result}
        elif drinker.is_valid():
            query = drinker.cleaned_data['drinker']
            query_result = ""
            tmp_query = query.replace(';',' ')
            if 'Drinkers' in tmp_query.split():
                query_result = getResultFromQuery(query)
            else:
                query_result = "Invalid Drinkers Table"
            args = {'bar':bar, 'drinker':drinker, 'frequent':frequent, 'hour':hour, 'item':item,  'item_sold':item_sold,'like':like, 'sell':sell, 'transaction':transaction,'query': query, 'query_result_drinker':query_result}
        elif frequent.is_valid():
            query = frequent.cleaned_data['frequent']
            query_result = ""
            tmp_query = query.replace(';',' ')
            if 'Frequents' in tmp_query.split():
                query_result = getResultFromQuery(query)
            else:
                query_result = "Invalid Frequents Table"
            args = {'bar':bar, 'drinker':drinker, 'frequent':frequent, 'hour':hour, 'item':item,  'item_sold':item_sold,'like':like, 'sell':sell, 'transaction':transaction,'query': query, 'query_result_frequent':query_result}
        elif hour.is_valid():
            query = hour.cleaned_data['hour']
            query_result = ""
            tmp_query = query.replace(';',' ')
            if 'Hours' in tmp_query.split():
                query_result = getResultFromQuery(query)
            else:
                query_result = "Invalid Hours Table"
            args = {'bar':bar, 'drinker':drinker, 'frequent':frequent, 'hour':hour, 'item':item,  'item_sold':item_sold,'like':like, 'sell':sell, 'transaction':transaction,'query': query, 'query_result_hour':query_result}
        elif item.is_valid():
            query = item.cleaned_data['item']
            query_result = ""
            tmp_query = query.replace(';',' ')
            if 'Items' in tmp_query.split():
                query_result = getResultFromQuery(query)
            else:
                query_result = "Invalid Items Table"
            args = {'bar':bar, 'drinker':drinker, 'frequent':frequent, 'hour':hour, 'item':item,  'item_sold':item_sold,'like':like, 'sell':sell, 'transaction':transaction,'query': query, 'query_result_item':query_result}
        elif item_sold.is_valid():
            query = item_sold.cleaned_data['item_sold']
            query_result = ""
            tmp_query = query.replace(';',' ')
            if 'Items_Sold' in tmp_query.split():
                query_result = getResultFromQuery(query)
            else:
                query_result = "Invalid Items_Sold Table"
            args = {'bar':bar, 'drinker':drinker, 'frequent':frequent, 'hour':hour, 'item':item,  'item_sold':item_sold,'like':like, 'sell':sell, 'transaction':transaction,'query': query, 'query_result_item_sold':query_result}
        elif like.is_valid():
            query = like.cleaned_data['like']
            query_result = ""
            tmp_query = query.replace(';',' ')
            if 'Likes' in tmp_query.split():
                query_result = getResultFromQuery(query)
            else:
                query_result = "Invalid Likes Table"
            args = {'bar':bar, 'drinker':drinker, 'frequent':frequent, 'hour':hour, 'item':item,  'item_sold':item_sold,'like':like, 'sell':sell, 'transaction':transaction,'query': query, 'query_result_like':query_result}
        elif sell.is_valid():
            query = sell.cleaned_data['sell']
            query_result = ""
            tmp_query = query.replace(';',' ')
            if 'Sells' in tmp_query.split(' '):
                query_result = getResultFromQuery(query)
            else:
                query_result = "Invalid Sells Table"
            args = {'bar':bar, 'drinker':drinker, 'frequent':frequent, 'hour':hour, 'item':item,  'item_sold':item_sold,'like':like, 'sell':sell, 'transaction':transaction,'query': query, 'query_result_sell':query_result}
        elif transaction.is_valid():
            query = transaction.cleaned_data['transaction']
            query_result = ""
            tmp_query = query.replace(';',' ')
            if 'Transactions' in tmp_query.split():
                query_result = getResultFromQuery(query)
            else:
                query_result = "Invalid Transactions Table"
            args = {'bar':bar, 'drinker':drinker, 'frequent':frequent, 'hour':hour, 'item':item,  'item_sold':item_sold,'like':like, 'sell':sell, 'transaction':transaction,'query': query, 'query_result_transaction':query_result}
        
        return render(request, template_name, args)        

    return HttpResponse(template.render(context,request))


'''

print(request.POST)
        drinker = DrinkerForm(request.POST)
        transaction = TransactionForm(request.POST)

        # print('drinker',drinker['query'])
        # print('transaction',transaction['query'])
        query = "Enter Query"

        if drinker.is_valid():
            query = drinker.cleaned_data['drinker']
            print('drinker',query)
            query_result = getResultFromQuery(query)
            args = {'form':drinker,'other_form':transaction, 'query': query, 'query_result':query_result}

            return render(request, template_name, args)
        if transaction.is_valid():
            query = transaction.cleaned_data['transaction']
            print('transaction',query)
            query_result = getResultFromQuery(query)
            args = {'form':transaction, 'other_form':drinker, 'query': query, 'query_result':query_result}
        
            return render(request, template_name, args)
'''