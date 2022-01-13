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
    print("")


def list_products_per_tag(tag_id):
    tag = Tag.get_by_id(tag_id)
    products_per_tag = [
        product
        for product in Product.select()
        if tag in product.descriptive_tags
    ]

    table = Table(
        title="List of products that have tag: "
        + f"'{tag.name}' (tag id: {tag_id})"
    )
    table.add_column("Product id", justify="right")
    table.add_column("Product name")
    for product in products_per_tag:
        table.add_row(str(product.id), product.name)
    console.print(Panel.fit(table))
    print("")


def add_product_to_catalog(user_id, product):
    product_id = product.id
    update_stock(user_id, product_id, 1)


def update_stock(user_id, product_id, new_quantity):
    user = User.get_by_id(user_id)
    product_to_add = Product.get_by_id(product_id)
    existing_asset = (
        Asset.select()
        .where(Asset.owner == user)
        .where(Asset.product == product_to_add)
        .first()
    )
    # is user does not yet have the product:
    if existing_asset is None:
        # create new asset
        Asset.create(
            owner=user, product=product_to_add, product_quantity=new_quantity
        )
        print(
            f"Added product '{product_to_add.name}' "
            + f"with a quantity of {new_quantity} "
            + f"to catalog of user '{user.first_name} {user.last_name}':"
        )
    # if user already has the product:
    else:
        # increase quantity of the product in the existing asset record
        existing_asset.product_quantity += new_quantity
        if existing_asset.product_quantity < 0:
            print("User cannot have a quantity of less than 0 of a product")
        existing_asset.save()
        print(
            f"For user '{user.first_name} {user.last_name}' "
            + f"quantity of product '{existing_asset.product.name}' "
            + f"has been updated from "
            + f"{existing_asset.product_quantity - new_quantity}"
            + f" to {existing_asset.product_quantity}:"
        )
    list_user_products(user_id)


def purchase_product(product_id, buyer_id, seller_id, quantity):
    seller = User.get_by_id(seller_id)
    buyer = User.get_by_id(buyer_id)
    product_to_purchase = Product.get_by_id(product_id)
    existing_asset_from_seller = (
        Asset.select()
        .where(Asset.owner == seller)
        .where(Asset.product == product_to_purchase)
        .first()
    )
    if seller == buyer:
        print(
            f"Sorry, {buyer.first_name} {buyer.last_name}, "
            + "you cannot buy products from yourself..."
        )
    # if seller does not have the product available:
    elif existing_asset_from_seller is None:
        print("The seller does not have the desired product")
    elif existing_asset_from_seller.product_quantity < quantity:
        print("The seller does not have the desired quantity of the product")
    else:
        print(
            "--- TRANSACTION ---\n"
            + f"A quantity of {quantity} "
            + f"of product '{product_to_purchase.name}' has been sold "
            + f"from '{seller.first_name} {seller.last_name}'"
            + f"to '{buyer.first_name} {buyer.last_name}': \n"
        )
        Transaction.create(
            buyer=buyer,
            seller=seller,
            product=product_to_purchase,
            product_quantity=quantity,
        )
        existing_asset_from_buyer = (
            Asset.select()
            .where(Asset.owner == buyer)
            .where(Asset.product == product_to_purchase)
            .first()
        )
        existing_buyer_product_quantity = 0
        if existing_asset_from_buyer is not None:
            existing_buyer_product_quantity = (
                existing_asset_from_buyer.product_quantity
            )
        update_stock(
            buyer.id,
            product_to_purchase.id,
            existing_buyer_product_quantity + quantity,
        )
        update_stock(
            seller.id,
            product_to_purchase.id,
            existing_asset_from_seller.product_quantity - quantity,
        )


def remove_product(user_id, product_id):
    update_stock(user_id, product_id, -1)


def initialize_db():
    db.create_tables([Asset, Product, Tag, Transaction, User, ProductTag])
    insert_data()  # insert product, tag and user data
    create_assets()  # makes users own products (create asset records in db)
    add_tags_to_products()


initialize_db()
list_user_products(1)
list_products_per_tag(1)
printje = Product.get_by_id(1)
statue = Product.get_by_id(2)
add_product_to_catalog(1, printje)
add_product_to_catalog(1, statue)
update_stock(1, 2, 4)
purchase_product(1, 2, 1, 2)
remove_product(1, 1)
