from django.contrib import admin

from movies.models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork


class PersonRoleInline(admin.TabularInline):
    model = PersonFilmWork
    extra = 0

    def get_queryset(self, request):
        return super(PersonRoleInline, self)\
            .get_queryset(request).select_related('person')


class GenreInline(admin.TabularInline):
    model = GenreFilmWork
    extra = 0

    def get_queryset(self, request):
        return super(GenreInline, self)\
            .get_queryset(request).select_related('genre')


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'creation_date', 'rating')

    list_filter = ('type',)

    fields = (
        'title', 'type', 'description', 'creation_date', 'file_path', 'rating',
    )

    search_fields = ('title', 'description', 'id')

    inlines = [
        PersonRoleInline,
        GenreInline,
    ]


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name',)

    list_filter = ('full_name',)

    search_fields = ('full_name', 'id')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

    list_filter = ('name',)

    search_fields = ('name', 'description', 'id')
