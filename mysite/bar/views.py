from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import datetime
from bar.barQuery import Bar, getAllBarNames
from bar.forms import BarForm, TransactionForm
from django.shortcuts import render

def BarView(request):
    template_name = 'bar/index.html'

    if request.method == 'GET':
        form = BarForm()
        transaction_form = TransactionForm()
        bars = getAllBarNames()
        args = {
            'form': form,
            'transaction_form': transaction_form,
            'bars': bars,
        }
        return render(request, template_name, args)
    
    elif request.method == 'POST':
        form = BarForm(request.POST)
        transaction_form = TransactionForm(request.POST)
        bars = getAllBarNames()

        if transaction_form.is_valid():
            bar_name = transaction_form.cleaned_data['bar']
            bar = Bar(bar_name)
            print('TRANSACTION VALID')
            if bar.not_found:
                args = {'form': form,
                        'transaction_form': transaction_form,
                        'bars': bars,
                        'not_found': bar.not_found,
                }
            else:
                bar_name = bar.clean_bar_name
                top_drinkers_list = bar.getTopBarTransactions()
                top_items_sold = bar.getTopItems()
                sale_times = bar.getSalesByTime()

                args = {'form':form,
                        'transaction_form': transaction_form, 
                        'bars': bars,
                        'bar_name': bar_name, 
                        'name': top_drinkers_list['name'], 
                        'total': top_drinkers_list['total'],
                        'item_name': top_items_sold['item'],
                        'item_sold': top_items_sold['item_sold'],
                        'manf_name': top_items_sold['manf'],
                        'manf_sold': top_items_sold['manf_sold'],
                        'day': sale_times['weekday'],
                        'day_sold': sale_times['day_sold'],
                        'hour': sale_times['hour'],
                        'hour_sold': sale_times['hour_sold'],
                        }

        elif form.is_valid():
            bar_name = form.cleaned_data['bar']
            bar = Bar(bar_name)

            if bar.not_found:
                args = {'form': form,
                        'transaction_form': transaction_form,
                        'bars': bars,
                        'not_found': bar.not_found,
                }
            else:
                bar_name = bar.clean_bar_name
                top_drinkers_list = bar.getTopBarTransactions()
                top_items_sold = bar.getTopItems()
                sale_times = bar.getSalesByTime()

                args = {'form':form,
                        'transaction_form': transaction_form, 
                        'bars': bars,
                        'bar_name': bar_name, 
                        'name': top_drinkers_list['name'], 
                        'total': top_drinkers_list['total'],
                        'item_name': top_items_sold['item'],
                        'item_sold': top_items_sold['item_sold'],
                        'manf_name': top_items_sold['manf'],
                        'manf_sold': top_items_sold['manf_sold'],
                        'day': sale_times['weekday'],
                        'day_sold': sale_times['day_sold'],
                        'hour': sale_times['hour'],
                        'hour_sold': sale_times['hour_sold'],
                        }
        else:
            form = BarForm()
            args = {
                'form': form,
                'bars': bars,
            }
        
        return render(request, template_name, args)


    return HttpResponse(template.render({"error":"error"},request))

