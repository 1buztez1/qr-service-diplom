from app import create_app, db
from asgiref.wsgi import WsgiToAsgi
import sys


sys.dont_write_bytecode = True
app = create_app()
asgi_app = WsgiToAsgi(app)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)