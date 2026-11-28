import camera
import vision
from flask import Flask, render_template, Response

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', cnt=vision.cnt)

@app.route('/video')
def video():
    return Response(
        camera.generate_frame(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route('/status')
def status():
    left, right, cnt = camera.latest_data
    return f"{left},{right},{cnt}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)
