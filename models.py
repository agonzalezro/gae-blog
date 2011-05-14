import datetime
import sys

from google.appengine.ext import db

#FETCH_THEM_ALL = ((sys.maxint - 1) >> 32) & 0xffffffff
FETCH_THEM_ALL = sys.maxint

class Article(db.Model):
    title = db.StringProperty(required=True)
    body = db.TextProperty()
    published_when = db.DateTimeProperty(auto_now_add=True)

    draft = db.BooleanProperty(required=True, default=False)

    @classmethod
    def get_all(cls):
        q = db.Query(Article)
        q.order('-published_when')
        return q.fetch(FETCH_THEM_ALL)
    
    @classmethod
    def get(cls, id):
        q = db.Query(Article)
        q.filter('id = ', id)
        return q.get()
    
    @classmethod
    def published_query(cls):
        q = db.Query(Article)
        q.filter('draft = ', False)
        return q
    
    @classmethod
    def published(cls):
        return Article.published_query().order('-published_when').fetch(FETCH_THEM_ALL)


    def save(self):
        try:
            previous_version = Article.get(self.key().id())
        except db.NotSavedError:
            previous_version = None

        try:
            draft = previous_version.draft
        except AttributeError:
            draft = False

        if draft and (not self.draft):
            # Going from draft to published. Update the timestamp.
            self.published_when = datetime.datetime.now()

        self.put()
        """try:
            obj_id = self.key().id()
            resave = False
        except db.NotSavedError:
            # No key, hence no ID yet. This one hasn't been saved.
            # We'll save it once without the ID field; this first
            # save will cause GAE to assign it a key. Then, we can
            # extract the ID, put it in our ID field, and resave
            # the object.
            resave = True

        self.put()
        if resave:
            #self.id = self.key().id()
            self.put()"""
