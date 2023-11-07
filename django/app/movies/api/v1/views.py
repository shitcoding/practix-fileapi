from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from rest_framework import generics

from movies.models import FilmWork, PersonFilmWork
from movies.serializers import FilmWorkSerializer


class BaseMovies:
    serializer_class = FilmWorkSerializer
    queryset = FilmWork.objects.order_by(
        'title'
    ).prefetch_related(
        'genres'
    ).annotate(
        actors=ArrayAgg('persons__full_name',
                        filter=Q(personfilmwork__role=PersonFilmWork.RoleType.ACTOR),
                        sep='\n',
                        distinct=True),
        directors=ArrayAgg('persons__full_name',
                           filter=Q(personfilmwork__role=PersonFilmWork.RoleType.DIRECTOR),
                           sep='\n',
                           distinct=True),
        writers=ArrayAgg('persons__full_name',
                         filter=Q(personfilmwork__role=PersonFilmWork.RoleType.WRITER),
                         sep='\n',
                         distinct=True)
    )


class MoviesList(BaseMovies, generics.ListAPIView):
    pass


class MoviesDetail(BaseMovies, generics.RetrieveAPIView):
    pass
