#File : portfolio/admin.py

from django.contrib import admin
from django.forms.widgets import RadioSelect 
from django import forms
from .models import User, Skill, Project, Service, Contact, Education, Experience, Certification, ProjectCategory, SkillCategory


# Register your models here.


# Registering models with the Django admin site for easy management.

# The admin interface allows for CRUD operations on the models.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'country', 'city')
    search_fields = ('first_name', 'last_name', 'email', 'country', 'city')
    list_filter = ('country', 'city')
    readonly_fields = ('meta_keywords',)
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name','tag_line', 'email', 'phone', 'banner_image', 'profile_image')
        }),
        ('Location', {
            'fields': ('country', 'city', 'area', 'location_link')
        }),
        ('Professional Links', {
            'fields': ('github', 'linkedin', 'portfolio'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('about', 'hobbies', 'language'),
            'classes': ('collapse',)
        }),
        ('Meta Tags', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )
    
    

# Registering the SkillCategory model with the admin site
@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}  # Auto-generate slug from name
    search_fields = ('name',)

# Registering the Skill model with the admin site
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage', 'category', 'user')
    list_filter = ('category', 'user')
    search_fields = ('name', 'user__id')
    
    

# Registering the ProjectCategory model with the admin site
@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}  # Auto-generate slug from name
    search_fields = ('name',)



# Registering the Project model with the admin site
class ProjectAdminForm(forms.ModelForm):
    # Custom form for the Project model to handle the toggle switch for is_featured field
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'is_featured': forms.CheckboxInput(attrs={'class': 'toggle-switch'}),
        }

    # Custom media for the admin form to include toggle switch CSS
    class Media:
        css = {
            'all': ('portfolio/css/toggle.css',) 
        }
        
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    
    list_display = ('title', 'display_categories', 'start_date', 'end_date', 'user')
    list_filter = ('categories', 'user')
    search_fields = ('title', 'description', 'user__id')
    filter_horizontal = ('categories',)
    date_hierarchy = 'end_date'
    readonly_fields = ('duration',)
    
    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    display_categories.short_description = 'Categories'
    
    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'tag_line', 'categories', 'is_featured')
        }),
        ('Details', {
            'fields': ('description', 'image_path')
        }),
        ('Links', {
            'fields': ('github_link', 'live_link')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'duration')
        }),
    )



# Registering the Service model with the admin site
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')
    list_filter = ('user',)
    search_fields = ('title', 'description', 'user__id')



# Registering the Contact model with the admin site
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at', 'user')
    list_filter = ('user', 'submitted_at')
    search_fields = ('name', 'email', 'subject' 'user__id')
    readonly_fields = ('submitted_at',)
    date_hierarchy = 'submitted_at'

    
    
# Registering the Certification model with the admin site
@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'user', 'issue_date')
    list_filter = ('organization', 'user', 'issue_date')
    search_fields = ('title', 'organization', 'user__id')
    date_hierarchy = 'issue_date'



# Registering the Education model with the admin site
@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'start_date', 'end_date', 'user')
    list_filter = ('user', 'institution')
    search_fields = ('degree', 'institution', 'department', 'user__id')
    readonly_fields = ('duration',)
    fieldsets = (
        (None, {
            'fields': ('user', 'degree', 'institution', 'institution_logo', 'department', 'department_logo')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'duration')
        }),
        ('Grades', {
            'fields': ('grade', 'grade_standard')
        }),
        ('Certificate', {
            'fields': ('certificate',)
        }),
    )



# Registering the Experience model with the admin site
@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution', 'start_date', 'end_date', 'user')
    list_filter = ('user', 'institution')
    search_fields = ('name', 'institution', 'description', 'user__id')
    readonly_fields = ('duration',)
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'institution', 'address')
        }),
        ('Details', {
            'fields': ('description',)
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'duration')
        }),
        ('Certificate', {
            'fields': ('certificate',)
        }),
    )