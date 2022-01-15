from models import Asset, Product, User, Tag, Transaction
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()
console_blue = Console(style="blue")


# ------------- SEARCH PRODUCTS -------------------------- #


def search(term):
    all_products = Product.select()
    products_with_term = find_products_with_term(term, all_products)
    table = create_search_results_table(term)
    fill_table_with_results(table, products_with_term, term)


def create_search_results_table(term):
    table = Table(
        title=f"Product search results for: '[r]{term}[/r]'", show_lines=True
    )
    table.add_column("Product name")
    table.add_column("Product description")
    table.add_column("Product tags")
    return table


def fill_table_with_results(table, products_with_term, term):
    for product in products_with_term:

        name = highlight(term, product.name)
        description = highlight(term, product.description)

        product_tags = ""
        for tag in product.descriptive_tags:
            product_tags += f"{tag.name}, "
        product_tags = product_tags[:-2]
        product_tags = highlight(term, product_tags)

        table.add_row(name, description, product_tags)
    console.print(Panel.fit(table))
    print()


def highlight(term, full_string):
    return ireplace(term, f"[r]{term}[/r]", full_string)


def find_products_with_term(term, products):
    products_with_term = []
    for product in products:
        if (
            term in product.name
            or term in product.description
            or term_in_descriptive_tags(term, product)
        ):
            products_with_term.append(product)
    return products_with_term


def ireplace(old, new, text):
    idx = 0
    while idx < len(text):
        index_l = text.lower().find(old.lower(), idx)
        if index_l == -1:
            return text
        text = text[:index_l] + new + text[index_l + len(old) :]
        idx = index_l + len(new)
    return text


def term_in_descriptive_tags(term, product):
    for tag in product.descriptive_tags:
        if term in tag.name:
            return True
    return False


# -------------- LIST USER PRODUCTS ---------------------- #


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


# -------------- LIST PRODUCTS PER TAG ------------------- #


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


# -------------- UPDATE STOCK ---------------------------- #


def update_stock(user_id, product_id, new_quantity):
    user = User.get_by_id(user_id)
    product = Product.get_by_id(product_id)
    asset = get_asset(user, product)
    # is user does not yet have the product:
    if asset is None:
        create_asset(new_quantity, user, product)
    # else: (if user already has an Asset for the product)
    else:
        # if user's quantity of the product is zero or negative: print error
        if asset.product_quantity <= 0:
            print_quantity_error(product)
            return
        # else: update quantity of the product in user's existing asset record
        else:
            update_product_quantity_in_asset(new_quantity, user, asset)
    list_user_products(user_id)


def update_product_quantity_in_asset(new_quantity, user, asset):
    asset.product_quantity = new_quantity
    asset.save()
    console.print(
        f"For user '{user.first_name} {user.last_name}' "
        + f"quantity of product '{asset.product.name}' "
        + f"has been updated to {asset.product_quantity}:"
    )


def print_quantity_error(product):
    console.print(f"Stock of product '{product.name}' not updated.")
    console.print("User cannot have a quantity of less than 0 of a product.")


def create_asset(new_quantity, user, product):
    Asset.create(
        owner=user,
        product=product,
        product_quantity=new_quantity,
    )
    console.print(
        f"Added product '{product.name}' "
        + f"with a quantity of {new_quantity} "
        + f"to the catalog of user '{user.first_name} {user.last_name}':"
    )


def get_asset(user, product):
    asset = (
        Asset.select()
        .where(Asset.owner == user)
        .where(Asset.product == product)
        .first()
    )
    return asset


# -------------- ADD PRODUCT TO CATALOG ------------------ #


def add_product_to_catalog(user_id, product):
    user = User.get_by_id(user_id)
    product_id = product.id
    existing_asset = get_asset(user, product)
    if existing_asset is None:
        update_stock(user_id, product_id, 1)
    else:
        update_stock(user_id, product_id, existing_asset.product_quantity + 1)


# -------------- PURCHASE PRODUCT ------------------------ #


def purchase_product(product_id, buyer_id, seller_id, quantity):
    product = Product.get_by_id(product_id)
    seller = User.get_by_id(seller_id)
    buyer = User.get_by_id(buyer_id)
    seller_asset = get_asset(seller, product)
    seller_stock = seller_asset.product_quantity
    if purchase_is_valid(quantity, seller, buyer, seller_asset, seller_stock):
        process_transaction(quantity, product, seller, buyer, seller_stock)


def purchase_is_valid(quantity, seller, buyer, seller_asset, seller_stock):
    purchase_ok = False
    if seller == buyer:
        console.print("Sorry, you cannot buy products from yourself.")
    elif quantity < 1:
        console.print("Sorry, you cannot purchase zero or negative quantity.")
    # if seller does not have the product available:
    elif seller_asset is None:
        console.print("The seller does not have the desired product.")
    elif seller_stock < quantity:
        console.print("Seller has insufficient quantity of the product.")
    else:
        purchase_ok = True
    return purchase_ok


def process_transaction(quantity, product, seller, buyer, seller_stock):
    create_transaction(quantity, product, seller, buyer)
    print_transaction_info(quantity, product, seller, buyer)
    buyer_asset = get_asset(buyer, product)
    buyer_stock = 0
    seller_new_stock = seller_stock - quantity
    if buyer_asset is not None:
        buyer_stock = buyer_asset.product_quantity
    update_stock(buyer.id, product.id, buyer_stock + quantity)
    update_stock(seller.id, product.id, seller_new_stock)


def create_transaction(quantity, product, seller, buyer):
    Transaction.create(
        buyer=buyer,
        seller=seller,
        product=product,
        product_quantity=quantity,
    )


def print_transaction_info(quantity, product, seller, buyer):
    console.print(
        "---- TRANSACTION ----\n"
        + f"A quantity of {quantity} "
        + f"of product '{product.name}' has been sold "
        + f"from '{seller.first_name} {seller.last_name}' "
        + f"to '{buyer.first_name} {buyer.last_name}': \n"
    )


# -------------- REMOVE PRODUCT -------------------------- #


def remove_product(user_id, product_id):
    user = User.get_by_id(user_id)
    product = Product.get_by_id(product_id)
    existing_asset = get_asset(user, product)
    if existing_asset is None:
        console.print("The seller does not have this product")
    else:
        new_quantity = existing_asset.product_quantity - 1
        update_stock(user_id, product_id, new_quantity)
