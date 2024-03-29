#!/usr/bin/env python
import sys
sys.path.append("./lib/")

import webapp2
import os
import jinja2
import cgi
from cookie import authenticate_cookie
from database import get_user
from collections import namedtuple
from database import gravatar, get_user
import calendar



def guess_autoescape(template_name):
    if template_name is None or '.' not in template_name:
        return False
    if template_name == "blog.html" or template_name == "index.html":
        return False
    ext = template_name.rsplit('.', 1)[1]
    return ext in ('html', 'htm', 'xml')

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                         autoescape=guess_autoescape,
                         extensions=['jinja2.ext.autoescape'])
                        
class Handler(webapp2.RequestHandler):
    def login(self):
        cookie = self.request.cookies.get("user_id")
        user = get_user(authenticate_cookie(cookie))
        self.user = user        
        
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        kw['gravatar'] = gravatar
        kw['get_user'] = get_user
        kw['calendar'] = calendar
        self.write(self.render_str(template, **kw))