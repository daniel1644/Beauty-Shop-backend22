from flask_restful import Resource
from flask import request, make_response, jsonify, session
from app.models import CartItem
from app.schemas import CartItemSchema
from app import db

class CartResource(Resource):
    def get(self, id):
        cart_item = CartItem.query.get_or_404(id)
        schema = CartItemSchema()
        response = make_response(jsonify(schema.dump(cart_item)), 200)
        return response

    def put(self, id):
        cart_item = CartItem.query.get_or_404(id)
        data = request.get_json()
        schema = CartItemSchema()
        cart_item = schema.load(data, instance=cart_item, partial=True)
        db.session.commit()
        response = make_response(jsonify(schema.dump(cart_item)), 200)
        return response

    def delete(self, id):
        cart_item = CartItem.query.get_or_404(id)
        db.session.delete(cart_item)
        db.session.commit()
        return make_response('', 204)

class CartListResource(Resource):
    def get(self):
        cart_items = CartItem.query.all()
        schema = CartItemSchema(many=True)
        response = make_response(jsonify(schema.dump(cart_items)), 200)
        return response

    def post(self):
        data = request.get_json()
        schema = CartItemSchema()
        cart_item = schema.load(data)
        db.session.add(cart_item)
        db.session.commit()
        response = make_response(jsonify(schema.dump(cart_item)), 201)
        return response
