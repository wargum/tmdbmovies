from django.contrib import admin
# Register your models here.

import tmdbmovies.models as models

@admin.register(models.Cast)
class CastAdmin(admin.ModelAdmin):
	fields = ['cast_name', 'gender']
	list_display = ['cast_name', 'gender']
	ordering = ['cast_name']

@admin.register(models.Gender)
class GenderAdmin(admin.ModelAdmin):
	fields = ['gender_name']
	list_display = ['gender_name']
	ordering = ['gender_name']

@admin.register(models.Genre)
class GenderAdmin(admin.ModelAdmin):
	fields = ['genre_name']
	list_display = ['genre_name']
	ordering = ['genre_name']

@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
	fields = ['budget', 'homepage', 'tmdb_id', 'original_language', 'original_title', 'overview', 'popularity', 'revenue', 'runtime', 'tagline', 'title', 'vote_average', 'vote_count']
	list_display = ['budget', 'homepage', 'tmdb_id', 'original_language', 'original_title', 'overview', 'popularity', 'revenue', 'runtime', 'tagline', 'title', 'vote_average', 'vote_count']
	ordering = ['title']