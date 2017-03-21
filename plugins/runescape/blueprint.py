#!/usr/bin/env python
# coding=utf-8
from flask import Blueprint, json, render_template, redirect, url_for
from .player import Player, RSApiError

rs_bp = Blueprint('RuneScape', 'runescape', url_prefix='/rs')


@rs_bp.errorhandler(RSApiError)
def rs_err_handler(e):
    return f'RS API returned {e.status_code}, try refreshing'


@rs_bp.route('/')
def index():
    return redirect(url_for('RuneScape.compare', player1='DJetelina', player2='M Janiczek'))


@rs_bp.route('/compare/<string:player1>/<string:player2>')
def compare(player1, player2):
    return render_template('rs/compare.html', player1=Player(player1), player2=Player(player2))

@rs_bp.route('/api/player/')
@rs_bp.route('/api/player/<string:name>')
def player(name='DJetelina'):
    return json.jsonify(Player(name).__dict__)
