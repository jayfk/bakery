# -*- coding: utf-8 -*-
# Olá, meu nome é Pedro
from __future__ import print_function
from flask import Flask, request, jsonify, send_file
import os
from envparse import env
import tempfile
import zipfile
from cookiecutter.main import cookiecutter
import json

ROOT = os.path.dirname(os.path.abspath(__file__))

def generate_cookiecutters():
    for item in os.listdir('/cookiecutters'):
        if os.path.isdir(os.path.join('/cookiecutters', item)):
            with open(os.path.join('/cookiecutters', item, "cookiecutter.json"), "r") as f:
                cookiecutter_json = json.loads(f.read())
                yield (item, {
                    "path": os.path.join('/cookiecutters', item),
                    "cookiecutter.json": cookiecutter_json
                })
INSTALLED_COOKIECUTTERS = dict(generate_cookiecutters())

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.get_json(silent=True)

        if not data:
            return jsonify({"error": "feed me json"}), 400

        selected_cookiecutter = data.pop("cookiecutter", False)
        if not selected_cookiecutter:
            return jsonify({"error": "please select a cookiecutter"})

        if selected_cookiecutter not in INSTALLED_COOKIECUTTERS:
            return jsonify({"error": f"{selected_cookiecutter} is not installed."}), 400

        cookiecutter_template = INSTALLED_COOKIECUTTERS.get(selected_cookiecutter)

        exclusives = list(generate_exclusive_items(
            data.keys(),
            cookiecutter_template["cookiecutter.json"].keys()
        ))
        if exclusives:
            error = f"some of your keys are not in cookiecutter.json: {exclusives}"
            return jsonify({"error": error}), 400
        
        output_dir = tempfile.mkdtemp()
        cookiecutter(
                cookiecutter_template.get("path"),
                no_input=True,
                extra_context=data,
                output_dir=output_dir
            )
        zip = make_zip(output_dir)
        return send_file(zip.name), 200

    return jsonify({"cookiecutters": INSTALLED_COOKIECUTTERS}), 200

def generate_exclusive_items(list_a, list_b):
    for item in list_a:
        if item not in list_b:
            yield item

def make_zip(path):
    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
        zip = zipfile.ZipFile(tmp.name, 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(path):
            for file in files:
                relpath = os.path.relpath(os.path.join(root, file), path)
                zip.write(
                    os.path.join(root, file),
                    relpath
                )
        zip.close()
        return tmp

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
