#!/usr/bin/python3
"""
Module for Places review
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review

@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def  get_all_reviews(place_id):
    """  Method retrieve list of all Reviews"""
    place = storage.get('Place', place_id)
    if place:
        reviews = place.reviews
        return jsonify([review.to_dict() for review in reviews])
    else:
        return abort(404)
