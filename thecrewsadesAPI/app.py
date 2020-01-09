from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Shirt(db.Model):
  __tablename__ = "shirts"
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  done = db.Column(db.Boolean)

  def __init__(self, title, done):
    self.title = title
    self.done = done

class ShirtSchema(ma.Schema):
  class Meta:
    fields = ("id", "title", "done")

shirt_schema = ShirtSchema()
shirts_schema = ShirtSchema(many=True)

# CRUD
# GET
@app.route("/shirts", methods=["GET"])
def get_shirts():
  all_shirts = Shirt.query.all()
  result = shirts_schema.dump(all_shirts)

  return jsonify(result)

# POST
@app.route("/shirt", methods=["POST"])
def add_shirt():
  title = request.json["title"]
  done = request.json["done"]

  new_shirt = Shirt(title, done)

  db.session.add(new_shirt)
  db.session.commit()

  shirt = Shirt.query.get(new_shirt.id)
  return shirt_schema.jsonify(shirt)


# PUT/PATCH by ID
@app.route("/shirt/<id>", methods=["PATCH"])
def update_shirt(id):
  shirt = Shirt.query.get(id)

  new_done = request.json["done"]

  shirt.done = new_done

  db.session.commit()
  return todo_schema.jsonify(todo)

# DELETE
@app.route("/shirt/<id>", methods=["DELETE"])
def delete_shirt(id):
  shirt = Shirt.query.get(id)
  db.session.delete(shirt)
  db.session.commit()

  return jsonify("Got rid of that ish!")

if __name__ == "__main__":
  app.debug = True
  app.run()