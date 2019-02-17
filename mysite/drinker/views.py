from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import datetime
from drinker.drinkerQuery import getFinalTransaction, getSpendingFromName, getMostItemsOrderedFromName, getFinalSpending, Drinker, getAllDrinkerNames
from drinker.forms import DrinkerForm
from django.shortcuts import render
from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
# Create your views here.

def DrinkerView(request):
    template_name = 'drinker/index.html'
    template = loader.get_template(template_name)
    print(request.method)

    if request.method == 'GET':
        form = DrinkerForm()
        drinkers = getAllDrinkerNames()

        args = {
            'form': form,
            'drinkers': drinkers,
        }
        return render(request, template_name, args)

    if request.method == 'POST':
        form = DrinkerForm(request.POST)
        name = "default"

        drinkers = getAllDrinkerNames()

        if form.is_valid():
            name = form.cleaned_data['drinker']
            drinker = Drinker(name)
            if drinker.not_found:
                args = {'form': form,
                        'not_found': drinker.not_found,
                }
            else:
                name = drinker.clean_drinker_name
                print(drinker.d_id)
                transactions = drinker.getDrinkersTransactions()
                most_items_raw = getMostItemsOrderedFromName(name)[:10]
                most_items_x = [x[0] for x in most_items_raw]
                most_items_y = [x[1] for x in most_items_raw]
                date_time, week_time, month_time = getFinalSpending(name)
                
                date_time_data = list()
                date_time_label = list(date_time.keys())
                for d in date_time_label:
                    date_time_data.append(date_time[d])
                
                week_time_data = list()
                week_time_label = sorted(list(week_time.keys()))
                for l in week_time_label:
                    week_time_data.append(week_time[l])
                week_time_label = ["Week: " + str(x) for x in week_time_label] 

                month_time_data = list()
                month_time_label = sorted(list(month_time.keys()))
                for m in month_time_label:
                    month_time_data.append(month_time[m])
                month_time_label = ["Month: " + str(x) for x in month_time_label] 
                print(transactions[1])
                args = {
                    'form':form, 
                    'name': name, 
                    'transactions': transactions[0],
                    'items_on_transaction': transactions[1],
                    'most_items_x':most_items_x, 
                    'most_items_y':most_items_y, 
                    'date_time_label':date_time_label,
                    'date_time_data':date_time_data, 
                    'week_time_label':week_time_label,
                    'week_time_data':week_time_data, 
                    'month_time_label':month_time_label,
                    'month_time_data':month_time_data,
                    'drinkers': drinkers,
                }
        return render(request, template_name, args)

    print("\n\n\nShould not be here\n\n\n")
    return HttpResponse(template.render(context,request))

def HomeView(request):
    template_name = 'drinker/home.html'
    template = loader.get_template(template_name)
    print(request.method)

    if request.method == 'GET':

        args = {
        }
        return render(request, template_name, args)