# importiamo l'oggetto flask dal flask package.
from flask import Flask, render_template, request, url_for, redirect, send_file
from pymongo import MongoClient
import win32api

import download_from_db
import search_script


# usiamo l'oggetto Flask per creare l'istanza della nostra app Flask con il nome app.
# __name__ è il nome del modulo python corrente. Usato per dire all'app dove si trova. Serve perché Flask definisce dei path dietro le quinte.
app = Flask(__name__)

# ora che abbiamo creato l'app, la useremo per gestire le richieste HTTP che riceviamo.

#client = MongoClient('mongodb+srv://DeniseFalcone:Giappone4ever@cluster0.yelotpf.mongodb.net/test', 27017)
#db = client.RIBOdb
client = MongoClient('localhost')
db = client.RIBO_flask_db
collection = db.rna


@app.route('/search/', methods=('GET', 'POST'))
def search():
    return render_template('search.html')


@app.route('/search/res/', methods=['GET', 'POST'])
def search_result():
    if request.method == 'POST':
        org_name = request.form['Organism name']
        from_length = request.form['Length_from']
        to_length = request.form['Length_to']
        if from_length == '':
            from_length = -1
        if to_length == '':
            to_length = -1
        acc_num = request.form['Accession number']
        benchmark = request.form['Benchmark ID']
        num_dec = request.form['Number of decoupled nucleotides']
        if num_dec == '':
            num_dec = -1
        weak_from = request.form['Number_of_weak_bonds_from']
        weak_to = request.form['Number_of_weak_bonds_to']
        if weak_from == '':
            weak_from = -1
        if weak_to == '':
            weak_to = -1
        is_pseudoknotted = request.form['Is Pseudoknotted']
        pseudoknot_ord = request.form['Pseudoknot order']
        if pseudoknot_ord == '':
            pseudoknot_ord = -1
        rna_type = request.form['Rna Type']
        genus = request.form['Genus']
        if genus == '':
            genus = -1
        taxonomy = request.form['Taxonomy']
        core = request.form['Core']
        core_plus = request.form['Core plus']
        shape = request.form['Shape']
        result_org_name = search_script.search_org_name(org_name, collection)
        result_acc_num = search_script.search_acc_num(acc_num, result_org_name)
        result_length = search_script.search_length(int(from_length), int(to_length), result_acc_num)
        result_decoupled = search_script.search_num_decoup(int(num_dec), result_length)
        result_weak_bonds = search_script.search_weak_bonds(int(weak_from), int(weak_to), result_decoupled)
        result_is_pseudo = search_script.search_is_pseudo(is_pseudoknotted, result_weak_bonds)
        result_pseudo_ord = search_script.search_pseudo_order(int(pseudoknot_ord), result_is_pseudo)
        result_rna_type = search_script.search_rna_type(rna_type, result_pseudo_ord)
        result_genus = search_script.search_genus(int(genus), result_rna_type)
        result_core = search_script.search_core(core, result_genus)
        result_core_plus = search_script.search_core_plus(core_plus, result_core)
        result_shape = search_script.search_shape(shape, result_core_plus)
        result_benchmark = search_script.search_benchmark(benchmark, result_shape)
        result_taxonomy = search_script.search_taxonomy(taxonomy, result_benchmark)
        result = result_taxonomy.find()
        return render_template("search_results.html", result_list=result)

    return render_template('search_results.html')

@app.route('/download/')
def download():
    return render_template('download.html');


@app.route('/download_files/')
def test():
    ref_ids = request.args.get('variable', 'default').split(sep=",")
    format_string = request.args.get('format', 'default').split(sep=",")
    print(format_string)
    for i in format_string:
        print(i)
    for format_value in format_string:
        if format_value == "db":
            download_from_db.download_db_files(ref_ids)
        elif format_value == "ct":
            download_from_db.download_ct_files(ref_ids)
        elif format_value == "bpseq":
            download_from_db.download_bpseq_files(ref_ids)
        elif format_value == "db_nh":
            download_from_db.download_db_nh_files(ref_ids)
        elif format_value == "ct_nh":
            download_from_db.download_ct_nh_files(ref_ids)
        elif format_value == "bpseq_nh":
            download_from_db.download_bpseq_nh_files(ref_ids)
    return render_template('search_results.html');

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


@app.route('/info/')
def info():
    return render_template('info.html')



if __name__ == '__main__':
    app.run(debug=True)
