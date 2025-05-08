import datetime
import json
import logging

_logger = logging.getLogger(__name__)

LEVEL_ERROR = 'Error'
LEVEL_WARNING = 'Warning'
LEVEL_INFORMATION = 'Information'


class LogLine:

    def __init__(self, line: str):
        self._line = line
        self._parsed_json_line = json.loads(self._line)

        self.timestamp = None
        self.level = ''
        self.message_template = ''
        self.properties = dict()
        self.exception_stacktrace = ''

        self._parse()

    def get_timestamp(self) -> datetime.datetime:
        return self.timestamp

    def get_level(self) -> str:
        return self.level

    def get_message_template(self) -> str:
        return self.message_template

    def get_properties(self) -> dict:
        return self.properties

    def get_exception_stacktrace(self) -> str:
        return self.exception_stacktrace

    def _parse(self):
        self.timestamp = datetime.datetime.fromisoformat(self._try_get('Timestamp'))
        self.level = self._try_get('Level')
        self.message_template = self._try_get('MessageTemplate')
        self.properties = self._try_get('Properties')
        self.exception_stacktrace = self._parse_stacktrace()

    def _try_get(self, key: str) -> str:
        try:
            return self._parsed_json_line[key]
        except KeyError as e:
            _logger.error(f'Could not extract field {key} from log line {self._line}!')
            return ''

    def _parse_stacktrace(self) -> str:
        if 'Exception' in self._parsed_json_line:
            stacktrace = self._try_get('Exception')

            if stacktrace:
                return stacktrace.replace('\r\n', '\n')

        return ''
