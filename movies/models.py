from django.db import models
from django.urls import reverse

class Genre(models.Model):
    title = models.TextField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.title
    
class Movie(models.Model):
    movie_id = models.IntegerField()
    title = models.TextField()
    slug = models.SlugField(null=False, unique=True)
    is_active = models.BooleanField(default=True)
    overview = models.TextField()
    genre = models.ManyToManyField(Genre)
    popularity = models.FloatField()
    poster = models.URLField(null=True, blank=True)
    video = models.URLField(null=True, blank=True)
    release_date = models.DateField()
    language = models.TextField(max_length=100, null=True, blank=True)
    vote_averate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'Title: {self.title}'
    
    class Meta:
        ordering = ('-release_date',)