# File: Landing_spot/views.py

from django.shortcuts import render, redirect, get_object_or_404 # Import render for rendering templates
from django.http import HttpResponse # Import HttpResponse for returning responses
from django.template import loader # Import loader for rendering templates
from django.db.models import Count, Prefetch # Import Count for aggregating data, Prefetch for optimizing queries
from .models import User, ProjectCategory, SkillCategory, Skill, Contact, Project # Import necessary models
from django.contrib import messages # Import messages for user feedback
from .forms import ContactForm # Import the ContactForm for handling contact messages

#local methods
def landing_page(request, person):
    # User data 
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

    
    
    
# Create your views here.

# view function for owner. Use root address.
def owner_portfolio(request):
    # User data 
    person = User.objects.get(id=2)
    
    return landing_page(request, person)



# view function for general user. root/portfolio/username.
def other_portfolio(request, username):
    # User data 
    person = User.objects.get(username=username)
    
    return landing_page(request, person)



# Save contact form submission
def save_contact_message(request, username):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            person = User.objects.get(username=username)
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
    
    return redirect(f'/portfolio/{username}#contact')




# view function for project details
def Project_Details(request, username, slug):
    # Get the project by slug and username
    project = get_object_or_404(Project, slug=slug, user__username=username)
    project.user_phone = project.user.phone
    project.user_email = project.user.email
    root_url = request.build_absolute_uri('/')
    previous_page = request.META.get('HTTP_REFERER', '/')
    
    context = {
        'project': project,
        'username': username,
        'previous_page': previous_page,
        }
    
    return render(request, 'project_details.html', context)