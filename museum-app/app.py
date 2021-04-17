from flask import Flask, render_template, send_file, make_response, request
import predict
import os
from database import Database
import rekognition
import random
import pandas as pd
import base64
import operator

app = Flask(__name__)

@app.route('/')
def hello():
    database = Database()
    database.connect()
    data = database.getArtAll()
    keys = ['objectid', 'objectnumber', 'title', 'artworkdescription', 'culture',
       'city', 'country', 'timeperiod', 'artworkdate', 'datebegin', 'dateend',
       'department', 'accessionyear', 'accessiondate', 'accessionnumber',
       'medium', 'classification', 'dimensions', 'repository', 'tags',
       'imageurl', 'inscription', 'markings', 'artistdisplayname', 'artistid',
       'artistnationality', 'artistprefix', 'artistsuffix', 'nationality',
       'artistbegindate', 'artistenddate', 'artistgender', 'artistrole',
       'artistbio', 'artistulanurl', 'artistwikidataurl', 'objectwikidataurl',
       'tagsaaturl', 'creditline', 'tagswikidataurl', 'artworkurl',
       'rightsandreproduction', 'gallery', 'artistbirthplace',
       'artistdeathplace', 'continent', 'longitude', 'latitude', 's3url']
    form = {}
    for k in keys:
        form[k] = ""
    return render_template('template.html', data = data[1], page = "query", keys = keys, input = form)

@app.route('/index')
def index():
    database = Database()
    database.connect()
    data = database.getArtAll()
    keys = ['objectid', 'objectnumber', 'title', 'artworkdescription', 'culture',
       'city', 'country', 'timeperiod', 'artworkdate', 'datebegin', 'dateend',
       'department', 'accessionyear', 'accessiondate', 'accessionnumber',
       'medium', 'classification', 'dimensions', 'repository', 'tags',
       'imageurl', 'inscription', 'markings', 'artistdisplayname', 'artistid',
       'artistnationality', 'artistprefix', 'artistsuffix', 'nationality',
       'artistbegindate', 'artistenddate', 'artistgender', 'artistrole',
       'artistbio', 'artistulanurl', 'artistwikidataurl', 'objectwikidataurl',
       'tagsaaturl', 'creditline', 'tagswikidataurl', 'artworkurl',
       'rightsandreproduction', 'gallery', 'artistbirthplace',
       'artistdeathplace', 'continent', 'longitude', 'latitude', 's3url']
    form = {}
    for k in keys:
        form[k] = ""
    return render_template('template.html', data = data[1], page = "query", keys = keys, input = form)

@app.route('/infobox')
def infobox():
    objectid = request.args.get("objectid")
    repository = request.args.get("repository")
    if repository == "moma":
        repository = "The Museum of Modern Art"
    elif repository == "mia_":
        repository = "Minneapolis Institute of Art"
    elif repository == "cmoa":
        repository = "Carnegie Museum of Art"
    elif repository == "puam":
        repository = "Princeton University Art Museum"
    elif repository == "met_":
        repository = "Metropolitan Museum of Art, New York, NY"
    database = Database()
    database.connect()
    data = database.getSpecificArt(objectid, repository)[1]
    keys = ['objectid', 'objectnumber', 'title', 'artworkdescription', 'culture',
       'city', 'country', 'timeperiod', 'artworkdate', 'datebegin', 'dateend',
       'department', 'accessionyear', 'accessiondate', 'accessionnumber',
       'medium', 'classification', 'dimensions', 'repository', 'tags',
       'imageurl', 'inscription', 'markings', 'artistdisplayname', 'artistid',
       'artistnationality', 'artistprefix', 'artistsuffix', 'nationality',
       'artistbegindate', 'artistenddate', 'artistgender', 'artistrole',
       'artistbio', 'artistulanurl', 'artistwikidataurl', 'objectwikidataurl',
       'tagsaaturl', 'creditline', 'tagswikidataurl', 'artworkurl',
       'rightsandreproduction', 'gallery', 'artistbirthplace',
       'artistdeathplace', 'continent', 'longitude', 'latitude', 's3url']
    tags, conf = rekognition.detect_labels(data[0][20])
    return render_template('infobox.html', data = data, keys = keys, tags = tags, conf = conf)


@app.route('/query', methods=['GET'])
def query():
    database = Database()
    database.connect()
    data = database.getArtAll()
    keys = ['objectid', 'objectnumber', 'title', 'artworkdescription', 'culture',
       'city', 'country', 'timeperiod', 'artworkdate', 'datebegin', 'dateend',
       'department', 'accessionyear', 'accessiondate', 'accessionnumber',
       'medium', 'classification', 'dimensions', 'repository', 'tags',
       'imageurl', 'inscription', 'markings', 'artistdisplayname', 'artistid',
       'artistnationality', 'artistprefix', 'artistsuffix', 'nationality',
       'artistbegindate', 'artistenddate', 'artistgender', 'artistrole',
       'artistbio', 'artistulanurl', 'artistwikidataurl', 'objectwikidataurl',
       'tagsaaturl', 'creditline', 'tagswikidataurl', 'artworkurl',
       'rightsandreproduction', 'gallery', 'artistbirthplace',
       'artistdeathplace', 'continent', 'longitude', 'latitude', 's3url']
    form = {}
    for k in keys:
        form[k] = ""
    return render_template('template.html', data = data[1], page = "query", keys = keys, input = form)

