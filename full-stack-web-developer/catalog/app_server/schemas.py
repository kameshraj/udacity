from marshmallow import Schema, fields, ValidationError

def must_not_be_blank(data):
    """
    Validates given form data in not null

    Arguments:
        data: Any data to validate
    """
    if not data:
        raise ValidationError('Data not provided.')


class CategorySchema(Schema):
    """
    Schema for Categories table. Will also pull all items for this category
    """
    items = fields.Nested('ItemSchema', many=True)
    class Meta:
        fields = ('id', 'name', 'items')


class ItemSchema(Schema):
    """
    Schema for Items table.
    """
    class Meta:
        fields = ('id', 'name', 'description', 'category_id')


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
