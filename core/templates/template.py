from http import HTTPStatus

from jinja2 import Environment, FileSystemLoader, select_autoescape

from core.values import TEMPLATES


class BaseTemplate:
    def __init__(self, path: str, query: dict):
        self.env = Environment(
            loader=FileSystemLoader(TEMPLATES),
            autoescape=select_autoescape()
        )
        self.path = path
        self.query = query

    def error(self, status: HTTPStatus):
        return self.env.get_template('error.html').render(code=status.value, message=status.phrase)
