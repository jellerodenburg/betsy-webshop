from models import Asset, Product, User, Tag, Transaction
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()
console_blue = Console(style="blue")


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
    print()


def list_products_per_tag(tag_id):
    tag = Tag.get_by_id(tag_id)
    products_per_tag = [
        product
        for product in Product.select()
        if tag in product.descriptive_tags
    ]
    table = Table(
        title="List of products with descriptive tag: "
        + f"'{tag.name}'\n(tag id: {tag_id})"
    )
    table.add_column("Product id", justify="right")
    table.add_column("Product name")
    for product in products_per_tag:
        table.add_row(str(product.id), product.name)
    console.print(Panel.fit(table))
    print()


def update_stock(user_id, product_id, new_quantity):
    user = User.get_by_id(user_id)
    product_to_update = Product.get_by_id(product_id)
    existing_asset = (
        Asset.select()
        .where(Asset.owner == user)
        .where(Asset.product == product_to_update)
        .first()
    )
    # is user does not yet have the product:
    if existing_asset is None:
        # create new asset
        Asset.create(
            owner=user,
            product=product_to_update,
            product_quantity=new_quantity,
        )
        console.print(
            f"Added product '{product_to_update.name}' "
            + f"with a quantity of {new_quantity} "
            + f"to the catalog of user '{user.first_name} {user.last_name}':"
        )
    # if user already has the product:
    else:
        # if the quantity of the product is zero or negative: do nothing
        if existing_asset.product_quantity <= 0:
            console.print(
                f"Stock of product '{product_to_update.name}' not updated."
            )
            console.print(
                "User cannot have a quantity of less than 0 of a product."
            )
        # else: update quantity of the product in the existing asset record
        else:
            existing_asset.product_quantity = new_quantity
            existing_asset.save()
            console.print(
                f"For user '{user.first_name} {user.last_name}' "
                + f"quantity of product '{existing_asset.product.name}' "
                + f"has been updated to {existing_asset.product_quantity}:"
            )
    list_user_products(user_id)


def add_product_to_catalog(user_id, product):
    user = User.get_by_id(user_id)
    product_id = product.id
    existing_asset = (
        Asset.select()
        .where(Asset.owner == user)
        .where(Asset.product == product)
        .first()
    )
    if existing_asset is None:
        update_stock(user_id, product_id, 1)
    else:
        update_stock(user_id, product_id, existing_asset.product_quantity + 1)


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
        console.print(
            f"Sorry, {buyer.first_name} {buyer.last_name}, "
            + "you cannot buy products from yourself..."
        )
    # if seller does not have the product available:
    elif existing_asset_from_seller is None:
        console.print("The seller does not have the desired product")
    elif existing_asset_from_seller.product_quantity < quantity:
        console.print(
            "The seller does not have sufficient quantity of the product"
        )
    else:
        console.print(
            "----- TRANSACTION ------------\n"
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
            (existing_asset_from_seller.product_quantity + quantity),
        )


def remove_product(user_id, product_id):
    "----- REMOVE PRODUCT ------------\n"
    user = User.get_by_id(user_id)
    product = Product.get_by_id(product_id)
    existing_asset = (
        Asset.select()
        .where(Asset.owner == user)
        .where(Asset.product == product)
        .first()
    )
    if existing_asset is None:
        console.print("The seller does not have this product")
    else:
        update_stock(user_id, product_id, existing_asset.product_quantity - 1)
