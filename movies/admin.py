from django.contrib import admin

from .models import Genre, Movie

class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class MovieAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)

