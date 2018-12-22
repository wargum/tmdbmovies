
from tmdbmovies.models import Movie, Genre, Cast, MovieGenre, MovieCast, Gender
from rest_framework import response, serializers, status

class GenderSerializer(serializers.ModelSerializer):

	class Meta:
		model = Gender
		fields = ('gender_id', 'gender_name')

class GenreSerializer(serializers.ModelSerializer):

	class Meta:
		model = Genre
		fields = ('genre_id', 'genre_name')

class MovieGenreSerializer(serializers.ModelSerializer):
	movie_id = serializers.ReadOnlyField(source='movie.movie_id')
	genre_id = serializers.ReadOnlyField(source='genre.genre_id')

	class Meta:
		model = MovieGenre
		fields = ('movie_id', 'genre_id')

class MovieCastSerializer(serializers.ModelSerializer):
	movie_id = serializers.ReadOnlyField(source='movie.movie_id')
	cast_id = serializers.ReadOnlyField(source='cast.cast_id')
	characters = serializers.CharField(allow_blank=True, allow_null=True, max_length=300)

	class Meta:
		model = MovieCast
		fields = ('movie_id', 'cast_id', 'characters')

class MovieSerializer(serializers.ModelSerializer):
	budget = serializers.IntegerField(
        allow_null=True
	)
	homepage = serializers.CharField(
		allow_blank=True,
        allow_null=True,
        max_length=255
	)
	tmdb_id = serializers.IntegerField(
        allow_null=True
	)
	original_language = serializers.CharField(
		allow_blank=True,
        allow_null=True,
        max_length=255
	)
	original_title = serializers.CharField(
		allow_blank=True,
        allow_null=True,
        max_length=255
	)
	overview = serializers.CharField(
		allow_blank=True,
        allow_null=True
	)
	popularity = serializers.DecimalField(
		allow_null=True,
		max_digits=12,
		decimal_places=6
    )
	revenue = serializers.IntegerField(
        allow_null=True
    )
	runtime = serializers.IntegerField(        
		allow_null=True
    )
	tagline = serializers.CharField(        
        allow_blank=True,
        allow_null=True,
        max_length=255
    )
	title = serializers.CharField(
        allow_blank=True,
        allow_null=True,
        max_length=255      
    )
	vote_average = serializers.DecimalField(
		allow_null=True,
		max_digits=10,
		decimal_places=1
    )
	vote_count = serializers.IntegerField(        
        allow_null=True
    )
	movie_genre = MovieCastSerializer(
		source='movie_genre_set', # Note use of _set
		many=True,
		read_only=True
	)
	genre_ids = serializers.PrimaryKeyRelatedField(
		many=True,
		write_only=True,
		queryset=Genre.objects.all(),
		source='movie_genre'
	)

	class Meta:
		model = Movie
		fields = (
            'movie_id',
            'budget',
            'homepage',
            'tmdb_id',
            'original_language', 
            'original_title', 
            'overview', 
            'popularity', 
            'revenue',
            'runtime', 
            'tagline', 
            'title', 
            'vote_average', 
            'vote_count', 
            'movie_genre',
            'genre_ids'
		)

	def create(self, validated_data):

		genres = validated_data.pop('movie_genre')
		movie = Movie.objects.create(**validated_data)

		if genres is not None:
			for genre in genres:
				MovieGenre.objects.create(
					movie_id=movie.movie_id,
					genre_id=genre.genre_id
				)
		return movie

	def update(self, instance, validated_data):
		movie_id = instance.movie_id
		new_genres = validated_data.pop('movie_genre')

		instance.budget = validated_data.get(
			'budget',
			instance.budget
		)
		instance.homepage = validated_data.get(
			'homepage',
			instance.homepage
		)
		instance.justification = validated_data.get(
			'tmdb_id',
			instance.tmdb_id
		)
		instance.original_language = validated_data.get(
			'original_language',
			instance.original_language
		)
		instance.original_title = validated_data.get(
			'original_title',
			instance.original_title
		)
		instance.overview = validated_data.get(
			'overview',
			instance.overview
		)
		instance.popularity = validated_data.get(
			'popularity',
			instance.popularity
		)
		instance.revenue = validated_data.get(
			'revenue',
			instance.revenue
		)
		instance.runtime = validated_data.get(
			'runtime',
			instance.runtime
		)
		instance.tagline = validated_data.get(
			'tagline',
			instance.tagline
		)
		instance.title = validated_data.get(
			'title',
			instance.title
		)
		instance.vote_average = validated_data.get(
			'vote_average',
			instance.vote_average
		)
		instance.vote_count = validated_data.get(
			'vote_count',
			instance.vote_count
		)
		instance.save()

		# If any existing country/areas are not in updated list, delete them
		new_ids = []
		old_ids = MovieGenre.objects \
			.values_list('genre_id', flat=True) \
			.filter(movie_id__exact=movie_id)

		# TODO Insert may not be required (Just return instance)

		# Insert new unmatched country entries
		for genre in new_genres:
			new_id = genre.genre_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				MovieGenre.objects \
					.create(movie_id=movie_id, genre_id=new_id)

		# Delete old unmatched country entries
		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				MovieGenre.objects \
					.filter(movie_id=movie_id, old_id=new_id) \
					.delete()

		return instance

class CastSerializer(serializers.ModelSerializer):
	cast_name = serializers.CharField(
		allow_blank=False,
		max_length=45,
	)
	gender = GenderSerializer(
		source='gender_set', # Note use of _set
		many=False,
		read_only=True
	)
	gender_id = serializers.PrimaryKeyRelatedField(
		allow_null=False,
		many=False,
		write_only=True,
		queryset=Gender.objects.all(),
		source='gender'
	)
	movie_cast = MovieCastSerializer(
		source='movie_cast_set', # Note use of _set
		many=True,
		read_only=True
	)
	movie_casts = serializers.ListField(
		write_only=True,
		source='movie_cast'
	)

	class Meta:
		model = Cast
		fields = (
			'cast_id',
			'cast_name',
			'gender',
            'gender_id',
			'movie_cast',
			'movie_casts'
		)

	def create(self, validated_data):

		print(validated_data)

		characters = validated_data.pop('movie_cast')
		cast = Cast.objects.create(**validated_data)

		if characters is not None:
			for character in characters:
				MovieCast.objects.create(
					movie_id=character['movie_id'],
					cast_id=cast.cast_id,
					characters=character['character']
				)
		return cast

	def update(self, instance, validated_data):
		new_movies = validated_data.pop('movie_cast')
		cast_id = instance.cast_id

		instance.cast_name = validated_data.get(
			'cast_name',
			instance.cast_name
		)

		instance.gender_id = validated_data.get(
			'gender_id',
			instance.gender_id
		)

		instance.save()

		# If any existing movies are not in updated list, delete them
		new_ids = []
		old_ids = MovieCast.objects \
			.values_list('movie_id', flat=True) \
			.filter(cast_id__exact=cast_id)

		# TODO Insert may not be required (Just return instance)

		# Insert new unmatched country entries
		for movie in new_movies:
			new_id = movie['movie_id']
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				MovieCast.objects \
					.create(
					movie_id=new_id,
					cast_id=cast_id,
					characters=movie['character']
				)

		# Delete old unmatched country entries
		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				MovieCast.objects.filter(movie_id=old_id,cast_id=cast_id).delete()

		return instance