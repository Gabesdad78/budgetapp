from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({"message": "Hello from Vercel!", "status": "success"})

@app.route('/test')
def test():
    return jsonify({"message": "Test route working!", "status": "success"})

if __name__ == '__main__':
    app.run() 