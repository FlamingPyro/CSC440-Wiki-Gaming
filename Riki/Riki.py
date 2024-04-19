#!/Users/smcho/virtualenv/riki/bin/python

# -*- coding: utf-8 -*-
import os

from wiki import create_app
from wiki.web.extensions import db

directory = os.getcwd()
app = create_app(directory)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)