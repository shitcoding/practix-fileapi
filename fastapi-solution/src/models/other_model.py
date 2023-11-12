from templ_model import IdMix


class Genre(IdMix):
    name: str

class Person(IdMix):
    full_name: str