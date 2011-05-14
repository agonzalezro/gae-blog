import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from models import *
import request

#Exceptions
from google.appengine.ext.db import BadArgumentError

class ShowArticlesHandler(request.BlogRequestHandler):
    def get(self):       
        self.response.out.write(self.render_template('admin/main.html',
                                {'articles': Article.get_all()}))

class NewArticleHandler(request.BlogRequestHandler):
    def get(self):
        self.response.out.write(self.render_template('admin/edit.html',
                                {'article': Article(title='Your title here', body='And your body here!')}))

class SaveArticleHandler(request.BlogRequestHandler):
    def post(self):
        s_id = cgi.escape(self.request.get('id'))
        id = int(s_id) if s_id else None

        title = cgi.escape(self.request.get('title'))
        body = cgi.escape(self.request.get('content'))
        published_when = cgi.escape(self.request.get('published_when'))
        draft = cgi.escape(self.request.get('draft'))

        if not draft:
            draft = False
        else:
            draft = (draft.lower() == 'on')

        try:
            article = Article.get_by_id(id)
            if article:
                article.title = title
                article.body = body
                article.draft = draft
        except BadArgumentError:
            article = Article(title=title, body=body, draft=draft)
        article.save()

        self.redirect('/admin')


class EditArticleHandler(request.BlogRequestHandler):
        def get(self):
            id = int(self.request.get('id'))
            article = Article.get_by_id(id)
            if not article:
                raise ValueError, 'Article with ID %d does not exist.' % id

            self.response.out.write(self.render_template('admin/edit.html',
                                    {'article': article}))


class DeleteArticleHandler(request.BlogRequestHandler):
        def get(self):
            id = int(self.request.get('id'))
            article = Article.get_by_id(id)
            if article:
                article.delete()

            self.redirect('/admin/')


application = webapp.WSGIApplication(
        [('/admin/?', ShowArticlesHandler),
         ('/admin/article/new/?', NewArticleHandler),
         ('/admin/article/delete/?', DeleteArticleHandler),
         ('/admin/article/save/?', SaveArticleHandler),
         ('/admin/article/edit/?', EditArticleHandler),
         ], debug=True)

def main():
    util.run_wsgi_app(application)

if __name__ == "__main__":
    main()
