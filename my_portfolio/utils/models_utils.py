from django.db import models


class CustomProjectOrder(models.Manager):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Skill Category"
        verbose_name_plural = "Skill Categories"
