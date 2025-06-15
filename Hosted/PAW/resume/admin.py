# file: resume/admin.py

from django.contrib import admin
from django import forms
from .models import Resume, ResumeProject

from my_portfolio.utils.permission_utils import Restricted_if_not_supper

# class for the ResumeProject inline in the Resume admin
class ResumeProjectInline(Restricted_if_not_supper, admin.TabularInline):
    model = ResumeProject
    extra = 1
    autocomplete_fields = ['project']
    ordering = ['hierarchy']



# Registering the Resume model with the admin site
class ResumeAdminForm(forms.ModelForm):
    # Custom form for the Project model to handle the toggle switch for is_active field
    class Meta:
        model = Resume
        fields = '__all__'
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle-switch'}),
            # 'is_watermark': forms.CheckboxInput(attrs={'class': 'toggle-switch'}),
        }

    # Custom media for the admin form to include toggle switch CSS
    class Media:
        css = {
            'all': ('portfolio/css/toggle.css',) 
        }
@admin.register(Resume)
class ResumeAdmin(Restricted_if_not_supper, admin.ModelAdmin):
    form = ResumeAdminForm
    
    list_display = ('id', 'name', 'user')
    search_fields = ('name', 'user__username', 'user__email')
    list_filter = ('is_active', 'user')
    inlines = [ResumeProjectInline]


# Registering the ResumeProject model with the admin site
# @admin.register(ResumeProject)
# class ResumeProjectAdmin(Restricted_if_not_supper, admin.ModelAdmin):
#     list_display = ('resume', 'project', 'hierarchy')
#     list_filter = ('resume',)
#     search_fields = ('resume__name', 'project__title')

