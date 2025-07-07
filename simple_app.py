from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Render! Flask app is working!"

@app.route('/ping')
def ping():
    return "pong"

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8000))
    print(f"Starting simple app on port {port}")
    app.run(host='0.0.0.0', port=port) 