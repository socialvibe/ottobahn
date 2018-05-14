import configparser
import os

from flask import Flask, Response, send_file

from app.fragments import FragmentGenerator, ActiveManifest

App = Flask(__name__)

App.config['DEBUG'] = True

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))

active_manifest = ActiveManifest(config)
generator = FragmentGenerator(config)

active_manifest.fill(generator)


@App.route('/m', methods=['GET'])
def get_manifest():
    active_manifest.roll()
    active_manifest.fill(generator)
    return Response(active_manifest.build(), mimetype='application/x-mpegurl')


@App.route('/f/<f_id>', methods=['GET'])
def get_fragment(f_id):
    return send_file(active_manifest.fragment_path(f_id))
