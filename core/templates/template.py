from http import HTTPStatus

from jinja2 import Environment, FileSystemLoader, select_autoescape

from core.values import TEMPLATES


class BaseTemplate:
    template = 'error.html'

    def __init__(self, path: str, query: dict, params: dict):
        self.env = Environment(
            loader=FileSystemLoader(TEMPLATES),
            autoescape=select_autoescape()
        )
        self.query = query
        self.params = self.__construct_route_params(path, params)
        self.page = int(self.query.get('page', ['1'])[0])
        self._set_globals()

    @staticmethod
    def __construct_route_params(path: str, params: dict) -> dict:
        path = [part for part in path.split('/') if part]
        for name, index in params.items():
            params[name] = path[index]
        return params

    def render(self, **context) -> str:
        self._set_globals()
        return self.env.get_template(self.template).render(**context)

    def get_bool(self, getter: str) -> bool | None:
        if getter not in self.query or self.query[getter][0] not in ['0', '1']:
            return None
        return bool(int(self.query[getter][0]))

    def get_str(self, getter: str) -> bool | None:
        return self.query[getter][0] if getter in self.query else None

    def get_list(self, getter: str) -> list:
        return self.query[getter] if getter in self.query else []

    def _set_globals(self) -> None:
        self.env.globals.update(query=self._get_page())

    def _get_page(self) -> str:
        query_parts = [f'page={self.page + 1}']
        for key, values in self.query.items():
            if key == 'page':
                continue
            query_parts.extend([f'{key}={val}' for val in values])
        return '?' + '&'.join(query_parts)

    def error(self, status: HTTPStatus) -> str:
        return self.env.get_template('error.html').render(code=status.value, message=status.phrase)
