# File: portfolio/views.py

from django.shortcuts import render, redirect # Import render for rendering templates
from django.http import HttpResponse # Import HttpResponse for returning responses
from django.template import loader # Import loader for rendering templates
from django.db.models import Count, Prefetch # Import Count for aggregating data, Prefetch for optimizing queries
from .models import User, ProjectCategory, SkillCategory, Skill, Contact # Import necessary models
from django.contrib import messages # Import messages for user feedback
from .forms import ContactForm # Import the ContactForm for handling contact messages

# Create your views here.

# This view function handles the portfolio page for a user.
def landing_page_view(request):
    # User data 
    person = User.objects.get(id=2)
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
    
    
    # Get all skills category for the user
    used_skills_categories = (
        SkillCategory.objects
        .filter(skills__user=person)
        .annotate(occurrence=Count('skills'))
        .distinct()
    )
    
    # Skills grouped by category
    used_skills_categories = SkillCategory.objects.prefetch_related(
        Prefetch('skills', queryset=Skill.objects.filter(user=person))
    ).filter(skills__user=person).distinct()
    
    # Skills grouped by category
    skill_categories = SkillCategory.objects.prefetch_related(
        Prefetch('skills', queryset=Skill.objects.filter(user=person))
    ).filter(skills__user=person).distinct()
    
    # Skills grouped by category
    experiences = person.experiences.all()
    
    # Contact Form
    contact_form = ContactForm()
    
    # Prepare the context for rendering the template
    context = {
        'person': person,
        'services': services,
        'certifications' : certifications,
        'projects': projects,
        'projects_used_categories' : projects_used_categories,
        'educations': educations,
        'skill_categories': skill_categories,
        'used_skills_categories': used_skills_categories,
        'experiences': experiences,
        'contact_form': contact_form,
        }
    
    return render(request, 'intro.html', context)



# Save contact form submission
def save_contact_message(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            person = User.objects.get(id=1)
            Contact.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
                user=person
            )
            messages.success(request, "Your message has been sent successfully.")
        else:
            messages.error(request, "Please correct the errors in the form.")
    
    return redirect('/#contact')
