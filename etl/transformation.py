from data import ESData, ESPerson, FilmWork, Role


class Transformer:
    def transform_film_work_to_es(self, film_works: dict[str, FilmWork]) -> list[ESData]:
        res = []
        for fw in film_works.values():
            director, actors, writers = self._parse_persons(fw)
            genres = [genre.name for genre in fw.genres.values()]
            actors_names = [actor.name for actor in actors]
            writers_names = [writer.name for writer in writers]
            es_data = ESData(id=str(fw.id),
                             title=fw.title,
                             imdb_rating=fw.rating,
                             description=fw.description,
                             genre=genres,
                             director=director,
                             actors=actors,
                             actors_names=actors_names,
                             writers=writers,
                             writers_names=writers_names)
            res.append(es_data)
        return res

    @staticmethod
    def _parse_persons(film_work: FilmWork) -> (str, list[ESPerson], list[ESPerson]):
        actors = []
        writers = []
        director = ''
        for person in film_work.persons.values():
            es_person = ESPerson(id=str(person.id), name=person.name)
            if person.role == Role.ACTOR:
                actors.append(es_person)
            elif person.role == Role.WRITER:
                writers.append(es_person)
            else:
                director = person.name
        return director, actors, writers
