from flask_restful import Resource
from flask import request
from app.models import Product
from app.schemas import ProductSchema
from app import db

class ProductResource(Resource):
    def get(self, id):
        product = Product.query.get_or_404(id)
        schema = ProductSchema()
        return schema.dump(product), 200

    def put(self, id):
        product = Product.query.get_or_404(id)
        data = request.get_json()
        schema = ProductSchema()
        product = schema.load(data, instance=product, partial=True)
        db.session.commit()
        return schema.dump(product), 200

    def delete(self, id):
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return '', 204

class ProductListResource(Resource):
    def get(self):
        products = Product.query.all()
        schema = ProductSchema(many=True)
        return schema.dump(products), 200

    def post(self):
        data = request.get_json()
        schema = ProductSchema()
        product = schema.load(data)
        db.session.add(product)
        db.session.commit()
        return schema.dump(product), 201
