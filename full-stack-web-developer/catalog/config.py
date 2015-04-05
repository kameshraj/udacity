# All configs defined here

import os

# to disable cross site reference hack
WTF_CSRF_ENABLED = True
SECRET_KEY = 'catalog-project-secret-key'

# Github oath2
# (Not implemented Yet as we need a Public accessable site to catch github response)
GITHUB_CLIENT_ID = '1eb5ac65ce3a9a99285d'
GITHUB_CLIENT_SECRET = '75c0546abb4c637ffbec37f3431436d3feb99b78'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]

# for database and migration
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
# limit uploads to 8MB
MAX_CONTENT_LENGTH=8 * 1024 * 1024