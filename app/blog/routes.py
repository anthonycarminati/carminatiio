from flask import render_template
from . import blog
# import locale

# locale.setlocale(locale.LC_ALL, 'en_US')


@blog.route('/')
def index():
    return render_template('blog/index.html')
