from movies.models import FilmWork
from rest_framework import serializers


class FilmWorkSerializer(serializers.ModelSerializer):
    genres = serializers.StringRelatedField(many=True)
    writers = serializers.CharField()
    directors = serializers.CharField()
    actors = serializers.CharField()

    class Meta:
        model = FilmWork
        fields = ['id', 'title', 'description', 'creation_date',
                  'rating', 'type', 'genres', 'writers', 'directors', 'actors']
