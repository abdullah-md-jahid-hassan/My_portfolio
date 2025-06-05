from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
from django.db.models import Prefetch # Import Prefetch for optimizing queries
from landing_spot.models import User, Skill, SkillCategory, Project
from resume.models import Resume, ResumeProject

# Create your views here.



def pdf_resume_view(request, username, action):
    # User data 
    person = User.objects.get(username=username)
    if not person:
        return HttpResponse("User not found.", status=404)
    
    # Get the active resume for the user
    resume =person.resumes.filter(is_active=True).first()
    if not resume:
        return HttpResponse("No active resume found for this user.", status=404)
    
    # Skills grouped by category
    skill_categories = SkillCategory.objects.prefetch_related(
        Prefetch('skills', queryset=Skill.objects.filter(user=person))
    ).filter(skills__user=person).distinct()

    projects = Project.objects.filter(resume_projects__resume=resume).order_by('-resume_projects__hierarchy')

    
    # Prepare the context for rendering the template
    context = {
        'person': person,
        'resume': resume,
        'skill_categories': skill_categories,
        'projects': projects,
        }
    
    return render(request, 'resume_pdf.html', context)