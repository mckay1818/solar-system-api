from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.planet import Planet
from app.models.moon import Moon
from app.routes.routes_helper import validate_model

moons_bp = Blueprint("moons", __name__, url_prefix="/moons")

@moons_bp.route("", methods=["GET"])
def get_all_moons_name():
    moons_query = Moon.query

    name_query = request.args.get("name")
    if name_query:
        moons_query = moons_query.filter(Moon.name.ilike(f"%{name_query}%"))

    sort_query = request.args.get("sort")
    if sort_query == "asc":
        moons_query = moons_query.order_by(Moon.name.asc())
    if sort_query == "desc":
        moons_query = moons_query.order_by(Moon.name.desc())

    moons = moons_query.all()

    moons_response = []
    for moon in moons:
        moons_response.append(moon.to_dict()["name"])
        
    return jsonify(moons_response)



@moons_bp.route("/<moon_id>", methods=["GET"])
def get_one_moon_by_id(moon_id):
    moon = validate_model(Moon, moon_id)
    return moon.to_dict()["name"]