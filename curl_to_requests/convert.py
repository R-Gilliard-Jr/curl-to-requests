import functools
import re

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('convert', __name__)

@bp.route('/', methods=("GET", "POST"))
def index():
    if request.method == "POST":
        curl_request = request.form['curl_request']
        error = None
        
        if not curl_request:
            error = 'Please enter a curl request'
        
        if error is not None:
            flash(error)
        else:
            print(curl_request)


    return render_template('index.html')