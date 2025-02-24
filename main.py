from flask import *
from werkzeug.utils import *
import pandas
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


# Submit a champion

@app.route('/champion_submit.html/', methods=['GET', 'POST'])
def champion_submit():

    UPLOAD_FOLDER = 'uploads/photos/champions'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','webp'}
    
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    if request.method == 'POST':

        print(request.form) #request.files
        
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
            #filename = secure_filename(file.filename)
            champion_name = secure_filename(request.form.get("champion_name"))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], champion_name))
            return redirect(url_for('champion_vote.html', name=champion_name))
        
    return render_template('champion_submit.html')




# the champion vote page

@app.route('/champion_vote.html/', methods=['GET', 'POST'])
def champion_vote():

    if request.method == 'POST':

        print(request.form)



    if request.method == 'GET':
        print(request.args)

    


    return render_template('champion_vote.html')


if __name__ == '__main__':
    app.run(debug=True)