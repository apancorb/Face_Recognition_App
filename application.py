from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from face import face_rec

import os, shutil
import urllib.request

app = Flask(__name__)
app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# Function that checks if the file is allowed
def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function that clears the contents of a given directory
def clear_dir(folder): 
        for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                                os.unlink(file_path)
                        elif os.path.isdir(file_path):
                                shutil.rmtree(file_path)
                except Exception as e:
                        print('Failed to delete %s. Reason: %s' % (file_path, e))
        
@app.route('/')
def upload_form():
        return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
        # check for file
        if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)

        if request.method == "POST":

                # clear the contents of the directories we are going to use
                clear_dir('static/known_faces/user')
                clear_dir('static/unknown_faces')
                clear_dir('static/uploads')
                if len('static/known_faces/user') != 0 or len('static/unknown_faces') != 0 or len('static/uploads') != 0:
                        flash("An error occured in the system. Error: Dirs not empty.")

                files = request.files.getlist("file")

                # process each file we are given 
                for file in files:
                        if file.filename == '':
                                flash('No image selected for uploading')
                                return redirect(request.url)

                        if file and allowed_file(file.filename):
                                filename = secure_filename(file.filename)
                                if "test" in file.filename:
                                        file.save(os.path.join('static/unknown_faces', filename))
                                else:
                                        file.save(os.path.join('static/known_faces/user', filename)) 
                                flash('Image successfully uploaded and displayed')          
                        else:
                                flash('Allowed image types are -> png, jpg, jpeg, gif')
                                return redirect(request.url)

                # check if we have a test image
                if len('static/unknown_faces') == 0:
                        flash("You didn't provide a test image or you didn't name your test image as <test>.")
                        return redirect(request.url)

                # call the face recognition function 
                face_rec_image = face_rec()
                if face_rec_image == False:
                        flash("The Web App wasn't able to recognize no face for the given user you provided :(")
                        return redirect(request.url)
                else:
                        # if we were able to recognize a face display it
                        return redirect(url_for('static', filename= 'uploads/result.jpg'), code=301)

        return redirect(request.url)

if __name__ == "__main__":
    app.run()
