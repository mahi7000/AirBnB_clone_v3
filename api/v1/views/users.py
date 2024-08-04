#!/usr/bin/python3
"""
Module View Cities
"""
from api.v1.views import app_views
from flask import Flask, abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def get_all_users():
    """List of all users
    """
    all_user = storage.all('User').values()
    if all_user:
        return jsonify([user.to_dict() for user in all_user])


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
    """gets a particular user"""
    user = storage.get('User', user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        return abort(404)
