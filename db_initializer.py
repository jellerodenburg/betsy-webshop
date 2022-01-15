from models import Asset, Product, User, Tag, Transaction, ProductTag, db
from example_data import users, tags, products


def initialize_db():
    db.create_tables([Asset, Product, Tag, Transaction, User, ProductTag])
    insert_data()  # insert product, tag and user data
    create_assets()  # makes users own products (create Asset records in db)
    add_tags_to_products()


def insert_data():

    with db.atomic():

        User.insert_many(
            users,
            fields=[
                User.first_name,
                User.last_name,
                User.street,
                User.house_number,
                User.house_number_addition,
                User.postal_code,
                User.city,
                User.email,
                User.telephone,
            ],
        ).execute()

        Tag.insert_many(tags).execute()

        Product.insert_many(
            products,
            fields=[
                Product.name,
                Product.description,
                Product.price_per_unit_in_cents,
            ],
        ).execute()


def create_assets():
    # get users
    alfred = User.get_by_id(1)
    barry = User.get_by_id(2)
    cornelis = User.get_by_id(3)

    # get products
    print = Product.get_by_id(1)
    statue = Product.get_by_id(2)
    bracelet = Product.get_by_id(3)
    # link users to products
    Asset.create(owner=alfred, product=print, product_quantity=5)
    Asset.create(owner=alfred, product=bracelet, product_quantity=3)
    Asset.create(owner=barry, product=statue, product_quantity=1)
    Asset.create(owner=cornelis, product=bracelet, product_quantity=3)


def add_tags_to_products():
    # get products
    print = Product.get_by_id(1)
    statue = Product.get_by_id(2)
    # get tags
    tag_art = Tag.get_by_id(1)
    tag_print = Tag.get_by_id(2)
    tag_red = Tag.get_by_id(3)
    tag_white = Tag.get_by_id(4)
    tag_blue = Tag.get_by_id(5)
    tag_pink = Tag.get_by_id(6)

    # add tags to the print product
    print.descriptive_tags.add(
        [tag_art, tag_print, tag_red, tag_white, tag_blue, tag_pink]
    )
    statue.descriptive_tags.add(tag_art)