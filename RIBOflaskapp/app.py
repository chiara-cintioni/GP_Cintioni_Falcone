# importiamo l'oggetto flask dal flask package.
import io
import json
import os
import tempfile
import time
import zipfile


from bson import json_util
from flask import Flask, render_template, request, send_file
import pandas
from pandas import json_normalize
from pymongo import MongoClient

import search_script

# usiamo l'oggetto Flask per creare l'istanza della nostra app Flask con il nome app.
# __name__ è il nome del modulo python corrente. Usato per dire all'app dove si trova. Serve perché Flask definisce dei path dietro le quinte.
app = Flask(__name__)

#per ubuntu per prendere i file : /var/www/gci/Flask_App/RIBOflaskapp/static/client/nomefile
app.config[
    "DB_FILES"] = "C:\\Users\\Chiara\\OneDrive\\Desktop\\GP-Master\\GP_DA_GIT\\GroupProject-master\\RIBOflaskapp\\static\\client\\db_file"
app.config[
    "CT_FILES"] = "C:\\Users\\Chiara\\OneDrive\\Desktop\\GP-Master\\GP_DA_GIT\\GroupProject-master\\RIBOflaskapp\\static\\client\\ct_file"
app.config[
    "BPSEQ_FILES"] = "C:\\Users\\Chiara\\OneDrive\\Desktop\\GP-Master\\GP_DA_GIT\\GroupProject-master\\RIBOflaskapp\\static\\client\\bpseq_file"
app.config[
    "BPSEQ_FILES_NH"] = "C:\\Users\\Chiara\\OneDrive\\Desktop\\GP-Master\\GP_DA_GIT\\GroupProject-master\\RIBOflaskapp\\static\\client\\bpseq_nH_file"
app.config[
    "CT_FILES_NH"] = "C:\\Users\\Chiara\\OneDrive\\Desktop\\GP-Master\\GP_DA_GIT\\GroupProject-master\\RIBOflaskapp\\static\\client\\ct_nH_file"
app.config[
    "DB_FILES_NH"] = "C:\\Users\\Chiara\\OneDrive\\Desktop\\GP-Master\\GP_DA_GIT\\GroupProject-master\\RIBOflaskapp\\static\\client\\db_nH_file"


# ora che abbiamo creato l'app, la useremo per gestire le richieste HTTP che riceviamo.

client = MongoClient('mongodb+srv://DeniseFalcone:Giappone4ever@cluster0.yelotpf.mongodb.net/test', 27017)
#client = MongoClient('localhost')
db = client.RIBOdb
collection = db.rna_sequences


if __name__ == '__main__':
    app.run(debug=True)

app.config.from_pyfile('config.py')


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
        rank = request.form['Taxonomy_rank']
        taxon = request.form['rank_value']
        db_name = request.form['Database']
        is_val = request.form['Is Validated']
        # taxonomy rank deve essere fatto come primo controllo di campo ricerca: il problema sta nella collection temp che potrebbe essere cancellata ce semo capiti
        result_taxonomy_rank = search_script.search_rank(taxonomy, rank, taxon, collection)
        result_org_name = search_script.search_org_name(org_name, result_taxonomy_rank)
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
        result_db_name = search_script.search_db_name(db_name, result_taxonomy)
        result_is_validated = search_script.search_is_validated(is_val, result_db_name)
        result = result_is_validated.find()
        return render_template("search_results.html", result_list=result)


@app.route('/download_files_csv/<filenames>/<taxonomy>', methods=['GET', 'POST'])
def download(filenames, taxonomy):
    if request.method == 'GET':
        filenames = filenames.split(sep=',')
        taxonomy = taxonomy.split(sep=',')
        db.get_collection("temp").delete_many({})
        for filename in filenames:
            if filename != '' and taxonomy[0] != '':
                search_script.get_file_with_one_taxonomy(filename, taxonomy[0])
        mongo_docs = db.get_collection("temp").find({},{'_id':False})
        sanitized = json.loads(json_util.dumps(mongo_docs))
        normalized = json_normalize(sanitized)
        docs = pandas.DataFrame(normalized)
        '''
        Consider using os.path.join(tempfile.gettempdir(), os.urandom(24).hex()) instead. 
        It's reliable, cross-platform, and the only caveat is that it doesn't work on FAT partitions. 
        NamedTemporaryFile has a number of issues, not the least of which is that it can fail to create files because of a permission error,
        fail to detect the permission error, and then loop millions of times, hanging your program and your filesystem.
        '''
        temp = os.path.join(tempfile.gettempdir(), os.urandom(24).hex())
        print("temp: "+temp)
        docs.to_csv(temp, sep=',', index=False)
        return send_file(temp, as_attachment=True, download_name='Result.csv')



@app.route('/download_files/<filenames>/<formats>', methods=['GET', 'POST'])
def test(filenames, formats):
    if request.method == 'GET':
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zf:
            filenames = filenames.split(sep=',')
            formats = formats.split(sep=',')
            for f in formats:
                path = return_format(f)
                if path != '':
                    for file in filenames:
                        if file != '':
                            file = file + f
                            for file_selected in os.listdir(path):
                                if file == file_selected:
                                    print("file: " + file)
                                    file_path = os.path.join(path, file_selected)
                                    op_file = open(file_path, 'r')
                                    long_line = ''
                                    for line in op_file:
                                        long_line = long_line + line
                                    data = zipfile.ZipInfo(file_selected)
                                    data.date_time = time.localtime(time.time())[:6]
                                    data.compress_type = zipfile.ZIP_DEFLATED
                                    zf.writestr(data, long_line)
                                    break
        memory_file.seek(0)
        search_result()
        return send_file(memory_file, as_attachment=True, download_name='files.zip')


def return_format(f):
    if f =='.db':
        path = app.config['DB_FILES']
        return path
    elif f == '.ct':
        path = app.config['CT_FILES']
        return path
    elif f == '.bpseq':
        path = app.config['BPSEQ_FILES']
        return path
    elif f =='nH.db':
        path = app.config['DB_FILES_NH']
        return path
    elif f== 'nH.ct':
        path = app.config['CT_FILES_MH']
        return path
    elif f=='nH.bpseq':
        path = app.config['BPSEQ_FILES_NH']
        return path
    else :
        path = ''
    return path


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

