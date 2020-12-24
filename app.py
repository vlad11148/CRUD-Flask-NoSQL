import os

from flask import Flask, render_template
from views.users import user_blueprint
from views.assets import asset_blueprint


app = Flask(__name__)
app.secret_key = 'vlad'
app.config.update(
    ADMIN=os.environ.get('ADMIN')
)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(asset_blueprint, url_prefix="/assets")


if __name__ == "__main__":
    app.run(debug=True)
