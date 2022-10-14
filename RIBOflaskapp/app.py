# importiamo l'oggetto flask dal flask package.
from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
import search_script

# usiamo l'oggetto Flask per creare l'istanza della nostra app Flask con il nome app.
# __name__ è il nome del modulo python corrente. Usato per dire all'app dove si trova. Serve perché Flask definisce dei path dietro le quinte.
app = Flask(__name__)

# ora che abbiamo creato l'app, la useremo per gestire le richieste HTTP che riceviamo.

client = MongoClient('mongodb+srv://DeniseFalcone:Giappone4ever@cluster0.yelotpf.mongodb.net/test', 27017)
db = client.RIBOdb
#client = MongoClient('localhost')
#db = client.databaseRIBO
collection = db.rna_sequences


@app.route('/search/', methods=('GET', 'POST'))
def search():
    return render_template('search.html')


@app.route('/search/result', methods=['GET', 'POST'])
def search_db():
    if request.method == 'POST':
        if request.form.get()
            redirect("/search/", code=302)
        org_name = request.form['Organism name']
        length = request.form['Length']
        if length == '':
            length = -1
        acc_num = request.form['Accession number']
        benchmark = request.form['Benchmark ID']
        num_dec = request.form['Number of decoupled nucleotides']
        if num_dec == '':
            num_dec = -1
        num_weak_bonds = request.form['Number of weak bonds']
        if num_weak_bonds == '':
            num_weak_bonds = -1
        is_pseudoknotted = request.form['Is Pseudoknotted']
        pseudoknot_ord = request.form['Pseudoknot order']
        if pseudoknot_ord == '':
            pseudoknot_ord = -1
        rna_type = request.form['Rna Type']
        genus = request.form['Genus']
        if genus == '':
            genus = -1
        core = request.form['Core']
        core_plus = request.form['Core plus']
        shape = request.form['Shape']
        result_org_name = search_script.search_org_name(org_name, collection)
        result_acc_num = search_script.search_acc_num(acc_num, result_org_name)
        result_length = search_script.search_length(int(length), result_acc_num)
        result_decoupled = search_script.search_num_decoup(int(num_dec), result_length)
        result_weak_bonds = search_script.search_weak_bonds(int(num_weak_bonds), result_decoupled)
        result_is_pseudo = search_script.search_is_pseudo(is_pseudoknotted, result_weak_bonds)
        result_pseudo_ord = search_script.search_pseudo_order(int(pseudoknot_ord), result_is_pseudo)
        result_rna_type = search_script.search_rna_type(rna_type, result_pseudo_ord)
        result_genus = search_script.search_genus(int(genus), result_rna_type)
        result_core = search_script.search_core(core, result_genus)
        result_core_plus = search_script.search_core_plus(core_plus, result_core)
        result_shape = search_script.search_shape(shape, result_core_plus)
        result_benchmark = search_script.search_benchmark(benchmark, result_shape)
        result = result_benchmark.find()
        return render_template("form.html", result_list=result)

    return render_template('form.html')


@app.route('/')
def home():
    return render_template('home.html')


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



if __name__ == '__main__':
    app.run(debug=True)
