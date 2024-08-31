from flask_restful import Resource
from flask import request
from app.models import Order, OrderItem
from app.schemas import OrderSchema, OrderItemSchema
from app import db

class OrderResource(Resource):
    def get(self, id):
        order = Order.query.get_or_404(id)
        schema = OrderSchema()
        return schema.dump(order), 200

    def put(self, id):
        order = Order.query.get_or_404(id)
        data = request.get_json()
        schema = OrderSchema()
        order = schema.load(data, instance=order, partial=True)
        db.session.commit()
        return schema.dump(order), 200

    def delete(self, id):
        order = Order.query.get_or_404(id)
        db.session.delete(order)
        db.session.commit()
        return '', 204

class OrderListResource(Resource):
    def get(self):
        orders = Order.query.all()
        schema = OrderSchema(many=True)
        return schema.dump(orders), 200

    def post(self):
        data = request.get_json()
        schema = OrderSchema()
        order = schema.load(data)
        db.session.add(order)
        db.session.commit()
        return schema.dump(order), 201
