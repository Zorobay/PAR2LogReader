from enum import StrEnum, auto


class LogLevel(StrEnum):
    def _generate_next_value_(name, start, count, last_values):
        return name.upper()

    @classmethod
    def get_by_name(cls, name: str) -> 'LogLevel':
        try:
            return LogLevel(name.upper())
        except KeyError:
            return LogLevel.UNKNOWN

    @classmethod
    def get_known_options(cls) -> list['LogLevel']:
        return [ll for ll in LogLevel if ll != LogLevel.UNKNOWN]

    def __str__(self):
        return self.value

    ERROR = auto()
    WARNING = auto()
    INFORMATION = auto()
    DEBUG = auto()
    UNKNOWN = auto()
