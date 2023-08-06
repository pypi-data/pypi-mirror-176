import typer
from rich import print

from gdshoplib import Description

app = typer.Typer()


@app.command()
def update_descriptions(sku=None):
    description = Description()
    if not sku:
        for product in description.notion_manager.get_products():
            description.update(product["sku"])
            print(f"Обновлен продукт {product['sku']}")
        return

    description.update(sku)
    print(f"Обновлен продукт {sku}")


@app.command()
def hello(name: str):
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
