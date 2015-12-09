from flask import render_template
from . import site
import locale

# locale.setlocale(locale.LC_ALL, 'en_US')


@site.route('/')
def index():
    return render_template('site/index.html')
