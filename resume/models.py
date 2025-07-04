# file: resume/models.py

from django.db import models
from landing_spot.models import User
from landing_spot.models import Project


# Create your models here.



class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    summary = models.TextField(null=True, blank=True)
    # is_watermark = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_active:
            # Set is_active=False for all other records of the same user
            Resume.objects.filter(user=self.user, is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)
        
        

class ResumeProject(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='resume_projects')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='resume_projects')
    hierarchy = models.PositiveIntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['-hierarchy']