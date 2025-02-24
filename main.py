from flask import *
from werkzeug.utils import *
import sys
import pandas
import os
import base64


app = Flask(__name__, template_folder='.')

# various utility functions

def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def calculate_elo(elo1, elo2, winner):

    # this is the odds that champion 1 wins
    expected = 1 / (10**((elo2 - elo1) / 400) + 1)

    k_factor = 32 #* (1000 / max(elo1, elo2))
    
    if winner == 1:
        delta = round(k_factor * (1 - expected))
    else:
        delta = round(k_factor * (0 - expected))

    new_elo1 = elo1 + delta
    new_elo2 = elo2 - delta

    return new_elo1, new_elo2




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

        print(request.form)
        
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

            # save the champion image
            sanitized_file_name = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], sanitized_file_name))

            # get the database
            try:
                db = pandas.read_csv('data/champion_data.csv')
            except:
                
                db = pandas.DataFrame(columns=["name", "date_added", "elo", "wins", "losses", "kd", "image"])

            # add the new data
            name = request.form.get("champion_name")
            date_added = datetime.now().strftime("%m/%d/%Y")
            elo = 1000
            wins = 0
            losses = 0
            kd = "NA"
            image_path = 'uploads/photos/champions/' + sanitized_file_name
            db.loc[len(db)] = [name, date_added, elo, wins, losses, kd, image_path]

            # save the new data
            db.to_csv('data/champion_data.csv', index=False)

            # send the user to the voting page
            return redirect(url_for('champion_vote'))
        
    return render_template('champion_submit.html')




# the champion vote page

@app.route('/champion_vote.html/', methods=['GET', 'POST'])
def champion_vote():


    # handle the votes

    if request.method == 'POST':

        print("Voted for " + request.form['winner'] + " over " + request.form['loser'])

        # get the database
        try:
            db = pandas.read_csv('data/champion_data.csv')
        except:
            db = pandas.DataFrame(columns=["name", "date_added", "elo", "wins", "losses", "kd", "image"])

        # update the elo of the champions
        winner = db.loc[db['name'] == request.form['winner']]
        loser = db.loc[db['name'] == request.form['loser']]

        winner_elo = winner.iloc[0]['elo']
        loser_elo = loser.iloc[0]['elo']
        

    # get two random champions from the csv database using pandas

    db = pandas.read_csv('data/champion_data.csv')
    champion_1_data = db.sample(n=1).iloc[0].to_dict()
    champion_2_data = db.sample(n=1).iloc[0].to_dict()

    # make sure the two champions are different
    while champion_1_data['name'] == champion_2_data['name']:
        champion_2_data = db.sample(n=1).iloc[0].to_dict()

    # replace the image src with base64 img data
    for champion in [champion_1_data, champion_2_data]:
        with open(champion['image'], 'rb') as f:
            imagebase64data = base64.b64encode(f.read()).decode('utf-8')
            champion['image'] = 'data:image/png;base64,' + imagebase64data


    # champion_data will look something like {"name": name, "date_added": date_added, "elo": elo, "kd": kd, "image": imagebase64data}

    return render_template('champion_vote.html', champion_1_data=champion_1_data, champion_2_data=champion_2_data)



if __name__ == '__main__':
    app.run(debug=True)
    