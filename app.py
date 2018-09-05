from flask import Flask

from routes.post import main as post_routes

'''
1. pages, templates
    1.1 index.html showing all posts
    1.3 comment
2. data models
    # - Users
    - Posts
    - Comments
3. logic, redirects
    - if not logged, redirect to login page
    - only edit to owner
4. beautify
'''

app = Flask(__name__)
app.secret_key = 'testhard'

app.register_blueprint(post_routes, url_prefix='/post')

if __name__ == '__main__':
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=2000,
    )
    app.run(**config)
