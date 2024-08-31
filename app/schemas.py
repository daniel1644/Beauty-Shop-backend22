from marshmallow import Schema, fields, validate, validates, ValidationError
from app.models import User, Product, Order, OrderItem

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=4, max=50))
    email = fields.Email(required=True, validate=validate.Length(max=120))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    
    @validates('username')
    def validate_username(self, value):
        if User.query.filter_by(username=value).first():
            raise ValidationError("Username is already taken.")

class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    price = fields.Float(required=True, validate=validate.Range(min=0.01))
    description = fields.Str(validate=validate.Length(max=500))
    category = fields.Str(required=True, validate=validate.Length(max=50))
    stock = fields.Int(required=True, validate=validate.Range(min=0))

    @validates('name')
    def validate_product_name(self, value):
        if Product.query.filter_by(name=value).first():
            raise ValidationError("Product name must be unique.")
    
    @validates('category')
    def validate_category(self, value):
        allowed_categories = ["Electronics", "Clothing", "Beauty", "Home", "Toys", "Books"]
        if value not in allowed_categories:
            raise ValidationError(f"Category must be one of: {', '.join(allowed_categories)}.")

class CartItemSchema(Schema):
    id = fields.Int(dump_only=True)
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))
    user_id = fields.Int(required=True)
    
    @validates('product_id')
    def validate_product_id(self, value):
        if not Product.query.get(value):
            raise ValidationError("Product not found.")
    
    @validates('user_id')
    def validate_user_id(self, value):
        if not User.query.get(value):
            raise ValidationError("User not found.")

class OrderSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    total = fields.Float(required=True, validate=validate.Range(min=0.01))
    items = fields.List(fields.Nested('OrderItemSchema'), dump_only=True)

    @validates('user_id')
    def validate_user_id(self, value):
        if not User.query.get(value):
            raise ValidationError("User not found.")
    
    @validates('total')
    def validate_total(self, value):
        if value <= 0:
            raise ValidationError("Total must be greater than zero.")

class OrderItemSchema(Schema):
    id = fields.Int(dump_only=True)
    product_id = fields.Int(required=True)
    order_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))
    price = fields.Float(required=True, validate=validate.Range(min=0.01))
    
    @validates('product_id')
    def validate_product_id(self, value):
        if not Product.query.get(value):
            raise ValidationError("Product not found.")
    
    @validates('order_id')
    def validate_order_id(self, value):
        if not Order.query.get(value):
            raise ValidationError("Order not found.")
