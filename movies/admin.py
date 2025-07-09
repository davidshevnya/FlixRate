from django.contrib import admin

from .models import Genre

class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Genre, GenreAdmin)
