from dataclasses import asdict, dataclass
from datetime import datetime, timezone

from storage import BaseStorage


@dataclass
class State:
    update_date: datetime = str(datetime(day=1, month=1, year=1900, microsecond=1, tzinfo=timezone.utc))
    offset_person: int = 0
    offset_genre: int = 0
    offset_film_works: int = 0


class StateManager:
    """Класс для работы с состояниями."""

    def __init__(self, storage: BaseStorage) -> None:
        self.storage = storage

    def set_state(self, state: State) -> None:
        """Установить состояние"""
        self.storage.save_state(asdict(state))

    def get_state(self) -> State:
        """Получить состояние"""
        d_storage = self.storage.retrieve_state()
        state = State()
        if d_storage:
            state = State(update_date=datetime.strptime(d_storage['update_date'], '%Y-%m-%d %H:%M:%S.%f%z'),
                          offset_genre=d_storage['offset_genre'],
                          offset_person=d_storage['offset_person'],
                          offset_film_works=d_storage['offset_film_works']
                          )
        return state
