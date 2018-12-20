from typing import Callable, Dict, Optional, Union

from jinja2 import Environment, FileSystemLoader, Template
from sanic import Sanic
from sanic.response import html


class TemplatingMiddleware:
    def __init__(self, app: Sanic, path: str, filters: Optional[Dict[str, Callable]] = None) -> None:
        self.app = app
        loader = FileSystemLoader(searchpath=path)
        self.env = Environment(loader=loader)
        if filters:
            self.env.filters.update(filters)

        template_globals = dict(
            url_for=self.app.url_for
        )
        self.env.globals.update(template_globals)

        app.templating = self

    def render_template(self, template: Union[Template, str], **kwargs) -> str:
        template = self.env.get_template(template)
        return html(template.render(**kwargs))
