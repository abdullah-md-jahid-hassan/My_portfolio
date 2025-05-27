# File: portfolio/signals.py


import os
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.db.models import FileField
from django.db import models


# This method retrieves all FileField instances from a model instance.
def get_file_fields(instance):
    return [field for field in instance._meta.fields if isinstance(field, FileField)]


# Signal to delete old files when a model instance is updated
@receiver(pre_save)
def delete_old_files_on_change(sender, instance, **kwargs):
    # Only process subclasses of django.db.models.Model (avoid internal models)
    if not issubclass(sender, models.Model) or not instance.pk: # Check if model is a subclass of Model and bing created
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist: # Instance does not exist, so do nothing
        return

    # Iterate through all FileFields and delete old files if they have changed
    for field in get_file_fields(instance):
        old_file = getattr(old_instance, field.name)
        new_file = getattr(instance, field.name)

        if old_file and old_file != new_file: # Check if the file has changed
            if hasattr(old_file, 'path') and os.path.isfile(old_file.path): # Check if the old file exists
                os.remove(old_file.path)


# Signal to delete files when a model instance is deleted
@receiver(post_delete)
def delete_files_on_instance_delete(sender, instance, **kwargs):
    # Only process subclasses of django.db.models.Model. This avoids processing internal models
    if not issubclass(sender, models.Model): # Check if model is a subclass of Model
        return

    # Iterate through all FileFields and delete files associated with the instance
    for field in get_file_fields(instance):
        file_field = getattr(instance, field.name)
        if file_field and hasattr(file_field, 'path') and os.path.isfile(file_field.path): # Check if the file exists
            os.remove(file_field.path)
