#!/usr/bin/env python
# coding=utf-8
from flask import Blueprint, json
from .player import Player

rs_bp = Blueprint('RuneScape', 'runescape', url_prefix='/rs/')

@rs_bp.route('/')
def index():
    return 'coming soon-ish'


@rs_bp.route('/api/player/<string:name>')
def player(name='DJetelina'):
    return json.jsonify(Player(name).__dict__)
