__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

from models import Asset, Product, User, Tag, Transaction, ProductTag, db
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from db_data_inserter import insert_data, create_assets, add_tags_to_products

console = Console()


def search(term):
    pass


def list_user_products(user_id):
    user = User.get_by_id(user_id)
    assets = Asset.select().where(Asset.owner == user)

    table = Table(
        title="List of products owned by:\n"
        + f"'{user.first_name} {user.last_name}'\n"
        + f"(user id: {user_id})"
    )
    table.add_column("Product name")
    table.add_column("Quantity", justify="right")

    for asset in assets:
        product = asset.product
        table.add_row(product.name, str(asset.product_quantity))

    console.print(Panel.fit(table))


def list_products_per_tag(tag_id):
    tag = Tag.get_by_id(tag_id)
    products_per_tag = [
        product
        for product in Product.select()
        if tag in product.descriptive_tags
    ]
    for product in products_per_tag:
        print(product.name)

    table = Table(
        title="List of products that have tag:"
        + f"{tag.name} (tag id: {tag_id}"
    )
    table.add_column("Product name")
    table.add_column("Quantity", justify="right")


def add_product_to_catalog(user_id, product):
    ...


def update_stock(product_id, new_quantity):
    ...


def purchase_product(product_id, buyer_id, quantity):
    ...


def remove_product(product_id):
    ...


def initialize_db():
    db.create_tables([Asset, Product, Tag, Transaction, User, ProductTag])
    insert_data()  # insert product, tag and user data
    create_assets()  # makes users own products (assets)
    add_tags_to_products()


initialize_db()
list_user_products(1)
list_products_per_tag(1)
