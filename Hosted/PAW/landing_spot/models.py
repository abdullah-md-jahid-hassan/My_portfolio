#File : landing_port/models.py

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

# Imported functions
# To find the duration.
from my_portfolio.utils.date_utils import duration
from my_portfolio.utils.models_utils import CustomProjectOrder


# Create your models here.

#User profile model containing personal and professional information.
# This model can be used to store user details, contact information, etc.
# The 'profile_image' field can be used to store a profile picture.
class User(AbstractUser):
    tag_line = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=False, unique=True)
    country = models.CharField(max_length=100, null=True, blank=False)
    city = models.CharField(max_length=100, null=True, blank=False)
    area = models.CharField(max_length=100, null=True, blank=False)
    location_link = models.CharField(max_length=255, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    github = models.URLField(max_length=255, null=True, blank=True)
    linkedin = models.URLField(max_length=255, null=True, blank=True)
    portfolio = models.URLField(max_length=255, null=True, blank=True)
    static_resume_file = models.FileField(upload_to='portfolio/img/resume/static/', null=True, blank=True)
    banner_image = models.ImageField(upload_to='portfolio/img/person/banner_images/', null=True, blank=False)
    profile_image = models.ImageField(upload_to='portfolio/img/person/profile_images/', null=True, blank=False)
    hobbies = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=255, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.email} --> {self.first_name} {self.last_name}" if self.first_name and self.last_name else str(self.email)
    
    @property
    # Generate dynamic meta keywords based on user profile and related models.
    # This method can be used to create a list of keywords for SEO purposes.
    def meta_keywords(self):
        keywords = ['portfolio']
        
        # Add full name if available
        if self.first_name and self.last_name:
            full_name = f"{self.first_name} {self.last_name}"
            keywords.append(full_name)
        
        # Add related objects' names/titles if they exist
        related_fields = [
            ('projects', 'title'),
            ('services', 'title'),
            ('certifications', 'title'),
            ('skills', 'name'),
            ('experiences', 'name'),
            ('educations', 'degree'),
        ]
        
        for relation, field_name in related_fields:
            try:
                items = getattr(self, relation).values_list(field_name, flat=True)
                keywords.extend([item for item in items if item])
            except Exception:
                continue
        
        # Add other relevant fields
        if self.tag_line:
            keywords.append(self.tag_line)
        if self.country:
            keywords.append(self.country)
        if self.city:
            keywords.append(self.city)
        if self.area:
            keywords.append(self.area)
        if self.language:
            keywords.extend([lang.strip() for lang in self.language.split(',') if lang.strip()])
        
        # Remove duplicates and empty strings, then join
        unique_keywords = set(filter(None, keywords))
        return ", ".join(unique_keywords) if unique_keywords else ""

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


# SkillCategory model representing different categories of Skills.
# This model can be used to classify Skills into different domains.
class SkillCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Skill Category"
        verbose_name_plural = "Skill Categories"





#Skills model representing different skills with proficiency percentages.
# This model can be used to showcase technical skills, languages, etc.
# The 'percentage' field can be used to indicate the proficiency level.
class Skill(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=False)
    percentage = models.PositiveIntegerField(null=True, blank=False)
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')

    def __str__(self):
        return f"{self.user} --> {self.category} --> {self.name} - ({self.percentage}%)"

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"


# ProjectCategory model representing different categories of projects.
# This model can be used to classify projects into different domains.
class ProjectCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"



# Projects model containing details about various projects.
# This model can be used to showcase personal projects, contributions, etc.
# The 'category' field can be used to classify projects into different domains.
class Project(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=True, blank=False)
    tag_line = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=300, unique=True, null=True, blank=True)
    categories = models.ManyToManyField(ProjectCategory)
    description = models.TextField(null=True, blank=True)
    resume_des = models.TextField(null=True, blank=True)
    image_path = models.ImageField(upload_to='portfolio/img/project_images/', null=True, blank=True)
    github_link = models.URLField(max_length=255, null=True, blank=True)
    live_link = models.URLField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    
    

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

        


    all_objects = models.Manager()  # Default manager
    objects = CustomProjectOrder() # Custom ordering

    def __str__(self):
        return self.title or f"Project {self.id}"
    
    @property
    def duration(self):
        return duration(self.start_date, self.end_date)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"



# Services model representing services offered by the user.
# This model can be used to showcase different services or skills.
class Service(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=True, blank=False)
    description = models.TextField(null=True, blank=True)
    icon_class = models.CharField(max_length=50, null=True, blank=True)  # FontAwesome/bootstrap class
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return self.title or f"Service {self.id}"

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"




# Contact model for storing messages from users.
# This model can be used to store inquiries, feedback, etc.
class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=False)
    email = models.EmailField(max_length=255, null=True, blank=False)
    subject = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    is_seen = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-submitted_at']
        
        

# Certification model representing various certifications.  
class Certification(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name="Certification Title", null=True, blank=False)
    organization = models.CharField(max_length=255, verbose_name="Issuing Organization", null=True, blank=False)
    certificate_image = models.ImageField(upload_to='portfolio/img/certificate_images/', null=True, blank=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='certifications', verbose_name="User")
    issue_date = models.DateField(null=True, blank=True, verbose_name="Issue Date")

    def __str__(self):
        return f"{self.title} from {self.organization}"

    class Meta:
        verbose_name = "Certification"
        verbose_name_plural = "Certifications"
        ordering = ['-issue_date']




# Education model representing educational qualifications.
# This model can be used to store degrees, certifications, etc.
class Education(models.Model):
    GRADE_STANDARD_CHOICES = [
        ('4', 'Out of 4'),
        ('5', 'Out of 5'),
        ('100', 'Out of 100'),
    ]
    
    id = models.AutoField(primary_key=True)
    degree = models.CharField(max_length=255, null=True, blank=False)
    institution = models.CharField(max_length=255, null=True, blank=False)
    institution_logo = models.ImageField(upload_to='portfolio/img/education/institution_logo', null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    department_logo = models.ImageField(upload_to='portfolio/img/education/department_logo', null=True, blank=True)
    resume_achi = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=False)
    end_date = models.DateField(null=True, blank=True)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=False)
    grade_standard = models.CharField(max_length=10, choices=GRADE_STANDARD_CHOICES, null=True, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='educations')
    certificate = models.ForeignKey(Certification, on_delete=models.CASCADE, related_name='educations', null=True, blank=True)

    def __str__(self):
        return f"{self.degree} at {self.institution}"
    
    
    @property
    # Calculate education duration in years.
    def duration(self):
        return duration(self.start_date, self.end_date)
    
    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Education"
        ordering = ['-end_date']




# Experience model representing work experience.
# This model can be used to store internships, jobs, etc.
class Experience(models.Model):
    type_choices = [
        ('on_site', 'On-site'),
        ('remote', 'Remote'),
        ('hybrid', 'Hybrid'),
    ]
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=False)  # Position name
    type = models.CharField(max_length=20, choices=type_choices, default='on_site', null=True, blank=False)
    institution = models.CharField(max_length=255, null=True, blank=False)
    address = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    resume_des = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=False)
    end_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    certificate = models.ForeignKey(Certification, on_delete=models.CASCADE, related_name='experiences', null=True, blank=True)

    def __str__(self):
        return f"{self.name} at {self.institution}"
    
    @property
    # Calculate experience duration in months.
    def duration(self):
        return duration(self.start_date, self.end_date)

    class Meta:
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"
        ordering = ['-start_date']