from marshmallow import Schema, fields, ValidationError

def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')

class CategorySchema(Schema):
    items = fields.Nested('ItemSchema', many=True)
    class Meta:
        fields = ('id', 'name', 'items')

class ItemSchema(Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'category_id')

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
