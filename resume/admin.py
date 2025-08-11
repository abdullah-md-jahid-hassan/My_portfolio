# file: resume/admin.py

from django.contrib import admin
from django import forms
from .models import Resume, Reference, ResumeProject, ResumeCertificate, ResumeReference

from my_portfolio.utils.permission_utils import Restricted_if_not_supper

# Registering the Resume model with the admin site
class ResumeAdminForm(forms.ModelForm):
    # Custom form for the Project model to handle the toggle switch for is_active field
    class Meta:
        model = Resume
        fields = '__all__'
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle-switch'}),
        }

    # Custom media for the admin form to include toggle switch CSS
    class Media:
        css = {
            'all': ('portfolio/css/toggle.css',) 
        }
        
        
# class for the Resume Project inline in the Resume admin
class ResumeProjectInline(Restricted_if_not_supper, admin.TabularInline):
    model = ResumeProject
    extra = 1
    autocomplete_fields = ['project']
        
        
# class for the Resume Project inline in the Resume admin
class ResumeCertificateInline(Restricted_if_not_supper, admin.TabularInline):
    model = ResumeCertificate
    extra = 1
    autocomplete_fields = ['certificate']
        
        
# class for the Resume Reference inline in the Resume admin
class ResumeReferenceInline(Restricted_if_not_supper, admin.TabularInline):
    model = ResumeReference
    extra = 1
    autocomplete_fields = ['reference']


@admin.register(Reference)
class ReferenceAdmin(Restricted_if_not_supper, admin.ModelAdmin):
    list_display = ('id', 'name', 'designation', 'email', 'phone', 'user')
    search_fields = ('name', 'designation', 'email', 'user__username')


@admin.register(Resume)
class ResumeAdmin(Restricted_if_not_supper, admin.ModelAdmin):
    form = ResumeAdminForm
    
    list_display = ('id', 'name', 'user', 'is_active')
    search_fields = ('name', 'user__username', 'user__email')
    list_filter = ('is_active', 'user')
    inlines = [ResumeProjectInline, ResumeCertificateInline, ResumeReferenceInline]


# # Registering the ResumeProject model with the admin site
# @admin.register(ResumeProject)
# class ResumeProjectAdmin(Restricted_if_not_supper, admin.ModelAdmin):
#     list_display = ('resume', 'project', 'hierarchy')
#     list_filter = ('resume',)
#     search_fields = ('resume__name', 'project__title')


# # Registering the ResumeReference model with the admin site
# @admin.register(ResumeReference)
# class ResumeReferenceAdmin(Restricted_if_not_supper, admin.ModelAdmin):
#     list_display = ('resume', 'reference', 'hierarchy')
#     list_filter = ('resume',)
#     search_fields = ('resume__name', 'reference__name')

