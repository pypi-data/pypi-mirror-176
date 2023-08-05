# Менеджер управления Notion
import json
from random import randrange

from dateutil.parser import parse as date_parser
from gdshoplib.core import BaseManager
from gdshoplib.services.notion.models import (
    Product,
    ProductProperties,
    ProductSettingsBlock,
    ProductDescriptionBlock,
    User,
    properties_type_parse_map,
    properties_keys_map,
)
from gdshoplib.services.notion.settings import Settings
from gdshoplib.packages.lang import transliterate


class NotionManager(BaseManager):
    SETTINGS = Settings
    BASE_URL = "https://api.notion.com/v1/"

    def get_headers(self):
        return {
            **self.auth_headers(),
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
            "Accept": "application/json",
        }

    def auth(self):
        return True

    def auth_headers(self):
        return {"Authorization": "Bearer " + self.settings.NOTION_SECRET_TOKEN}

    def get_user(self, user_id):
        data = self.make_request(f"users/{user_id}", method="get").json()
        if data.get("results"):
            data = data.get("results")[0]
        return User.parse_obj(
            {**data, "email": data.get("person", {}).get("email") or data.get("name")}
        )

    def is_settings_block(self, capture):
        return "base_settings" in capture

    def is_description_block(self, capture):
        return "description" in capture

    def set_technical_blocks(self, product: Product):
        # Поиск блока с настройками и загрузка
        for block_response in self.pagination(
            f"blocks/{product.id}/children/", method="get"
        ):
            for raw_block in block_response.json()["results"]:
                if raw_block["type"] != "code":
                    continue

                capture = raw_block["code"].get("caption", [{}])[0].get("plain_text")
                content = properties_type_parse_map["rich_text"](raw_block["code"])

                if self.is_settings_block(capture):
                    block = ProductSettingsBlock(
                        id=raw_block["id"], **json.loads(content)
                    )
                    product.settings = block

                elif self.is_description_block(capture):
                    platform = capture.split(":")
                    platform = platform[-1].upper() if len(platform) > 1 else None
                    block = ProductDescriptionBlock(
                        id=raw_block["id"],
                        platform=platform if platform else None,
                        description=content,
                    )
                    product.descriptions[platform] = block

    def get_products(self):
        products = []
        for page in self.pagination(
            f"databases/{self.settings.PRODUCT_DB}/query", method="post", params=None
        ):
            for raw_product in page.json()["results"]:
                product = self.parse_product(raw_product)
                products.append(product.dict())

        return products

    def get_product(self, sku):
        data = self.make_request(
            f"databases/{self.settings.PRODUCT_DB}/query",
            method="post",
            params={"filter": {"property": "Наш SKU", "rich_text": {"contains": sku}}},
        ).json()["results"]

        try:
            return self.parse_product(data[0]).dict()
        except IndexError:
            return None

    def generate_sku(self, product):
        # Сгенерировать SKU на основе продукта
        # Категория.Бренд.Цена_покупки.месяц_добавления.год_добавления.случайные_4_числа

        created_at = date_parser(product["created_at"])
        sku = (
            f"{transliterate(product['category_product']).upper()}."
            f"{product['description_brand'].upper()}."
            f"{product['price_source']}."
            f"{created_at.month}."
            f"{created_at.year}."
            f"{randrange(1111, 9999)}"
        )

        return sku.replace(" ", "")

    def set_sku(self):
        # Найти товары без SKU и проставить
        for page in self.pagination(
            f"databases/{self.settings.PRODUCT_DB}/query",
            method="post",
            params={"filter": {"property": "Наш SKU", "rich_text": {"is_empty": True}}},
        ):
            for raw_product in page.json()["results"]:
                product = self.parse_product(raw_product)
                sku = self.generate_sku(product.dict())
                assert self.update_sku(
                    product.id, sku
                ), f"Не удалось обновить SKU для {raw_product['url']}"

    def update_sku(self, product_id, sku):
        _r = self.make_request(
            f"pages/{product_id}",
            method="patch",
            params={"properties": {"Наш SKU": [{"text": {"content": sku}}]}},
        )
        return _r.ok

    def update_block(self, block_id, content):
        _r = self.make_request(
            f"blocks/{block_id}",
            method="patch",
            params={"code": {"rich_text": [{"text": {"content": content}}]}},
        )
        return _r.ok

    def parse_properties(self, properties):
        result = []
        for k, v in properties.items():
            prop = properties_keys_map.get(v["id"], {})
            if not prop.get("key"):
                continue

            value_parser = properties_type_parse_map.get(
                v["type"], lambda data: str(data)
            )

            result.append(
                ProductProperties(
                    name=k,
                    value=value_parser(v),
                    key=prop.get("key"),
                    addon=prop.get("addon"),
                )
            )

        return result

    def parse_product(self, product):
        _product = Product.parse_obj(
            {
                **product,
                **{
                    "created_by": self.get_user(product["created_by"]["id"]).email,
                    "last_edited_by": self.get_user(
                        product["last_edited_by"]["id"]
                    ).email,
                    "properties": self.parse_properties(product["properties"]),
                },
            }
        )
        self.set_technical_blocks(_product)
        return _product

    def pagination(self, url, *, params=None, **kwargs):
        _params = params or {}
        response = None
        while True:
            response = self.make_request(url, params=_params, **kwargs)
            next_cursor = self.pagination_next(response)

            match next_cursor:
                case None:
                    yield response
                case False:
                    yield response
                    return
                case _:
                    _params = {**_params, **dict(start_cursor=next_cursor)}

    def pagination_next(self, response):
        """Выдаем данные для следующего"""
        if not response:
            return None

        if not response.json().get("has_more"):
            return False

        return response.json()["next_cursor"]
