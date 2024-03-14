import re

from core.templates.template import BaseTemplate

urls = [
    ('/home', BaseTemplate),
]


class Routes:
    def __init__(self):
        self.routes = {}
        self.regex = {'token': re.compile(r'\w{8}'), 'string': re.compile(r'[.\w-]*')}
        self.temp_parts = []
        self.temp_tokens = {}

    def add_regex(self, key: str, pattern: re.Pattern) -> None:
        self.regex[key] = pattern

    def __check_part(self, index: int, part: str) -> str | re.Pattern:
        if part.startswith('{') and part.endswith('}'):
            key, name = part.split(':', 1)
            self.temp_tokens[name] = index
            return self.regex[key]
        return part

    def __clear_temp(self) -> None:
        self.temp_parts.clear()
        self.temp_tokens.clear()

    def construct_routes(self, routes: list[tuple]) -> dict:
        for route in routes:
            route, clazz = route
            split_route = [part for part in route.split('/') if part]
            for index, part in enumerate(split_route):
                self.temp_parts.append(self.__check_part(index, part))
            full_route = '/' + '/'.join(self.temp_parts)
            self.routes[re.compile(full_route)] = (clazz, self.temp_tokens.copy())
            self.__clear_temp()
        return self.routes


url_route = Routes()
