from tmdbmovies.models import Movie, Genre, Cast, MovieGenre, MovieCast, Gender 
from api.serializers import MovieSerializer, CastSerializer
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response


class MovieViewSet(viewsets.ModelViewSet):
	queryset = Movie.objects.order_by('title')
	serializer_class = MovieSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def delete(self, request, pk, format=None):
		movie = self.get_object(pk)
		self.perform_destroy(self, movie)

		return Response(status=status.HTTP_204_NO_CONTENT)

	def perform_destroy(self, instance):
		instance.delete()


class CastViewSet(viewsets.ModelViewSet):

	queryset = Cast.objects.select_related('gender').order_by('cast_name')
	serializer_class = CastSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def delete(self, request, pk, format=None):
		cast = self.get_object(pk)
		self.perform_destroy(self, cast)

		return Response(status=status.HTTP_204_NO_CONTENT)

	def perform_destroy(self, instance):
		instance.delete()
