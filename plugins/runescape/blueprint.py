#!/usr/bin/env python
# coding=utf-8
from flask import Blueprint, json, render_template
from .player import Player, RSApiError

rs_bp = Blueprint('RuneScape', 'runescape', url_prefix='/rs')


@rs_bp.errorhandler(RSApiError)
def rs_err_handler(e):
    return f'RS API returned {e.status_code}, try refreshing'


@rs_bp.route('/')
def index():
    return render_template('rs/compare.html', player1=Player(), player2=Player('M Janiczek'))


@rs_bp.route('/api/player/')
@rs_bp.route('/api/player/<string:name>')
def player(name='DJetelina'):
    return json.jsonify(Player(name).__dict__)
