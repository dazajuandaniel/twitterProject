from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
#db = SQLAlchemy(app)

from web_app import views, models