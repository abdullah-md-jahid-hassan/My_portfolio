#File : landing_spot/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.forms.widgets import RadioSelect 
from django import forms
from .models import User, Skill, Project, Service, Contact, Education, Experience, Certification, ProjectCategory, SkillCategory

# Import Custom Class
from my_portfolio.utils.permission_utils import Restricted_if_not_supper

# Import Custom Methods

# Register your models here.


# Registering models with the Django admin site for easy management.

# The admin interface allows for CRUD operations on the models.
@admin.register(User)
class UserAdmin(Restricted_if_not_supper, BaseUserAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'city', 'country')
    search_fields = ('first_name', 'last_name', 'email', 'country', 'city')
    list_filter = ('country', 'city')
    readonly_fields = ('meta_keywords',)


    # Define permission and important date fields to make readonly
    PERMISSION_FIELDS = (
        'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',
    )
    IMPORTANT_DATE_FIELDS = (
        'last_login', 'date_joined',
    )

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))

        # If user is in "General Users" group, add the fields
        if request.user.groups.filter(name='General Users').exists():
            readonly += list(self.PERMISSION_FIELDS) + list(self.IMPORTANT_DATE_FIELDS)

        return readonly
    
    
    # Hide permission and user control for general user
    def get_fieldsets(self, request, obj=None):
        personal_info = None
        admin_control = []

        for section in BaseUserAdmin.fieldsets:
            # Skip permission section for general users
            if (section[0] == 'Permissions' or section[0] == 'Important dates') and request.user.groups.filter(name='General Users').exists():
                continue

            if section[0] == 'Personal info':
                personal_info = (
                    'Personal Information',
                    {
                        **section[1],
                        'fields': section[1]['fields'] + (
                            'tag_line', 'phone', 'banner_image', 'profile_image'
                        )
                    }
                )
            else:
                admin_control.append(section)

        final_fieldsets = [
            personal_info,
            ('Location', {
                'fields': ('country', 'city', 'area', 'location_link')
            }),
            ('Professional Links', {
                'fields': ('github', 'linkedin', 'portfolio'),
            }),
            ('Additional Information', {
                'fields': ('about', 'hobbies', 'language'),
                'classes': ('collapse',)
            }),
            ('Meta Tags', {
                'fields': ('meta_description', 'meta_keywords'),
                'classes': ('collapse',)
            }),
        ] + admin_control

        return tuple(fs for fs in final_fieldsets if fs is not None)
    
    

# Registering the SkillCategory model with the admin site
@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}  # Auto-generate slug from name
    search_fields = ('name',)

# Registering the Skill model with the admin site
@admin.register(Skill)
class SkillAdmin(Restricted_if_not_supper, admin.ModelAdmin):
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
class ProjectAdmin(Restricted_if_not_supper, admin.ModelAdmin):
    form = ProjectAdminForm
    
    list_display = ( 'is_featured', 'title', 'display_categories', 'user')
    list_filter = ('is_featured', 'categories', 'user')
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
            'fields': ('description', 'image_path', 'resume_des')
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
class ServiceAdmin(Restricted_if_not_supper, admin.ModelAdmin):
    list_display = ('title', 'user')
    list_filter = ('user',)
    search_fields = ('title', 'description', 'user__id')


# Registering the Contact model with the admin site
class ContactAdminForm(forms.ModelForm):
    # Custom form for the Contact model to handle the toggle switch for is_seen field
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'is_seen': forms.CheckboxInput(attrs={'class': 'toggle-switch'}),
        }

    # Custom media for the admin form to include toggle switch CSS
    class Media:
        css = {
            'all': ('portfolio/css/toggle.css',) 
        }
        
# Registering the Contact model with the admin site
@admin.register(Contact)
class ContactAdmin(Restricted_if_not_supper, admin.ModelAdmin):
    form = ContactAdminForm
    
    list_display = ('is_seen','name', 'email', 'subject', 'submitted_at', 'user')
    list_filter = ('submitted_at','is_seen', 'user')
    search_fields = ('name', 'email', 'subject', 'user__id')
    readonly_fields = ('submitted_at',)
    date_hierarchy = 'submitted_at'

    
    
# Registering the Certification model with the admin site
@admin.register(Certification)
class CertificationAdmin(Restricted_if_not_supper, admin.ModelAdmin):
    list_display = ('title', 'organization', 'user', 'issue_date')
    list_filter = ('organization', 'issue_date', 'user')
    search_fields = ('title', 'organization', 'user__id')
    date_hierarchy = 'issue_date'



# Registering the Education model with the admin site
@admin.register(Education)
class EducationAdmin(Restricted_if_not_supper, admin.ModelAdmin):
    list_display = ('degree', 'institution', 'start_date', 'end_date', 'user')
    list_filter = ('institution', 'user')
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
class ExperienceAdmin(Restricted_if_not_supper, admin.ModelAdmin):
    list_display = ('name', 'institution', 'start_date', 'end_date', 'user')
    list_filter = ('institution', 'user')
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