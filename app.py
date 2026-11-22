import camera
from flask import Flask, render_template, Response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/video")
def video():
    # 실시간 영상 HTTP 응답
    return Response(
        camera.generate_frame(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)
