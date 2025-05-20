#File : portfolio/admin.py

from django.contrib import admin
from .models import User, Skill, Project, Service, Contact, Education, Experience, Achievement, Certification, ProjectCategory


# Register your models here.


# Registering models with the Django admin site for easy management.

# The admin interface allows for CRUD operations on the models.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'country', 'city')
    search_fields = ('first_name', 'last_name', 'email', 'country', 'city')
    list_filter = ('country', 'city')
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'banner_image', 'profile_image')
        }),
        ('Location', {
            'fields': ('country', 'city', 'area')
        }),
        ('Professional Links', {
            'fields': ('github', 'linkedin', 'portfolio'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('about', 'hobbies', 'language'),
            'classes': ('collapse',)
        }),
    )

# Registering the Skill model with the admin site
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage', 'type', 'user_id')
    list_filter = ('type', 'user_id')
    search_fields = ('name', 'user_id__id')
    
    

# Registering the ProjectCategory model with the admin site
@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}  # Auto-generate slug from name
    search_fields = ('name',)



# Registering the Project model with the admin site
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_categories', 'start_date', 'end_date', 'user_id')
    list_filter = ('categories', 'user_id')  # Updated to filter by categories
    search_fields = ('title', 'description', 'user_id__id')
    filter_horizontal = ('categories',)  # Adds a nice widget for selecting multiple categories
    date_hierarchy = 'end_date'
    readonly_fields = ('duration',)
    
    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    display_categories.short_description = 'Categories'
    
    fieldsets = (
        (None, {
            'fields': ('user_id', 'title', 'categories')  # Updated to include categories
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
    list_display = ('title', 'user_id')
    list_filter = ('user_id',)
    search_fields = ('title', 'description', 'user_id__id')



# Registering the Contact model with the admin site
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at', 'user_id')
    list_filter = ('user_id', 'submitted_at')
    search_fields = ('name', 'email', 'subject' 'user_id__id')
    readonly_fields = ('submitted_at',)
    date_hierarchy = 'submitted_at'


# Registering the Education model with the admin site
@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'start_date', 'end_date', 'user_id')
    list_filter = ('user_id', 'institution')
    search_fields = ('degree', 'institution', 'department', 'user_id__id')
    readonly_fields = ('duration',)
    fieldsets = (
        (None, {
            'fields': ('user_id', 'degree', 'institution', 'institution_logo', 'department', 'department_logo')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'duration')
        }),
        ('Grades', {
            'fields': ('grade', 'grade_standard')
        }),
    )



# Registering the Experience model with the admin site
@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution', 'start_date', 'end_date', 'user_id')
    list_filter = ('user_id', 'institution')
    search_fields = ('name', 'institution', 'description', 'user_id__id')
    readonly_fields = ('duration',)
    fieldsets = (
        (None, {
            'fields': ('user_id', 'name', 'institution')
        }),
        ('Details', {
            'fields': ('description',)
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'duration')
        }),
    )



# Registering the Achievement model with the admin site
@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'content_type', 'object_id', 'user_id', 'get_linked_object')
    list_filter = ('user_id', 'content_type')
    search_fields = ('name', 'user_id__id')
    readonly_fields = ('get_linked_object',)
    
    # Custom method to display the linked object
    def get_linked_object(self, obj):
        return obj.epe_id
    get_linked_object.short_description = 'Linked Object'

    fieldsets = (
        (None, {
            'fields': ('user_id', 'name')
        }),
        ('Generic Relationship', {
            'fields': ('content_type', 'object_id', 'get_linked_object')
        }),
    )
    
    
    
# 
@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'user_id', 'issue_date')
    list_filter = ('organization', 'user_id', 'issue_date')
    search_fields = ('title', 'organization', 'user_id__id')
    date_hierarchy = 'issue_date'
    
    fieldsets = (
        (None, {
            'fields': ('user_id', 'title', 'organization', 'issue_date')
        }),
        ('Credential Information', {
            'fields': ('credential_id', 'credential_url'),
            'classes': ('collapse',)
        }),
    )