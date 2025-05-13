from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def portfolio(request):
    template = loader.get_template('intro.html')
    return HttpResponse(template.render())
