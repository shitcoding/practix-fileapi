from data import ESData, ESGenre, ESPerson, FilmWork, Role


class Transformer:
    def transform_film_work_to_es(self, film_works: dict[str, FilmWork]) -> list[ESData]:
        res = []
        for fw in film_works.values():
            directors, actors, writers = self._parse_persons(fw)
            genres = [ESGenre(uuid=str(genre.id), name=genre.name) for genre in fw.genres.values()]
            actors_names = [actor.full_name for actor in actors]
            writers_names = [writer.full_name for writer in writers]
            es_data = ESData(uuid=str(fw.id),
                             title=fw.title,
                             imdb_rating=fw.rating,
                             description=fw.description,
                             file_path=fw.file_path,
                             genre=genres,
                             directors=directors,
                             actors=actors,
                             actors_names=actors_names,
                             writers=writers,
                             writers_names=writers_names)
            res.append(es_data)
        return res

    @staticmethod
    def _parse_persons(film_work: FilmWork) -> (list[ESPerson], list[ESPerson], list[ESPerson]):
        actors = []
        writers = []
        directors = []
        for person in film_work.persons.values():
            es_person = ESPerson(uuid=str(person.id), full_name=person.name)
            if person.role == Role.ACTOR:
                actors.append(es_person)
            elif person.role == Role.WRITER:
                writers.append(es_person)
            else:
                directors.append(es_person)
        return directors, actors, writers
