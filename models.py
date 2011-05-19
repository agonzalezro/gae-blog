from google.appengine.ext import db

class Post(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    content_html = db.TextProperty(required = True)

    when = db.DateTimeProperty(auto_now_add = True)
    draft = db.BooleanProperty(required=True, default=False)
