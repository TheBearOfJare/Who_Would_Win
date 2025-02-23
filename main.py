from flask import *
from werkzeug.utils import *
import sqlite3
import os


app = Flask(__name__, template_folder='.')

# various utility functions

def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS







# The Home page

@app.route('/', methods=['GET', 'POST'])
def index():
        
    return render_template('index.html')


# Submit a selfie

@app.route('/selfie_submit.html/', methods=['GET', 'POST'])
def selfie_submit():

    UPLOAD_FOLDER = 'uploads/photos/selfies'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','webp'}
    
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    if request.method == 'POST':

        print(request.files) #request.files
        for i in request.files:
            print(i)
            #i.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        
        # check if the post request has the file part
        if 'file' not in request.files:
            print("ERROR: NO FILE PART")
            print(request)
            print(request.files)
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('selfie_vote.html', name=filename))
        
    return render_template('selfie_submit.html')


if __name__ == '__main__':
    app.run(debug=True)