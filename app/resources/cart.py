from flask_restful import Resource
from flask import request
from app.models import CartItem
from app.schemas import CartItemSchema
from app import db

class CartResource(Resource):
    def get(self, id):
        cart_item = CartItem.query.get_or_404(id)
        schema = CartItemSchema()
        return schema.dump(cart_item), 200

    def put(self, id):
        cart_item = CartItem.query.get_or_404(id)
        data = request.get_json()
        schema = CartItemSchema()
        cart_item = schema.load(data, instance=cart_item, partial=True)
        db.session.commit()
        return schema.dump(cart_item), 200

    def delete(self, id):
        cart_item = CartItem.query.get_or_404(id)
        db.session.delete(cart_item)
        db.session.commit()
        return '', 204

class CartListResource(Resource):
    def get(self):
        cart_items = CartItem.query.all()
        schema = CartItemSchema(many=True)
        return schema.dump(cart_items), 200

    def post(self):
        data = request.get_json()
        schema = CartItemSchema()
        cart_item = schema.load(data)
        db.session.add(cart_item)
        db.session.commit()
        return schema.dump(cart_item), 201
