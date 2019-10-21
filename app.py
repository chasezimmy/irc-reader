from flask import Flask
from irc.irc import irc_routes


app = Flask(__name__)
app.register_blueprint(irc_routes)


if __name__ == '__main__':
    app.run(debug=True)
