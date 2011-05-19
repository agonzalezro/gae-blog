from blog import app
from models import Post
from flask import render_template, flash, redirect, url_for, Markup
from decorators import login_required
from forms import PostForm

@app.route('/posts')
def list_posts():
    posts = Post.all()
    return render_template('list_posts.html', posts=posts)

@app.route('/posts/new', methods = ['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data,
                    content = form.content.data)
        post.put()
        flash('Post saved on database.')
        return redirect(url_for('list_posts'))
    return render_template('new_post.html', form=form)
