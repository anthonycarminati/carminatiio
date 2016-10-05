from flask import render_template, flash, redirect, url_for, abort, request, current_app, Markup
from . import blog
from flask_login import login_required, current_user
from .. import db
from ..models import User, Post
from .forms import ProfileForm, PostForm, CommentForm, AdminCommentForm


@blog.route('/')
def blog_home():
    # db.create_engine()  # TODO - need to re-establish connection automatically
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.post_date.desc())\
        .paginate(page, per_page=current_app.config['TALKS_PER_PAGE'], error_out=False)
    post_list = pagination.items
    return render_template('blog/blog.html', posts=post_list, pagination=pagination)


@blog.route('/new', methods=['GET', 'POST'])
@login_required  # TODO - Require login for creating a new blog post
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(author_id=current_user.get_id())
        form.to_model(post)
        db.session.add(post)
        db.session.commit()
        flash('Your post was added successfully!')
        return redirect(url_for('.blog_home'))
    return render_template('blog/new_post.html', form=form)


@blog.route('/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('blog/post.html',
                           post=post)



@blog.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.bio = form.bio.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('blog.blog_home'))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.bio.data = current_user.bio
    return render_template('blog/profile.html', form=form)
