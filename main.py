from flask import *
from werkzeug.utils import *
import sys
import pandas
import os
import base64
import warnings
# from waitress import *
from markupsafe import Markup
# import google.genai as genai
# import google.genai.types as types
import html
import asyncio
from image_fixer import image_fixer
from dupe_remover import remove_duplicates
import threading


# with open('var.txt', 'r') as f:
#     key = f.read()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



# client = genai.Client(api_key=key)


warnings.filterwarnings("ignore")


app = Flask(__name__, template_folder='.')

# various utility functions

def run_image_fixer():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(image_fixer())

def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def calculate_elo(elo1, elo2, winner):

    # this is the odds that champion 1 wins
    expected = 1 / (10**((elo2 - elo1) / 300) + 1)

    k_factor = 32 #* (1000 / max(elo1, elo2))
    
    if winner == 1:
        delta = round(k_factor * (1 - expected))
    else:
        delta = round(k_factor * (0 - expected))

    new_elo1 = elo1 + delta
    new_elo2 = elo2 - delta

    return new_elo1, new_elo2




# The Default page

@app.route('/', methods=['GET', 'POST'])
def index():
        
    return redirect(url_for('champion_vote'))

# the about page
@app.route('/about.html')
def about():
    return render_template('static/html/about.html')


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

            # before all else, check if the champion already exists with gemini

            # get the database
            try:
                db = pandas.read_csv('data/champion_data.csv')
            except:
                
                db = pandas.DataFrame(columns=["name", "date_added", "elo", "wins", "losses", "kd", "image"])

            """
            # response = client.models.generate_content(
            #     model="gemini-2.0-flash",
            #     contents="Is " + request.form.get("champion_name").replace(",", "") + " similar enough to one of the following: " + ", ".join(db['name'].tolist()) + " that there would be no need to have both? Yes or No",
            #     config=types.GenerateContentConfig(
            #         max_output_tokens=60)
                
            # )

            # text = response.candidates[0].content.parts[0].text

            # if "yes" in text.lower():
            #     print("Rejected: " + request.form.get("champion_name").replace(",", ""))
            #     return redirect(url_for('champion_submission_invalid'))

            # if (db['name'] == request.form.get("champion_name").replace(",", "")).any().any():
                # print("Rejected: " + request.form.get("champion_name").replace(",", ""))
                # return redirect(url_for('champion_submission_invalid'))

                """

            # save the champion image
            sanitized_file_name = secure_filename(file.filename).replace("&#x27;", "'")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], sanitized_file_name))

           
            # add the new data
            name = html.escape(request.form.get("champion_name").replace(",", ""))
            date_added = datetime.now().strftime("%m/%d/%Y")
            elo = 1000
            wins = 0
            losses = 0
            kd = "NA"
            image_path = 'uploads/photos/champions/' + sanitized_file_name
            db.loc[len(db)] = [name, date_added, elo, wins, losses, kd, image_path]

            # save the new data
            db.to_csv('data/champion_data.csv', index=False)

            print(bcolors.OKBLUE + "New champion: " + name + bcolors.ENDC)

            # run image fixer in the background
            run_image_fixer()
            remove_duplicates()
            # send the user to the voting page
            return redirect(url_for('champion_vote'))
        
    return render_template('static/html/champion_submit.html')


# the invalid submission page

@app.route('/champion_submission_invalid.html/')
def champion_submission_invalid():
    return render_template('/static/html/champion_submission_invalid.html')


# the champion vote page

@app.route('/champion_vote.html/', methods=['GET', 'POST'])
def champion_vote():

    #remove_duplicates()

    if request.method == 'POST':
        return handle_vote()
    else:
            

        # get two random champions from the csv database using pandas

        db = pandas.read_csv('data/champion_data.csv')
        champion_1_data = db.sample(n=1).iloc[0].to_dict()
        champion_2_data = db.sample(n=1).iloc[0].to_dict()

        # make sure the two champions are different
        while champion_1_data['name'] == champion_2_data['name']:
            champion_2_data = db.sample(n=1).iloc[0].to_dict()

        
        # replace the image src with base64 img data
        for champion in [champion_1_data, champion_2_data]:
            
            try:
                with open(champion['image'], 'rb') as f:
                    imagebase64data = base64.b64encode(f.read()).decode('utf-8')
                    champion['image'] = 'data:image/png;base64,' + imagebase64data
            except Exception as e:
                print(bcolors.FAIL + "Image not found or some other exception thrown with " + champion['image'] + ": " + str(e) + bcolors.ENDC)
                
                return redirect(url_for('champion_vote'))


        # champion_data will look something like {"name": name, "date_added": date_added, "elo": elo, "kd": kd, "image": imagebase64data}

        return render_template('static/html/champion_vote.html', champion_1_data=champion_1_data, champion_2_data=champion_2_data)