@app.route('/visualize', methods=['GET'])
def visualize():
    return render_template('template.html', page = "visualize")

@app.route('/visualize_data', methods=['GET'])
def visualize_data():
    database = Database()
    database.connect()
    culture_data, year_data, artist_data, classification_data =  database.getArtAllPlots()
    culture = []
    culture_counts = []
    if culture_data[0]:
        culture, culture_counts= clean_cultures([x[0] for x in culture_data[1]], [x[1] for x in culture_data[1]])
    year = []
    year_counts = []
    if year_data[0]:
        year = [str(x[0])[:-2] for x in year_data[1]][::-1]
        year_counts = [x[1] for x in year_data[1]][::-1]
    if artist_data[0]:
        artist, artist_counts= clean_artists([x[0] for x in artist_data[1]], [x[1] for x in artist_data[1]])
    classification = []
    classification_counts = []
    if classification_data[0]:
        classification = [x[0] for x in classification_data[1]]
        classification_counts = [x[1] for x in classification_data[1]]

    keys = ['objectid', 'objectnumber', 'title', 'artworkdescription', 'culture',
       'city', 'country', 'timeperiod', 'artworkdate', 'datebegin', 'dateend',
       'department', 'accessionyear', 'accessiondate', 'accessionnumber',
       'medium', 'classification', 'dimensions', 'repository', 'tags',
       'imageurl', 'inscription', 'markings', 'artistdisplayname', 'artistid',
       'artistnationality', 'artistprefix', 'artistsuffix', 'nationality',
       'artistbegindate', 'artistenddate', 'artistgender', 'artistrole',
       'artistbio', 'artistulanurl', 'artistwikidataurl', 'objectwikidataurl',
       'tagsaaturl', 'creditline', 'tagswikidataurl', 'artworkurl',
       'rightsandreproduction', 'gallery', 'artistbirthplace',
       'artistdeathplace', 'continent', 'longitude', 'latitude', 's3url']
    form = {}
    for k in keys:
        form[k] = ""
    return render_template('template.html', page = "visualize_data", culture_labels=culture[:min(10, len(culture))], culture_values=culture_counts[:min(10, len(culture))], year_labels=year, year_values= year_counts, artist_labels=artist[:min(10, len(artist))], artist_values = artist_counts[:min(10, len(artist))], classification_labels = classification, classification_values = classification_counts, input = form)

@app.route('/visualize_data', methods=['POST'])
def visualize_data_post():
    database = Database()
    database.connect()
    culture_data, year_data, artist_data, classification_data =  database.getArtPlots(dict(request.form))
    culture, culture_counts = clean_cultures([x[0] for x in culture_data[1]], [x[1] for x in culture_data[1]])
    culture = []
    culture_counts = []
    if culture_data[0]:
        culture, culture_counts= clean_cultures([x[0] for x in culture_data[1]], [x[1] for x in culture_data[1]])
    year = []
    year_counts = []
    if year_data[0]:
        year = [str(x[0])[:-2] for x in year_data[1]][::-1]
        year_counts = [x[1] for x in year_data[1]][::-1]
    artist = []
    artist_counts = []
    if artist_data[0]:
        artist, artist_counts= clean_artists([x[0] for x in artist_data[1]], [x[1] for x in artist_data[1]])
    classification = []
    classification_counts = []
    if classification_data[0]:
        classification = [x[0] for x in classification_data[1]]
        classification_counts = [x[1] for x in classification_data[1]]
    return render_template('template.html', page = "visualize_data", culture_labels=culture[:min(10, len(culture))], culture_values=culture_counts[:min(10, len(culture))], year_labels=year, year_values= year_counts, artist_labels=artist[:min(10, len(artist))], artist_values = artist_counts[:min(10, len(artist))], classification_labels = classification, classification_values = classification_counts, input = dict(request.form))

def clean_artists(artists, artist_counts):
    counts = {}
    for i in range(len(artists)):
        if artists[i].lower() in counts.keys():
            counts[artists[i].lower()] = counts[artists[i].lower()] + artist_counts[i]

        else:
            counts[artists[i].lower()] = artist_counts[i]

    counts = dict( sorted(counts.items(), key=operator.itemgetter(1),reverse=True))
    return [k for k in counts.keys()], [v for v in counts.values()]

