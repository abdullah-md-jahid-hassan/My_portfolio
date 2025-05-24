from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import User

# Create your views here.
def portfolio(request):
    person = User.objects.get(id=1)
    context = { 'person': person }
    template = loader.get_template('intro.html')
    return HttpResponse(template.render(context, request))
