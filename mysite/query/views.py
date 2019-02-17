from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from query.queryQuery import getResultFromQuery
from query.forms import QueryForm

def QueryView(request):
    template_name = 'query/index.html'
    template = loader.get_template(template_name)

    if request.method == 'GET':
        form = QueryForm()
        return render(request, template_name, {'form':form})
    if request.method == 'POST':
        form = QueryForm(request.POST)
        query = "Enter Query"
        if form.is_valid():
            query = form.cleaned_data['query']
        query_result = getResultFromQuery(query)
        args = {'form':form, 'query': query, 'query_result':query_result}
        return render(request, template_name, args)

    return HttpResponse(template.render(context,request))
