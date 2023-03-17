import flask
from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from http import HTTPStatus
from schemas import *
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import *
from hashids import Hashids
import requests

bp = Blueprint('url', __name__, url_prefix='/minrl', description="all operations related to api")

hash = Hashids("Qwerty Salt 15504778953948945358657168914613", 6)


@bp.route('/get_mini_url')
class Url(MethodView):

    @bp.response(HTTPStatus.ACCEPTED, UrlSchema(many=True))
    def get(self):
        urls = UrlModel.query.all()
        return urls

    @bp.arguments(UrlSchema)
    @bp.response(HTTPStatus.ACCEPTED)
    def post(self, url_data):
        url = UrlModel(**url_data)
        if not url:
            abort(HTTPStatus.BAD_REQUEST, 'url is required')

        db_url = UrlModel.query.filter(UrlModel.original_url == url.original_url).first()
        if not db_url:
            try:
                db.session.add(url)
                db.session.commit()
            except SQLAlchemyError as e:
                abort(HTTPStatus.BAD_REQUEST, e)

            db_url = UrlModel.query.filter(UrlModel.original_url == url.original_url).first()
        url_id = db_url.id
        hash_id = hash.encode(url_id)

        short_url = request.host_url + 'minrl/' + hash_id
        response = jsonify({"url": short_url})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
        return response


@bp.route("/<string:hash_id>")
class Redirect(MethodView):

    @bp.response(HTTPStatus.CREATED)
    def get(self, hash_id):
        id = hash.decode(hash_id)[0]
        data = UrlModel.query.get_or_404(id)
        return flask.redirect(data.original_url)
        # return data.original_url
#
