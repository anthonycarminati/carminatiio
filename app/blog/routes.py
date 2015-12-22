from flask import render_template, flash, redirect, url_for, abort, request, current_app
from . import blog
from flask.ext.login import login_required, current_user
from .. import db
from ..models import User, Post, Comment
from .forms import ProfileForm, PostForm, CommentForm, AdminCommentForm


@blog.route('/')
def blog_home():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.post_date.desc()).\
        paginate(page, per_page=current_app.config['TALKS_PER_PAGE'], error_out=False)
    post_list = pagination.items
    return render_template('blog/index.html', posts=post_list, pagination=pagination)


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
        return redirect(url_for('blog.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.bio.data = current_user.bio
    return render_template('blog/profile.html', form=form)


@blog.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(author=current_user)
        form.to_model(post)
        db.session.add(post)
        db.session.commit()
        flash('Your talk was added successfully!')
        return redirect(url_for('.blog_home'))
    return render_template('blog/edit_post.html', form=form)


@blog.route('/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comment = None
    if current_user.is_authenticated():
        form = AdminCommentForm()
        if form.validate_on_submit():
            comment = Comment(body=form.body.data,
                              post=post,
                              author=current_user,
                              notify=False,
                              approved=True)
    else:
        form = CommentForm()
        if form.validate_on_submit():
            comment = Comment(body=form.body.data,
                              post=post,
                              author_name=form.name.data,
                              author_email=form.email.data,
                              notify=form.notify.data,
                              approved=False)
    if comment:
        db.session.add(comment)
        db.session.commit()
        if comment.approved:
            # send_comment_notification(comment)
            flash('Your comment has been published.')
        else:
            # send_author_notification(post)
            flash('Your comment will be published once it has been approved.')
        return redirect(url_for('.post', id=post.post_id) + '#top')
    if post.author == current_user or (current_user.is_authenticated() and current_user.is_admin):
        comments_query = post.comments
    else:
        comments_query = post.approved_comments()
    page = request.args.get('page', 1, type=int)
    pagination = comments_query.order_by(Comment.timestamp.asc()).\
        paginate(page, per_page=current_app.config['COMMENTS_PER_PAGE'], error_out=False)
    comments = pagination.items
    headers = {}
    if current_user.is_authenticated():
        headers['X-XSS-Protection'] = '0'
    return render_template('blog/post.html',
                           post=post,
                           form=form,
                           comments=comments,
                           pagination=pagination), 200, headers


@blog.route('/moderate')
@login_required
def moderate():
    comments = current_user.for_moderation().order_by(Comment.timestamp.asc())
    return render_template('blog/moderate.html', comments=comments)


@blog.route('/blog/moderate-admin')
@login_required
def moderate_admin():
    if not current_user.is_admin:
        abort(403)
    comments = Comment.for_moderation().order_by(Comment.timestamp.asc())
    return render_template('blog/moderate.html', comments=comments)