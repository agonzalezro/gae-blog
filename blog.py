from models import *
import defs
import request

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

class FrontPageHandler(request.BlogRequestHandler):
    """
    Handles requests to display the front (or main) page of the blog.
    """
    def get(self):
        articles = Article.published()

        self.response.out.write(self.render_template('blog/main.html',
                                {'articles': articles, 'request': self.request}))


# -----------------------------------------------------------------------------
# Main program
# -----------------------------------------------------------------------------

application = webapp.WSGIApplication(
    [('/', FrontPageHandler),
     ],

    debug=True)

def main():
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