def clean_cultures(cultures, culture_counts):
    country_info = pd.read_csv("country_code_merged.csv")
    non_asian_nationality = country_info.loc[country_info.region != "Asia"].nationality.tolist()
    others = ["British", "Greek", "Roman", "European", "African", "Native American", "Attic", "Flemish", "Dutch", "Etruscan", "Italic"]
    non_asian_nationality.extend(others)
    non_asian_country = country_info.loc[country_info.region != "Asia"].name.tolist()
    country_nat = dict(country_info[["name", "nationality"]].values)
    
    counts = {}
    for i in range(len(cultures)):
        cultures[i] = cultures[i].split("|")[0].strip()
        cultures[i] = cultures[i].split("(")[0].strip()
        if cultures[i].strip() not in non_asian_nationality and cultures[i].strip() not in non_asian_country:
          if cultures[i] in country_nat.keys():
              cultures[i] = country_nat[cultures[i]].strip()
          if cultures[i] in counts.keys():
              counts[cultures[i]] = counts[cultures[i]] + culture_counts[i]
          else:
              counts[cultures[i]] = culture_counts[i]
    counts = dict( sorted(counts.items(), key=operator.itemgetter(1),reverse=True))
    return [k for k in counts.keys()], [v for v in counts.values()]

@app.route('/about', methods=['GET'])
def about():
    return render_template('template.html', page = "about")

@app.route('/dataset', methods=['GET'])
def dataset():
    return render_template('template.html', page = "dataset")

@app.route('/query', methods=['POST'])
def search_results():
    database = Database()
    database.connect()
    data =  database.getArt(dict(request.form))
    keys = ['objectid', 'objectnumber', 'title', 'artworkdescription', 'culture',
       'city', 'country', 'timeperiod', 'artworkdate', 'datebegin', 'dateend',
       'department', 'accessionyear', 'accessiondate', 'accessionnumber',
       'medium', 'classification', 'dimensions', 'repository', 'tags',
       'imageurl', 'inscription', 'markings', 'artistdisplayname', 'artistid',
       'artistnationality', 'artistprefix', 'artistsuffix', 'nationality',
       'artistbegindate', 'artistenddate', 'artistgender', 'artistrole',
       'artistbio', 'artistulanurl', 'artistwikidataurl', 'objectwikidataurl',
       'tagsaaturl', 'creditline', 'tagswikidataurl', 'artworkurl',
       'rightsandreproduction', 'gallery', 'artistbirthplace',
       'artistdeathplace', 'continent', 'longitude', 'latitude', 's3url']
    return render_template('template.html', data = data[1], page = "query", keys = keys, input = dict(request.form))

@app.route('/image', methods=['POST'])
def upload_file():
    uploaded_file = request.form.get('file')
    files = list(pd.read_csv("test_images.csv")['filepath'])

    if request.form['count'] == '' or request.form['count'] == None:
        input = {}
        input['count'] = 0
        return render_template('template.html', page = "image",uploaded_image = "all_image_data/" + uploaded_file, hasimage= False, test_images = files, input=input)

    N = int(request.form['count'])
    if uploaded_file and N >= 0 and N < 2000:
        models = predict.model_pred()
        images = predict.predictions(uploaded_file, N+1, (224, 224), models)
        return render_template('template.html', imagelist = images, page = "image",uploaded_image = "all_image_data/" + uploaded_file, hasimage= True, test_images = files, input = dict(request.form))
    else:
        return render_template('template.html', page = "image",uploaded_image = "all_image_data/" + uploaded_file, hasimage= False, test_images = files, input = dict(request.form))

@app.route('/image', methods=['GET'])
def image_clustering():
    files = list(pd.read_csv("test_images.csv")['filepath'])
    keys = ['objectid', 'objectnumber', 'title', 'artworkdescription', 'culture',
       'city', 'country', 'timeperiod', 'artworkdate', 'datebegin', 'dateend',
       'department', 'accessionyear', 'accessiondate', 'accessionnumber',
       'medium', 'classification', 'dimensions', 'repository', 'tags',
       'imageurl', 'inscription', 'markings', 'artistdisplayname', 'artistid',
       'artistnationality', 'artistprefix', 'artistsuffix', 'nationality',
       'artistbegindate', 'artistenddate', 'artistgender', 'artistrole',
       'artistbio', 'artistulanurl', 'artistwikidataurl', 'objectwikidataurl',
       'tagsaaturl', 'creditline', 'tagswikidataurl', 'artworkurl',
       'rightsandreproduction', 'gallery', 'artistbirthplace',
       'artistdeathplace', 'continent', 'longitude', 'latitude', 's3url']
    form = {}
    for k in keys:
        form[k] = ""

    input = {}
    input['count'] = 0
    return render_template('template.html', page = "image", hasimage= False, test_images = files, input = input)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=809, debug =True)