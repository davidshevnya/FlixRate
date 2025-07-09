from django.db import models
from django.urls import reverse

class Genre(models.Model):
    title = models.TextField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.title
    
    
    