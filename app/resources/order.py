from flask_restful import Resource
from flask import request, make_response, jsonify, session
from app.models import Order, OrderItem
from app.schemas import OrderSchema, OrderItemSchema
from app import db

class OrderResource(Resource):
    def get(self, id):
        order = Order.query.get_or_404(id)
        schema = OrderSchema()
        response = make_response(jsonify(schema.dump(order)), 200)
        return response

    def put(self, id):
        order = Order.query.get_or_404(id)
        data = request.get_json()
        schema = OrderSchema()
        try:
            order = schema.load(data, instance=order, partial=True)
            db.session.commit()
            response = make_response(jsonify(schema.dump(order)), 200)
        except Exception as e:
            db.session.rollback()
            response = make_response(jsonify({"error": str(e)}), 400)
        return response

    def delete(self, id):
        order = Order.query.get_or_404(id)
        try:
            db.session.delete(order)
            db.session.commit()
            response = make_response('', 204)
        except Exception as e:
            db.session.rollback()
            response = make_response(jsonify({"error": str(e)}), 400)
        return response

class OrderListResource(Resource):
    def get(self):
        orders = Order.query.all()
        schema = OrderSchema(many=True)
        response = make_response(jsonify(schema.dump(orders)), 200)
        return response

    def post(self):
        data = request.get_json()
        schema = OrderSchema()
        try:
            order = schema.load(data)
            db.session.add(order)
            db.session.commit()
            response = make_response(jsonify(schema.dump(order)), 201)
        except Exception as e:
            db.session.rollback()
            response = make_response(jsonify({"error": str(e)}), 400)
        return response
