from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from beer.beerQuery import Beer, getAllItemNames
from beer.forms import BeerForm
from django.shortcuts import render

def BeerView(request):
    template_name = 'beer/index.html'
    template = loader.get_template(template_name)

    if request.method == 'GET':
        form = BeerForm()
        items = getAllItemNames()

        args = {'form': form,
                'items': items,
                }

        return render(request, template_name, args)
    elif request.method == 'POST':
        form = BeerForm(request.POST)
        items = getAllItemNames()

        if form.is_valid():
            beer_name = form.cleaned_data['beer']
            beer = Beer(beer_name)
            beer_name = beer.clean_item_name

            if beer.not_found:
                args = {'form': form,
                        'items': items,
                        'not_found': beer.not_found,
                        'items': items,
                }
            else:
                top_sold = beer.getTopSold()
                top_consumed = beer.getTopConsumers()
                sale_times = beer.getSalesByTime()

                args = {'form':form, 
                        'name': beer_name, 
                        'bar' : top_sold['bar'], 
                        'amount_sold': top_sold['amount_sold'],
                        'drinker_name' : top_consumed['drinker_name'], 
                        'amount_consumed': top_consumed['amount_consumed'],
                        'day': sale_times['weekday'],
                        'day_sold': sale_times['day_sold'],
                        'hour': sale_times['hour'],
                        'hour_sold': sale_times['hour_sold'],
                        'items': items,
                        }
        else:
            args = {'form': form,
                    'items': items,
                }

        return render(request, template_name, args)

    return HttpResponse(template.render({"error":"error"},request))