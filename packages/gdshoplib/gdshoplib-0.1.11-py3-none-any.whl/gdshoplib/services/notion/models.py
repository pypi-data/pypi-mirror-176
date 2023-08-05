from typing import Callable, Dict, List, Optional, Union
from pydantic import BaseModel


def list_addon(data):
    if "/" in data:
        return [i.strip() for i in data.split("/")]
    return data


properties_keys_map = {
    "title": dict(name="Name", key="title"),
    "BeEA": dict(name="Публикация", key="status_public"),
    "MUl%7C": dict(name="Статус описания", key="status_description"),
    "BKOs": dict(name="Наш SKU", key="sku"),
    "pXTy": dict(name="Количество", key="quantity"),
    #
    "iwg%3C": dict(name="🎟️ Поставщик", key="supplier"),
    "BHve": dict(name="SKU поставщика", key="sku_supplier"),
    #
    "NEgM": dict(name="Категория товара", key="category_product"),
    "ePC%5C": dict(name="Вид спорта", key="product_sport"),
    #
    "%3D%3FrC": dict(name="🐴 Каналы", key="chanels"),
    "AyqD": dict(name="Цена (eur)", key="price_source"),
    #
    "TbyK": dict(name="Created by", key="created_by"),
    "v%5Dsj": dict(name="Created time", key="created_at"),
    "~%7BrF": dict(name="Last edited by", key="updated_by"),
    "mVEw": dict(name="Last edited time", key="updated_at"),
    #
    "pyiW": dict(name="Закупочная", key="price_supplier"),
    "opcQ": dict(name="Себестоимость", key="price_buy"),
    "VmWm": dict(name="Базовая", key="price_base"),
    "x%3A%5Ci": dict(name="Ходовая", key="price_general"),
    "%7Bh%7D%7B": dict(name="Скидка, 10%", key="price_sale_10"),
    "cPu~": dict(name="Скидка, 20%", key="price_sale_20"),
    "%7D%7CBr": dict(name="Скидка, 30%", key="price_sale_30"),
    #
    "COmf": dict(
        name="Материалы / Состав", key="description_materials", addon=list_addon
    ),
    "HI%5DA": dict(name="Основное фото", key="photo_general"),
    "Jvku": dict(name="Цвет", key="description_color"),
    "PJXf": dict(name="ШиринаxГлубинаxВысота (мм)", key="description_measurement"),
    "Tss%5D": dict(name="Название на русском", key="description_title"),
    "W%5BhI": dict(name="Коллекция", key="description_collection"),
    "%5DZ%3Az": dict(name="Бренд", key="description_brand"),
    "%5Dk%5CH": dict(name="Фото коллекции", key="photo_collection"),
    "%60jru": dict(name="Фото с сантиметром", key="photo_size"),
    "jiSN": dict(name="Подробное видео с голосом", key="video_description"),
    "sXND": dict(name="Примечания", key="description_notes", addon=list_addon),
    "taW%3B": dict(name="Размер", key="description_size"),
    "u_tU": dict(name="Короткое описание", key="description_short"),
    "ytWy": dict(name="Вес (кг)", key="description_weight"),
    "zejc": dict(name="Видео рилс", key="video_reals"),
    "MqdC": dict(name="Теги", key="tags", addon=list_addon),
}

properties_type_parse_map = {
    "rich_text": lambda data: " ".join(
        [t.get("plain_text", "") for t in data["rich_text"]]
    )
    or "",
    "number": lambda data: data["number"],
    "select": lambda data: data.get("select").get("name")
    if data.get("select")
    else None,
    "multi_select": lambda data: data,
    "status": lambda data: data["status"]["name"],
    "date": lambda data: data,
    "formula": lambda data: data["formula"]["number"],
    # "relation": lambda data: "",
    "rollup": lambda data: data,
    # "title": lambda data: data,
    "people": lambda data: data,
    "files": lambda data: data,
    "checkbox": lambda data: data,
    "url": lambda data: data["url"],
    "email": lambda data: data,
    "phone_number": lambda data: data,
    "created_time": lambda data: data["created_time"],
    # "created_by": lambda data: User.parse_obj(data),
    "last_edited_time": lambda data: data["last_edited_time"],
    # "last_edited_by": lambda data: User.parse_obj(data)
}


class ProductProperties(BaseModel):
    name: str
    key: str
    value: Optional[str]
    addon: Optional[Callable]


class ProductSettingsBlock(BaseModel):
    id: str
    media: Dict[str, List[Optional[str]]]
    price: Dict[str, Union[int, str]]


class ProductDescriptionBlock(BaseModel):
    id: str
    platform: Optional[str]
    description: str


class Product(BaseModel):
    # Нужна полноценная карточка товара со всеми параметрами
    id: str
    properties: List[ProductProperties]
    settings: Optional[ProductDescriptionBlock]
    descriptions: Dict[Union[str, None], ProductDescriptionBlock] = {}

    def dict(self, *args, **kwargs):
        _d = super(Product, self).dict(*args, **kwargs)

        props = {}
        for prop in self.properties:
            props[prop.key] = prop.addon(prop.value) if prop.addon else prop.value

        return {**_d, **props}


class User(BaseModel):
    id: str
    name: str
    email: str
