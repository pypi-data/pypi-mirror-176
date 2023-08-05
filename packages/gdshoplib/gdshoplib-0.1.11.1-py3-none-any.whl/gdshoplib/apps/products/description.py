# Работа с описаниями товаров
from jinja2 import Environment, FileSystemLoader, select_autoescape

from gdshoplib.core import BaseManager, settings
from gdshoplib.services import NotionManager


class Description:
    def __init__(self):
        self.jinja2_env = self.jinja2_env()

    def get(self, sku, platform):
        """Получить описание"""
        return self.render(
            BaseManager.get_manager_by_key(platform)(cache=True),
            NotionManager(cache=True).get_product(sku),
        )

    def update_products(self):
        ...

    def get_template(self, manager):
        return self.jinja2_env.get_template(manager.DESCRIPTION_TEMPLATE)

    def render(self, manager, params):
        return self.get_template(manager).render(product=params)

    @classmethod
    def jinja2_env(cls):
        return Environment(
            loader=FileSystemLoader(settings.TEMPLATES_PATH),
            autoescape=select_autoescape(),
        )
