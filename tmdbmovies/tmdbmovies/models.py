# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse

class Gender(models.Model):
    gender_id = models.AutoField(primary_key=True)
    gender_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'gender'
    
    def __str__(self):
        return self.gender_name


class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'genre'

    def __str__(self):
        return self.genre_name


class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    budget = models.IntegerField(blank=True, null=True)
    homepage = models.CharField(max_length=255, blank=True, null=True)
    tmdb_id = models.IntegerField(blank=True, null=True)
    original_language = models.CharField(max_length=255, blank=True, null=True)
    original_title = models.CharField(max_length=255, blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    popularity = models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True)
    revenue = models.BigIntegerField(blank=True, null=True)
    runtime = models.IntegerField(blank=True, null=True)
    tagline = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    vote_average = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True)
    vote_count = models.IntegerField(blank=True, null=True)

    genres = models.ManyToManyField(Genre, through='MovieGenre')

    class Meta:
        managed = False
        db_table = 'movie'

    def __str__(self):
        return self.title

    @property
    def genre_names(self):
        genres = self.genres.order_by('genre_name')

        names = []
        for genre in genres:
            name = genre.genre_name
            if name is None:
                continue
            if name not in names:
                names.append(name)

        return ', '.join(names)
    
    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'pk': self.pk})

class Cast(models.Model):
    cast_id = models.AutoField(primary_key=True)
    cast_name = models.CharField(max_length=45)
    gender = models.ForeignKey('Gender', on_delete=models.PROTECT, blank=True, null=True)
    movies = models.ManyToManyField(Movie, through='MovieCast')

    class Meta:
        managed = False
        db_table = 'cast'

    def __str__(self):
        return self.cast_name

    @property
    def movie_names(self):
        movies = self.movies.order_by('title')

        names = []
        for movie in movies:
            name = movie.title
            if name is None:
                continue
            character = MovieCast.objects.all().filter(movie_id = movie.movie_id).get(cast_id = self.cast_id).characters
            if character is not None:
                 name = ''.join([name, ' (', character, ')'])
            if name not in names:
                names.append(name)

        return ', '.join(names)

    def get_absolute_url(self):
        return reverse('cast_detail', kwargs={'pk': self.pk})

class MovieCast(models.Model):
    movie_cast_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    cast = models.ForeignKey(Cast, on_delete=models.CASCADE)
    characters = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_cast'


class MovieGenre(models.Model):
    movie_genre_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'movie_genre'
