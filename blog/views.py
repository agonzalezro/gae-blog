from blog import app
from models import Post
from flask import render_template, flash, redirect, url_for, Markup, request
from decorators import login_required
from forms import PostForm
from google.appengine.ext import db


@app.route('/')
def list_posts():
    posts = Post.all()
    return render_template('list_posts.html', posts=posts)

"""@app.route('/edit', methods = ['GET', 'POST'])
def edit_post():
    return edit_post()"""

@app.route('/edit', methods = ['GET', 'POST'])
@login_required
def edit_post():
    try:
        id = int(request.args.get('id', ''))
        post = Post.get_by_id(id)
    except ValueError:
        id = None
        post = None

    form = PostForm()
    if form.validate_on_submit():
        if post:
            post.title = form.title.data
            post.content = form.content.data
        else:
            post = Post(title = form.title.data,
                        content = form.content.data)
        post.put()
        flash('Post saved on database.')
        return redirect(url_for('list_posts'))
    return render_template('edit_post.html', id=id, form=form, post=post)
