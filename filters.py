import markdown as md
from flask import Markup
from blog import app

@app.template_filter('markdown')
def markdown(s):
    return Markup(md.markdown(s))
