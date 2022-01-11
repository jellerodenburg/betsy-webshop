import peewee

db = peewee.SqliteDatabase(":memory:")


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Tag(BaseModel):
    name = peewee.CharField()


class Product(BaseModel):
    name = peewee.CharField()
    description = peewee.CharField()
    descriptive_tags = peewee.ManyToManyField(Tag)
    price_per_unit_in_cents = peewee.IntegerField()


class User(BaseModel):
    first_name = peewee.CharField()
    last_name = peewee.CharField()
    street = peewee.CharField()
    house_number = peewee.CharField()
    house_number_addition = peewee.CharField()
    postal_code = peewee.CharField()
    city = peewee.CharField()
    email = peewee.CharField()
    telephone = peewee.CharField()


class Asset(BaseModel):
    owner = peewee.ForeignKeyField(User)
    product = peewee.ForeignKeyField(Product)
    product_quantity = peewee.IntegerField()


class Transaction(BaseModel):
    buyer = peewee.ForeignKeyField(User)
    seller = peewee.ForeignKeyField(User)
    product = peewee.ForeignKeyField(Product)
    product_quantity = peewee.IntegerField()


ProductTag = Product.descriptive_tags.get_through_model()
