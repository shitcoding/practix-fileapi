import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from movies.storage import CustomStorage
from psqlextra.indexes import UniqueIndex


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255, unique=True)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full_name'), max_length=255)

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        db_table = "content\".\"person"

    def __str__(self):
        return self.full_name


class FilmWork(UUIDMixin, TimeStampedMixin):
    class FilmWorkType(models.TextChoices):
        MOVIE = 'movie', _('movie')
        TV_SHOW = 'tv_show', _('tv_show')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'),
                                   blank=True, null=True)
    file_path = models.FileField(_('file_path'),
                                 blank=True, null=True, storage=CustomStorage,)
    creation_date = models.DateTimeField(_('creation_date'),
                                         blank=True, null=True)
    rating = models.FloatField(_('rating'),
                               blank=True, null=True,
                               validators=[MinValueValidator(0, f"""{_('rating')} не может быть меньше 0"""),
                                           MaxValueValidator(100, f"""{_('rating')}  не может быть больше 100""")])
    type = models.CharField(_('type'),
                            max_length=7, choices=FilmWorkType.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmWork')
    persons = models.ManyToManyField(Person, through='PersonFilmWork')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Movie')
        verbose_name_plural = _('Movies')

    def __str__(self):
        return self.title


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _("Genre")
        verbose_name_plural = _('Genres')

        indexes = [
            UniqueIndex(fields=('film_work', 'genre'),
                        name='film_work_genre'
                        ),
        ]


class PersonFilmWork(UUIDMixin):
    class RoleType(models.TextChoices):
        ACTOR = 'actor', _('actor')
        WRITER = 'writer', _('writer')
        DIRECTOR = 'director', _('director')

    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.CharField(_('role'), max_length=8, choices=RoleType.choices)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('Member')
        verbose_name_plural = _('Members')

        indexes = [
            UniqueIndex(fields=('film_work', 'person', 'role'),
                        name='film_work_person_role'
                        ),
        ]
