# importiamo l'oggetto flask dal flask package.
from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

# usiamo l'oggetto Flask per creare l'istanza della nostra app Flask con il nome app.
# __name__ è il nome del modulo python corrente. Usato per dire all'app dove si trova. Serve perché Flask definisce dei path dietro le quinte.
app = Flask(__name__)

# ora che abbiamo creato l'app, la useremo per gestire le richieste HTTP che riceviamo.

client = MongoClient('mongodb+srv://DeniseFalcone:Giappone4ever@cluster0.yelotpf.mongodb.net/test', 27017)
db = client.RIBOdb
collection = db.prova

#è un decoratore che rende una funzione python regolare in una funzione di vista Flask.
#serve a convertire il valore di ritorno della funzione in una risposta HTTP da far vedere
#al cliente HTTP, come un browser web.
#'/' vuol dire che la funzione risponderà alle richieste web per l'url '/' che è l'url principale.
# corrisponde al nostro home.html
@app.route('/search/', methods=('GET','POST'))
def search():
    if request.method == 'POST':
        content = request.form['organism_name']
        degree = request.form['reference_id']
        collection.insert_one({'Organism name': content, 'Reference ID': degree})
        return redirect(url_for('search'))

    all_collections = collection.find()
    return render_template('search2.html', collection=all_collections)

@app.route('/home/')
def home():
    return render_template('home.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/sources/')
def sources():
    return render_template('sources.html')

@app.route('/search_tutorial')
def s_tutorial():
    return render_template('s_tutorial.html')

@app.route('/download_tutorial')
def d_tutorial():
    return render_template('d_tutorial.html')

@app.route('/download/')
def download():
    return render_template('download.html')

@app.route('/info/')
def info():
    return render_template('info.html')

@app.route('/list', methods=['GET','POST'])
def lists():
    if request.method == 'POST':
        my_position = request.form['mypos']#form input on initial position
        check_db = collection.find()#check all documents in collection
        for record in check_db:
            if record['content'] == my_position:
                return 'found'
            else:
                return 'sorry route not found'

    return render_template('form.html')

@app.post('/<id>/delete/')
def delete(id):
    collection.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

