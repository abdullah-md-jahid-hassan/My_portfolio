#file: my_portfolio/utils/date_utils.py

# Restricted access for non-supper user
class Restricted_if_not_supper:
    # Superusers can select any user
    # Staff users can only select themselves
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        if request.user.groups.filter(name='General Users').exists():
            # Get the user field
            if 'user' in form.base_fields:
                user_field = form.base_fields['user']
                user_field.queryset = user_field.queryset.filter(pk=request.user.pk)
                user_field.initial = request.user.pk
                
        return form
    

    # Superusers see all user accounts.
    # Normal users only see their own record.
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        if request.user.is_superuser:
            return qs
            
        if request.user.groups.filter(name='General Users').exists():
            # For User model
            if self.model._meta.model_name == 'user':
                return qs.filter(pk=request.user.pk)
            # For other models
            elif 'user' in [f.name for f in self.model._meta.get_fields()]:
                return qs.filter(user=request.user)
        
        return qs
    
    # Allow user to edit their own profile only.
    # Superusers can edit any record.
    def has_change_permission(self, request, obj=None):
        # Skip check for superusers
        if request.user.is_superuser:
            return True
            
        # Only apply restrictions for General Users
        if request.user.groups.filter(name='General Users').exists():
            if obj is None:
                return True  # Allow access to changelist view
                
            # Check model type once
            is_user_model = obj._meta.model_name == 'user'
            
            if is_user_model:
                return obj.pk == request.user.pk
            else:
                return obj.user == request.user
        
        return True
    
    # Allow user to delete their own profile only.
    # Superusers can delete any record.
def has_delete_permission(self, request, obj=None):
    # Superusers have full permissions
    if request.user.is_superuser:
        return True
        
    if request.user.groups.filter(name='General Users').exists():
        if obj is None:
            return False  # Disable bulk deletion
            
        # Check model type once
        is_user_model = obj._meta.model_name == 'user'
        
        if is_user_model:
            return False  # Or obj.pk == request.user.pk if allowing self-deletion
        else:
            return obj.user == request.user
    
    return True
    