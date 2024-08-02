#!/usr/bin/python3
"""
index page
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", strict_slashes=False)
def get_status():
    """ Return status OK in json format for the Route"""
    return jsonify(status='OK')


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Retrieves number of object Type
    """
    stats = {'amenities': storage.count('Amenity'),
             'cities': storage.count('City'),
             'places': storage.count('Places'),
             'reviews': storage.count('Review'),
             'states': storage.count('State'),
             'users': storage.couunt('User')
             }
    return jsonify(stats)
