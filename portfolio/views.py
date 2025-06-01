from django.shortcuts import render # Import render for rendering templates
from django.http import HttpResponse # Import HttpResponse for returning responses
from django.template import loader # Import loader for rendering templates
from django.db.models import Count # Import Count for aggregating data
from django.db.models import Prefetch # Import Prefetch for optimizing queries
from .models import User, ProjectCategory, SkillCategory, Skill # Import necessary models

# Create your views here.

# This view function handles the portfolio page for a user.
def portfolio(request):
    # User data 
    person = User.objects.get(id=1)
    person.tag_items = person.tag_line.split(' | ')
    
    # Services of the user
    services = person.services.all()
    
    # Classifications of the user
    certifications = person.certifications.all()
    
    # Projects for the user
    projects = person.projects.all()
    
    # Get all used project categories
    projects_used_categories = (
        ProjectCategory.objects
        .filter(project__user=person)
        .annotate(occurrence=Count('project'))
        .distinct()
    )
    
    # Get all educations for the user
    educations = person.educations.all()
    
    # Get all skills for the user
    
    
    # Skills grouped by category
    skill_categories = SkillCategory.objects.prefetch_related(
        Prefetch('skills', queryset=Skill.objects.filter(user=person))
    ).filter(skills__user=person).distinct()
    
    context = {
        'person': person,
        'services': services,
        'certifications' : certifications,
        'projects': projects,
        'projects_used_categories' : projects_used_categories,
        'educations': educations,
        'skill_categories': skill_categories,
        }
    template = loader.get_template('intro.html')
    return HttpResponse(template.render(context, request))
