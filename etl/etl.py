import logging
from datetime import datetime, timezone

from config.config import DSN, ES_SERVER, LIMIT, SCHEMA
from data import ESData, FilmWork
from extraction import PostgresExtractor, TablesNames
from loading import ESLoader
from state import State, StateManager
from storage import JsonFileStorage
from transformation import Transformer

logger = logging.getLogger(__name__)


class ETL:
    def __init__(self):
        logger.info("Инициализируем ETL")
        tn = TablesNames(
            film_work="film_work",
            genre="genre",
            genre_film_work="genre_film_work",
            person="person",
            person_film_work="person_film_work"
        )
        self._state_manager = StateManager(JsonFileStorage('state.json'))
        self._state = self._state_manager.get_state()
        self._extractor = PostgresExtractor(dsn=DSN, schema_name=SCHEMA, tables_names=tn)
        self._transformer = Transformer()
        self._loader = ESLoader(es_server=ES_SERVER)

    def run(self):
        amount = 1
        while amount > 0:
            film_works = self._extract_film_works(self._state)
            transformed_film_works = self._transform_film_works(film_works)
            amount = self._loader.load_es_data(transformed_film_works)
            if amount > 0:
                self._state.offset_genre += LIMIT
                self._state.offset_person += LIMIT
                self._state.offset_film_works += LIMIT
            else:
                self._state.offset_genre = 0
                self._state.offset_person = 0
                self._state.offset_film_works = 0
                self._state.update_date = str(datetime.now(timezone.utc))
            self._state_manager.set_state(self._state)

    def _extract_film_works(self, state: State) -> dict[str, FilmWork]:
        film_works = self._extractor.extract_data(state)
        return film_works

    def _transform_film_works(self, film_works: dict[str, FilmWork]) -> list[ESData]:
        return self._transformer.transform_to_es(film_works)
