from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('movies/', views.MovieListView.as_view(), name='movie'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('casts/', views.CastListView.as_view(), name='cast'),
    path('casts/<int:pk>/', views.CastDetailView.as_view(), name='cast_detail'),
    path('movies/new/', views.MovieCreateView.as_view(), name='movie_new'),
    path('movies/<int:pk>/delete/', views.MovieDeleteView.as_view(), name='movie_delete'),
    path('movies/<int:pk>/update/', views.MovieUpdateView.as_view(), name='movie_update'),
    path('casts/new/', views.CastCreateView.as_view(), name='cast_new'),
    path('casts/<int:pk>/delete/', views.CastDeleteView.as_view(), name='cast_delete'),
    path('casts/<int:pk>/update/', views.CastUpdateView.as_view(), name='cast_update'),
    path('movies/filter/', views.MovieFilterView.as_view(), kwargs=None, name='movie_filter'),
    path('casts/filter/', views.CastFilterView.as_view(), kwargs=None, name='cast_filter'),
    path('genres/filter/', views.GenreFilterView.as_view(), kwargs=None, name='genre_filter'),
]