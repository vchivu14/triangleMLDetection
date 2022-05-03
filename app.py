from flask import Flask, send_from_directory, request, redirect, jsonify
# CNN model dependencies
import os
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from keras.preprocessing import image
import numpy as np

UPLOAD_FOLDER = './images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def base():
    return send_from_directory("./svelte-client/public", "index.html")

@app.route("/<path:path>")
def home(path):
    return send_from_directory('./svelte-client/public', path)

@app.route('/test', methods=['post'])
def upload_file():
    print("I'm in")
    print(request.files)
    file = request.files['file']
    print(file)
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        print("we got the file")
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        imageSaved = UPLOAD_FOLDER+"/"+filename

        model = load_model('model.h5')
        targetSize = 28
        color = "grayscale"
        test_image = image.load_img(imageSaved, target_size=[targetSize,targetSize], color_mode=color)
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image,axis=0)
        result = model.predict(test_image/255.0)
        print(result)
        if result[0][2] > 0.55:
            print("it's a triangle")
            return jsonify("We predict it is a triangle with an accuracy of: " + str(result[0][2]))
        else:
            print("not a triangle")
            return jsonify("Most probably it is not a triangle")

if __name__ == "__main__":
    app.run()