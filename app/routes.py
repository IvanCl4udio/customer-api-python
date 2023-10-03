from flask import jsonify, request, abort
from app import app, db
from app.models import Customer

@app.route('/customers', methods=['GET'])
def get_all_customers():
    customers = Customer.query.all()
    return jsonify([c.as_dict() for c in customers])

@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return jsonify(customer.as_dict())

@app.route('/customers', methods=['POST'])
def create_customer():
    if not request.json or not 'name' in request.json or not 'email' in request.json:
        abort(400)
    customer = Customer(name=request.json['name'], email=request.json['email'])
    db.session.add(customer)
    db.session.commit()
    return jsonify(customer.as_dict()), 201

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    if 'name' in request.json:
        customer.name = request.json['name']
    if 'email' in request.json:
        customer.email = request.json['email']
    db.session.commit()
    return jsonify(customer.as_dict())

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'result': 'Customer deleted'}), 200
