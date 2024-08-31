from flask_restful import Resource
from flask import request, make_response, jsonify
from app.models import Product
from app.schemas import ProductSchema
from app import db

class ProductResource(Resource):
    def get(self, id):
        product = Product.query.get_or_404(id)
        schema = ProductSchema()
        response = make_response(jsonify(schema.dump(product)), 200)
        return response

    def put(self, id):
        product = Product.query.get_or_404(id)
        data = request.get_json()
        schema = ProductSchema()
        try:
            product = schema.load(data, instance=product, partial=True)
            db.session.commit()
            response = make_response(jsonify(schema.dump(product)), 200)
        except Exception as e:
            db.session.rollback()
            response = make_response(jsonify({"error": str(e)}), 400)
        return response

    def delete(self, id):
        product = Product.query.get_or_404(id)
        try:
            db.session.delete(product)
            db.session.commit()
            response = make_response('', 204)
        except Exception as e:
            db.session.rollback()
            response = make_response(jsonify({"error": str(e)}), 400)
        return response

class ProductListResource(Resource):
    def get(self):
        products = Product.query.all()
        schema = ProductSchema(many=True)
        response = make_response(jsonify(schema.dump(products)), 200)
        return response

    def post(self):
        data = request.get_json()
        schema = ProductSchema()
        try:
            product = schema.load(data)
            db.session.add(product)
            db.session.commit()
            response = make_response(jsonify(schema.dump(product)), 201)
        except Exception as e:
            db.session.rollback()
            response = make_response(jsonify({"error": str(e)}), 400)
        return response
