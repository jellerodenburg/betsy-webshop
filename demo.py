from models import Product
from rich.console import Console
from methods import (
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

    console_blue.print(
        "\n--- LIST USER PRODUCTS EXAMPLE ---\n"
        + "This method shows a table with name and quantity of the 'Product's "
        + "that are registered as 'Asset' for a 'User'.\n"
    )
    list_user_products(1)

    console_blue.print(
        "\n--- LIST PRODUCTS PER TAG EXAMPLE ---\n"
        + "This method shows a table with the id and name of all the 'Product's"
        + " that have a specific 'Tag'.\n"
    )
    list_products_per_tag(1)

    console_blue.print(
        "\n--- ADD PRODUCTS TO CATALOG EXAMPLES ---\n"
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

    console_blue.print(
        "\n--- UPDATE STOCK EXAMPLE ---\n"
        + "With this method you can update 'product_quantity' "
        + "of specifc 'Asset' for a 'User'.\n"
        + "The argument quantity can be a positive number (increase) "
        + "or negative number (decrease) to update stock quantity with.\n"
    )
    update_stock(1, 2, 4)

    console_blue.print(
        "\n--- PURCHASE PRODUCT EXAMPLE ---\n"
        + "If the 'seller' has the sufficient 'product_quantity' "
        + "of the 'Product' in an 'Asset', this method will:\n"
        + "1. Add the specified 'quantity' of 'Product' to the 'buyer's 'Asset';\n"
        + "2. Decrease 'product quantity' in the 'Asset' for the 'seller';\n"
        + "3. Log a 'Transaction' to the database.\n"
        + "Note: for step 1 and 2 the 'update_stock' method will be used.\n"
    )
    purchase_product(1, 2, 1, 2)

    console_blue.print(
        "\n--- REMOVE PRODUCT EXAMPLE ---\n"
        + "If the 'User' has an 'Asset' of the 'Product' "
        + "with a 'product_quantity' of at least 1, this method will:\n"
        + "Decrease 'product quantity' in the 'Asset' "
        + "using the 'update_stock' method.\n"
    )
    remove_product(1, 1)
    remove_product(1, 3)
    remove_product(1, 3)
    remove_product(1, 3)
    remove_product(1, 3)
    remove_product(1, 3)
