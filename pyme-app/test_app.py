from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World! Flask app is running!"

@app.route('/test')
def test():
    return {
        "status": "success",
        "message": "Test endpoint working",
        "port": os.environ.get('PORT', '8000')
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"Starting test app on port {port}")
    app.run(host='0.0.0.0', port=port) 