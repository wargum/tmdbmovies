from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django_filters.views import FilterView

from .filters import MovieFilter, CastFilter, GenreFilter

from .models import Movie
from .models import Cast
from .models import MovieCast
from .models import MovieGenre
from .forms import MovieForm
from .forms import CastForm

def index(request):
   return HttpResponse("Hello, world. You're at the tmdb movie index page.")

class AboutPageView(generic.TemplateView):
	template_name = 'tmdbmovies/about.html'


class HomePageView(generic.TemplateView):
	template_name = 'tmdbmovies/home.html'

@method_decorator(login_required, name='dispatch')
class MovieListView(generic.ListView):
	model = Movie
	context_object_name = 'movies'
	template_name = 'tmdbmovies/movie.html'
	paginate_by = 50
	
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_queryset(self):
		return Movie.objects.all().order_by('title')

@method_decorator(login_required, name='dispatch')
class MovieDetailView(generic.DetailView):
	model = Movie
	context_object_name = 'movie'
	template_name = 'tmdbmovies/movie_detail.html'
	
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

@method_decorator(login_required, name='dispatch')
class CastListView(generic.ListView):
	model = Cast
	context_object_name = 'casts'
	template_name = 'tmdbmovies/cast.html'
	paginate_by = 50
	
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_queryset(self):
		return Cast.objects.all().select_related('gender').order_by('cast_name')

@method_decorator(login_required, name='dispatch')
class CastDetailView(generic.DetailView):
	model = Cast
	context_object_name = 'cast'
	template_name = 'tmdbmovies/cast_detail.html'
	
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

@method_decorator(login_required, name='dispatch')
class MovieCreateView(generic.View):
	model = Movie
	form_class = MovieForm
	success_message = "Movie created successfully"
	template_name = 'tmdbmovies/movie_new.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def post(self, request):
		form = MovieForm(request.POST)
		if form.is_valid():
			movie = form.save(commit=False)
			movie.save()
			for genre in form.cleaned_data['genres']:
				MovieGenre.objects.create(movie=movie, genre=genre)
			return redirect(movie) # shortcut to object's get_absolute_url()
		return render(request, 'tmdbmovies/movie_new.html', {'form': form})

	def get(self, request):
		form = MovieForm()
		return render(request, 'tmdbmovies/movie_new.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class MovieUpdateView(generic.UpdateView):
	model = Movie
	form_class = MovieForm
	# fields = '__all__' <-- superseded by form_class
	context_object_name = 'movie'
	success_message = "Movie updated successfully"
	template_name = 'tmdbmovies/movie_update.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def form_valid(self, form):
		movie = form.save(commit=False)
		movie.save()

		old_ids = MovieGenre.objects\
			.values_list('genre_id', flat=True)\
			.filter(movie_id=movie.movie_id)

		new_genres = form.cleaned_data['genres']

		# New ids
		new_ids = []

		for genre in new_genres:
			new_id = genre.genre_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				MovieGenre.objects \
					.create(movie=movie, genre=genre)

		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				MovieGenre.objects \
					.filter(movie_id=movie.movie_id, genre_id=old_id) \
					.delete()

		return HttpResponseRedirect(movie.get_absolute_url())

@method_decorator(login_required, name='dispatch')
class MovieDeleteView(generic.DeleteView):
	model = Movie
	success_message = "Movie deleted successfully"
	success_url = reverse_lazy('movie')
	context_object_name = 'movie'
	template_name = 'tmdbmovies/movie_delete.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()

		# Delete HeritageSiteJurisdiction entries
		MovieGenre.objects \
			.filter(movie_id=self.object.movie_id) \
			.delete()

		MovieCast.objects \
			.filter(movie_id=self.object.movie_id) \
			.delete()

		self.object.delete()

		return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required, name='dispatch')
class CastCreateView(generic.View):
	model = Cast
	form_class = CastForm
	success_message = "Cast created successfully"
	template_name = 'tmdbmovies/cast_new.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def post(self, request):
		form = CastForm(request.POST)
		if form.is_valid():
			cast = form.save(commit=False)
			cast.save()
			for movie in form.cleaned_data['movies']:
				MovieCast.objects.create(movie = movie, cast=cast)
			return redirect(cast) # shortcut to object's get_absolute_url()
			# return HttpResponseRedirect(site.get_absolute_url())
		return render(request, 'tmdbmovies/cast_new.html', {'form': form})

	def get(self, request):
		form = CastForm()
		return render(request, 'tmdbmovies/cast_new.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class CastUpdateView(generic.UpdateView):
	model = Cast
	form_class = CastForm
	context_object_name = 'cast'
	success_message = "Cast updated successfully"
	template_name = 'tmdbmovies/cast_update.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def form_valid(self, form):
		cast = form.save(commit=False)
		cast.save()

		old_ids = MovieCast.objects\
			.values_list('movie_id', flat=True)\
			.filter(cast_id=cast.cast_id)

		new_movies = form.cleaned_data['movies']

		# New ids
		new_ids = []

		for movie in new_movies:
			new_id = movie.movie_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				MovieCast.objects \
					.create(movie=movie, cast=cast)

		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				MovieCast.objects \
					.filter(movie_id=old_id, cast_id=cast.cast_id) \
					.delete()

		return HttpResponseRedirect(cast.get_absolute_url())

@method_decorator(login_required, name='dispatch')
class CastDeleteView(generic.DeleteView):
	model = Cast
	success_message = "Cast deleted successfully"
	success_url = reverse_lazy('cast')
	context_object_name = 'cast'
	template_name = 'tmdbmovies/cast_delete.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()

		MovieCast.objects \
			.filter(cast_id=self.object.cast_id) \
			.delete()

		self.object.delete()

		return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required, name='dispatch')
class MovieFilterView(FilterView):
	filterset_class = MovieFilter
	template_name = 'tmdbmovies/movie_filter.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

@method_decorator(login_required, name='dispatch')
class CastFilterView(FilterView):
	filterset_class = CastFilter
	template_name = 'tmdbmovies/cast_filter.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

@method_decorator(login_required, name='dispatch')
class GenreFilterView(FilterView):
	filterset_class = GenreFilter
	template_name = 'tmdbmovies/genre_filter.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)