from flask import Flask, request, render_template, send_file
from stabilizer import Stabilizer
from werkzeug.utils import secure_filename

app = Flask(__name__)
DOWNLOAD_FILE_PATH = 'data/result.mp4'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files.get('video_file')
    filename = secure_filename(uploaded_file.filename)
    uploaded_file_path = f'data/{filename}'
    uploaded_file.save(uploaded_file_path)

    crop_height = request.form.get('crop_height')
    crop_width = request.form.get('crop_width')

    if crop_height != '':
        crop_height = int(crop_height)
    else:
        crop_height = None

    if crop_width != '':
        crop_width = int(crop_width)
    else:
        crop_width = None

    stabilizer = Stabilizer(input_video_path=uploaded_file_path,
                            crop_height=crop_height,
                            crop_width=crop_width,
                            output_video_path=DOWNLOAD_FILE_PATH)
    stabilizer.execute()

    return send_file(DOWNLOAD_FILE_PATH, as_attachment=True,
                     attachment_filename='result.mp4',
                     mimetype='video/mp4')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)