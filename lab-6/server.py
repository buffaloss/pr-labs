from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Step 1: Setting Up the Environment
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///electro_scooter.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Step 6: Creating a Model for Electro Scooter
class ElectroScooter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    battery_level = db.Column(db.Float, nullable=False)

    def __init__(self, name, battery_level):
        self.name = name
        self.battery_level = battery_level

class ElectroScooterSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "battery_level")

electro_scooter_schema = ElectroScooterSchema()
electro_scooters_schema = ElectroScooterSchema(many=True)

# Step 7: Creating a POST Request
@app.route('/api/electro-scooters', methods=['POST'])
def add_electro_scooter():
    name = request.json['name']
    battery_level = request.json['battery_level']
    new_scooter = ElectroScooter(name, battery_level)
    db.session.add(new_scooter)
    db.session.commit()
    return electro_scooter_schema.jsonify(new_scooter)

# Step 8: Creating a GET Request
@app.route('/api/electro-scooters/<id>', methods=['GET'])
def get_electro_scooter(id):
    scooter = ElectroScooter.query.get(id)
    if scooter:
        return electro_scooter_schema.jsonify(scooter)
    else:
        return jsonify({"error": "Scooter not found"}), 404

# Step 9: Creating a PUT Request
@app.route('/api/electro-scooters/<id>', methods=['PUT'])
def update_electro_scooter(id):
    scooter = ElectroScooter.query.get(id)
    if scooter:
        scooter.name = request.json['name']
        scooter.battery_level = request.json['battery_level']
        db.session.commit()
        return electro_scooter_schema.jsonify(scooter)
    else:
        return jsonify({"error": "Scooter not found"}), 404

# Step 10: Creating a DELETE Request
@app.route('/api/electro-scooters/<id>', methods=['DELETE'])
def delete_electro_scooter(id):
    scooter = ElectroScooter.query.get(id)
    if scooter:
        db.session.delete(scooter)
        db.session.commit()
        return electro_scooter_schema.jsonify(scooter)
    else:
        return jsonify({"error": "Scooter not found"}), 404

# Step 11: run the APP
if __name__ == '__main__':
    app.run(debug=True)