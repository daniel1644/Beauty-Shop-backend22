from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=4))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    description = fields.Str()
    category = fields.Str(required=True)
    stock = fields.Int()

class CartItemSchema(Schema):
    id = fields.Int(dump_only=True)
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True)
    user_id = fields.Int(required=True)

class OrderSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    total = fields.Float(required=True)
    items = fields.List(fields.Nested('OrderItemSchema'))

class OrderItemSchema(Schema):
    id = fields.Int(dump_only=True)
    product_id = fields.Int(required=True)
    order_id = fields.Int(required=True)
    quantity = fields.Int(required=True)