def handle_vote():

    # handle the votes

    print(bcolors.OKGREEN + "Voted for " + request.form['winner'] + " over " + request.form['loser'] + bcolors.ENDC)

    # get the database
    try:
        db = pandas.read_csv('data/champion_data.csv')
    except:
        db = pandas.DataFrame(columns=["name", "date_added", "elo", "wins", "losses", "kd", "image"])

    # Update the stats of the champions
    winner = db.loc[db['name'] == request.form['winner']]
    loser = db.loc[db['name'] == request.form['loser']]
    
    # Update the elo
    winner_elo = winner.iloc[0]['elo']
    loser_elo = loser.iloc[0]['elo']
    
    winner_elo, loser_elo = calculate_elo(winner_elo, loser_elo, 1)

    print(bcolors.OKCYAN + "New Elo: " + str(winner_elo) + " vs " + str(loser_elo) + bcolors.ENDC)
    
    # Update the winner and loser DataFrames
    winner_index = winner.index[0]
    loser_index = loser.index[0]
    
    db.at[winner_index, 'elo'] = winner_elo
    db.at[winner_index, 'wins'] += 1
    db.at[winner_index, 'kd'] = round(db.at[winner_index, 'wins'] / db.at[winner_index, 'losses'], 2)
    
    db.at[loser_index, 'elo'] = loser_elo
    db.at[loser_index, 'losses'] += 1
    db.at[loser_index, 'kd'] = round(db.at[loser_index, 'wins'] / db.at[loser_index, 'losses'], 2)
    


    # Save the changes to the CSV file
    db.to_csv('data/champion_data.csv', index=False)

    print(bcolors.OKCYAN + "Data saved" + bcolors.ENDC)

    
    # refresh the page to allow the user to vote on a new matchup
    return redirect(url_for('champion_vote'), code=302)


# the image getter
@app.route('/get_image', methods=['GET'])
def get_image():
    # handle the requests for the image data after the table loads. The request is the src of the desired image, and the response is the image data as base64
    if request.method == 'GET':

        src = request.args.get('src')

        # print("Requested received: " + f"{request.args}")
        # print(request)
        # print(src)

        with open(src, 'rb') as f:

            # in the unlikely event of the image being temporarily unavailible, this should avoid throwing a file not found error by looping until the image is found
            while True:
                try:
                    imagebase64data = base64.b64encode(f.read()).decode('utf-8')
                    break
                except:
                    pass

        return imagebase64data
        # return the image data for the requested image

@app.route('/champion_leaderboard.html')
def champion_leaderboard():

    remove_duplicates()

    # get every champion
    db = pandas.read_csv('data/champion_data.csv')

    # sort the dataframe by elo
    db = db.sort_values(by=['elo'], ascending=False)

    # replace the image src an img element. Don't inlcude image data yet, we'll add that after the page loads to improve performance. We'll set the id to the image path, so we can use it later.
    for index, row in db.iterrows():
        src = row['image']
        db.at[index, 'image'] = '<img class="champion_img" id="' + src + '" src="">'

    # champion_data will look something like {"name": name, "date_added": date_added, "elo": elo, "kd": kd, "image": (missing image data)}

    # pass the dataframe to the html page as a table
    leaderboard = db.to_html(index=False, escape=False)

    #print(leaderboard)

    return render_template('static/html/champion_leaderboard.html', leaderboard=Markup(leaderboard))


if __name__ == '__main__':
    app.run(debug=True)

    #serve(app, host='0.0.0.0', port=80)

    