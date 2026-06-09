from flask import Blueprint, render_template, request, jsonify, redirect, url_for

lewis_bp = Blueprint("lewis",__name__)
#presenter = LewisPresenter()


@lewis_bp.route("/", methods =["GET"])
def insertar():
    return render_template('Lewis/lewis.html')