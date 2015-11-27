from flask import render_template
from . import site
import locale


locale.setlocale(locale.LC_ALL, 'en_US')


@site.route('/trader_performance')
def trader_performance():

    return render_template('site/index.html')
