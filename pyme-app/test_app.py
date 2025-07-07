from flask import Flask
import os
import sys

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World! Flask app is running!"

@app.route('/test')
def test():
    return {
        "status": "success",
        "message": "Test endpoint working",
        "port": os.environ.get('PORT', '8000'),
        "python_version": sys.version,
        "working_directory": os.getcwd(),
        "files": os.listdir('.')
    }

@app.route('/health')
def health():
    return {"status": "healthy"}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"Starting test app on port {port}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Files: {os.listdir('.')}")
    app.run(host='0.0.0.0', port=port) 