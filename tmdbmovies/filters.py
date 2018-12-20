import django_filters
from tmdbmovies.models import Movie, Cast, Genre, Gender

class MovieFilter(django_filters.FilterSet):
	
	budget = django_filters.RangeFilter(
		field_name='budget',
		label='Budget'
	)
	
	homepage = django_filters.CharFilter(
		field_name='homepage',
		label='Homepage',
		lookup_expr='icontains'
	)
	
	tmdb_id = django_filters.NumberFilter(
		field_name='tmdb_id',
		label='DMDB ID',
		lookup_expr='exact'
	)
	
	original_language = django_filters.CharFilter(
		field_name='original_language',
		label='Original Language',
		lookup_expr='icontains'
	)
    
	original_title = django_filters.CharFilter(
		field_name='original_title',
		label='Original Title',
		lookup_expr='icontains'
	)
	
	overview = django_filters.CharFilter(
		field_name='overview',
		label='Overview',
		lookup_expr='icontains'
	)
	
	popularity = django_filters.RangeFilter(
		field_name='popularity',
		label='Popularity ',
	)
	
	revenue = django_filters.RangeFilter(
		field_name='revenue',
		label='Revenue',
	)
	
	runtime = django_filters.RangeFilter(
		field_name='runtime',
		label='Runtime',
	)
	
	tagline = django_filters.CharFilter(
		field_name='tagline',
		label='Tagline',
		lookup_expr='icontains'	
	)
	
	title = django_filters.CharFilter(
		field_name='title',
		label='Title',
		lookup_expr='icontains'
	)
	
	vote_average = django_filters.RangeFilter(
		field_name='vote_average',
		label='Vote Average'
	)
	
	vote_count = django_filters.RangeFilter(
		field_name='vote_count',
		label='Vote Count'
	)
	
	genre = django_filters.ModelChoiceFilter(
		field_name='genres',
		label='Genre',
		queryset=Genre.objects.all().order_by('genre_name'),
		lookup_expr='exact'
	)
	class Meta:
		model = Movie
		fields = []


class CastFilter(django_filters.FilterSet):

	cast_name = django_filters.CharFilter(
		field_name='cast_name',
		label='Cast',
		lookup_expr='icontains'
	)
	
	gender = django_filters.ModelChoiceFilter(
		field_name='gender',
		label='Gender',
		queryset=Gender.objects.all().order_by('gender_name'),
		lookup_expr='exact'
	)
	
	movie = django_filters.ModelChoiceFilter(
		field_name='movies',
		label='Movie',
		queryset=Movie.objects.all().order_by('title'),
		lookup_expr='exact'
	)
	
	class Meta:
		model = Cast
		fields = []

class GenreFilter(django_filters.FilterSet):
	
	genre_name = django_filters.CharFilter(
		field_name='genre_name',
		label='Genre',
		lookup_expr='icontains'
	)
	
	class Meta:
		model = Genre
		fields = []