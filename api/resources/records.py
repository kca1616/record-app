from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from peewee import DoesNotExist, IntegrityError
from playhouse.shortcuts import model_to_dict

from models.record import Record
from models.favorite import Favorite
from models.user import User

recordBP = Blueprint('records', __name__, url_prefix='/api/records')


@recordBP.route('/', methods=['GET'])
@login_required
def get_all_records():
    try:
        records = [model_to_dict(record) for record in Record.select()]
        return jsonify(records), 200
    except DoesNotExist:
        return jsonify(message="Error getting records."), 500


@recordBP.route('/new', methods=['POST'])
@login_required
def add_record():
    try:
        body = request.get_json()
        record, created = Record.get_or_create(**body)
        return jsonify(model_to_dict(record), created), 201
    except IntegrityError:
        return jsonify(message="Record with this catalog number already exists."), 200

@recordBP.route('/edit/<int:record_id>', methods=['PUT'])
@login_required
def update_record(record_id):
    try:
        body = request.get_json()
        Record.update(**body).where(Record.id == record_id).execute()
        record = Record.get_by_id(record_id)
        return jsonify(model_to_dict(record)), 201
    except DoesNotExist:
        return jsonify(message="Error finding record."), 500


@recordBP.route('/favorites', methods=['GET'])
@login_required
def get_favorites():
    try:
        user = User.get(current_user.id)
        records = [model_to_dict(record) for record in Favorite.select().where(
            Favorite.user == user)]
        return jsonify(records), 200
    except DoesNotExist:
        return jsonify(message="womp womp"), 500


@recordBP.route('/new-favorite/<int:record_id>', methods=['POST'])
@login_required
def add_wishlist(record_id):
    try:
        record = Record.get_by_id(record_id)
        user = User.get_by_id(current_user.id)
        if Favorite.get_or_none(Favorite.user == current_user.id,
            Favorite.record == record.id) != None:
            return jsonify(message="This pressing already exists in wishlist!"), 400
        Favorite.create(user=current_user, record=record)
        user_dict = model_to_dict(user, backrefs=True)
        del user_dict['password']
        return jsonify(message="Favorite created!"), 201
    except DoesNotExist:
        return jsonify(message="Error getting record."), 500


@recordBP.route('/favorites/<int:record_id>', methods=['DELETE'])
@login_required
def delete_wishlist(record_id):
    (Favorite
        .delete()
        .where((Favorite.record == record_id) & (Favorite.user == current_user.id)).execute())
    return jsonify(message="YASSSS"), 204


@recordBP.route('/<int:record_id>', methods=['DELETE'])
@login_required
def delete_record(record_id):
    (Record
        .delete()
        .where(Record.id == record_id).execute())
    return jsonify(message="YASSSS"), 204
