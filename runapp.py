import os
from paste.deploy import loadapp
from waitress import serve

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app = loadapp('config:production.ini', relative_to='.')

    serve(app, host='127.0.0.1', port=port)
