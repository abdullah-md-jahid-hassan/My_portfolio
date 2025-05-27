from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import User, ProjectCategory

# Create your views here.

# This view function handles the portfolio page for a user.
def portfolio(request):
    # User data 
    person = User.objects.get(id=1)
    person.tag_items = person.tag_line.split(' | ')
    
    # Services of the user
    services = person.services.all()
    
    # Skills of the user
    skills = person.skills.all()
    
    # Classifications of the user
    certifications = person.certifications.all()
    
    # Projects for the user
    projects = person.projects.all()
    
    # Get all used project categories
    projects_used_categories = list(ProjectCategory.objects.filter(project__user=person).distinct())
    
    context = {
        'person': person,
        'services': services,
        'skills': skills,
        'certifications' : certifications,
        'projects': projects,
        'projects_used_categories' : projects_used_categories,
        }
    template = loader.get_template('intro.html')
    return HttpResponse(template.render(context, request))
