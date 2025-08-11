# file: resume/models.py

from django.db import models
from landing_spot.models import User, Project, Certification


# Create your models here.

class Reference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='references', blank=False, null=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    designation = models.CharField(max_length=100, blank=False, null=False)
    institution = models.CharField(max_length=100, default=None)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.designation}"
    

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    summary = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.is_active:
            # Set is_active=False for all other records of the same user
            Resume.objects.filter(user=self.user, is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)
        
        

class ResumeProject(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='project_resume')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='resume_project')
    hierarchy = models.PositiveIntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['-hierarchy']
        
        

class ResumeCertificate(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='certificate_resume')
    certificate = models.ForeignKey(Certification, on_delete=models.CASCADE, related_name='resume_certificate')
    hierarchy = models.PositiveIntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['-hierarchy']
        
        

class ResumeReference(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='reference_resume')
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE, related_name='resume_reference')
    hierarchy = models.PositiveIntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['-hierarchy']