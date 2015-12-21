from flask import render_template
from . import blog


@blog.route('/blog')
def blog_home():
    return render_template('blog/index.html')
