from models import Product
from rich.console import Console
from methods import (
    search,
    list_user_products,
    list_products_per_tag,
    add_product_to_catalog,
    update_stock,
    purchase_product,
    remove_product,
)

console = Console()
console_blue = Console(style="blue")


def show_demo():
    search_demo()
    list_user_products_demo()
    list_products_per_tag_demo()
    add_products_to_catalog_demo()
    update_stock_demo()
    purchase_product_demo()
    remove_product_demo()


def search_demo():
    console_blue.print(
        "\n[b]--- SEARCH EXAMPLE ---[/b]\n"
        + "This method looks for a search term in the "
        + "'name', 'description' and 'descriptive_tags' of all 'Product's.\n"
    )
    search("in")
    search("dog")
    search("diamond")


def list_user_products_demo():
    console_blue.print(
        "\n[b]--- LIST USER PRODUCTS EXAMPLE ---[/b]\n"
        + "This method shows a table with name and quantity of the 'Product's "
        + "that are registered as 'Asset' for a 'User'.\n"
    )
    list_user_products(1)


def list_products_per_tag_demo():
    console_blue.print(
        "\n[b]--- LIST PRODUCTS PER TAG EXAMPLE ---[/b]\n"
        + "This method shows a table with the id and name "
        + "of all the 'Product's that have a specific 'Tag'.\n"
    )
    list_products_per_tag(1)


def add_products_to_catalog_demo():
    console_blue.print(
        "\n[b]--- ADD PRODUCTS TO CATALOG EXAMPLES ---[/b]\n"
        + "This method will:\n"
        + "- Increase stock quantity by 1 "
        + "if the 'User' already has an 'Asset' for the specified 'Product'.\n"
        + "or:\n"
        + "- Create a new 'Asset' for the 'User' "
        + "if it does not have an 'Asset' of this 'Product' yet.\n"
    )
    art_print = Product.get_by_id(1)
    statue = Product.get_by_id(2)
    add_product_to_catalog(1, art_print)
    add_product_to_catalog(1, statue)


def update_stock_demo():
    console_blue.print(
        "\n[b]--- UPDATE STOCK EXAMPLE ---[/b]\n"
        + "With this method 'product_quantity' "
        + "of specifc 'Asset' can be updated for a 'User'.\n"
    )
    update_stock(1, 2, 7)


def purchase_product_demo():
    console_blue.print(
        "\n[b]--- PURCHASE PRODUCT EXAMPLE ---[/b]\n"
        + "If the 'seller' has the sufficient 'product_quantity' "
        + "of the 'Product' in an 'Asset', this method will:\n"
        + "1. Add the 'quantity' of 'Product' to the 'buyer's 'Asset';\n"
        + "2. Decrease 'product quantity' in the 'Asset' for the 'seller';\n"
        + "3. Log a 'Transaction' to the database.\n"
        + "Note: for step 1 and 2 the 'update_stock' method will be used.\n"
    )
    purchase_product(1, 2, 1, 2)


def remove_product_demo():
    console_blue.print(
        "\n[b]--- REMOVE PRODUCT EXAMPLE ---[/b]\n"
        + "If the 'User' has an 'Asset' of the 'Product' "
        + "with a 'product_quantity' of at least 1, this method will:\n"
        + "Decrease 'product quantity' by 1 in the 'Asset' "
        + "using the 'update_stock' method.\n"
    )
    console_blue.print("Remove Print from Alfred (he has 4):")
    remove_product(1, 1)
    console_blue.print("Remove Statue from Barry (he has 1):")
    remove_product(2, 2)
    console_blue.print("Try to remove Statue from Barry again, does not work:")
    remove_product(2, 2)
