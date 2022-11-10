# importiamo l'oggetto flask dal flask package.
import io
import os
import pathlib
import shutil
import time
import zipfile
from zipfile import ZipFile

from flask import Flask, render_template, request, abort, send_file, send_from_directory, make_response
from pymongo import MongoClient
from flask_pymongo import PyMongo

import search_script

# usiamo l'oggetto Flask per creare l'istanza della nostra app Flask con il nome app.
# __name__ è il nome del modulo python corrente. Usato per dire all'app dove si trova. Serve perché Flask definisce dei path dietro le quinte.
app = Flask(__name__)

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

# client = MongoClient('mongodb+srv://DeniseFalcone:Giappone4ever@cluster0.yelotpf.mongodb.net/test', 27017)
# db = client.RIBOdb
client = MongoClient('localhost')
db = client.RIBOdb
collection = db.rna_sequences


@app.route('/search/', methods=('GET', 'POST'))
def search():
    return render_template('search.html')


@app.route('/search/res/', methods=['GET', 'POST'])
def search_result():
    # This is a conditional statement. It checks if the request method is POST.
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
        result = result_taxonomy.find()
        return render_template("search_results.html", result_list=result)
    return render_template('search_results.html')


@app.route('/download/')
def download():
    return render_template('download.html')


'''
@app.route('/download/', methods = ['GET', 'POST'])
def download():
    file_name = request.args.get('variable', 'default') + ".ct"
    print(file_name)
    grid_fs_file = fs.find_one({'filename': file_name})
    response = make_response(grid_fs_file.read())
    response.headers['Content-Type'] = 'text/ct'
    response.headers["Content-Disposition"] = "attachment; filename={}".format(file_name)
    return response
'''

''''
@app.route('/download_files/<filenames>')
def test(filenames):
    print(filenames)
    filename_array = filenames.split(sep=",")
    for filename in filename_array:
        dir2 = 'test'
        par_dir = 'C:\\Users\\Chiara\\OneDrive\\Desktop'
        path = os.path.join(par_dir, dir2)
        try:
            os.mkdir(path)
        except FileExistsError:
            os.rmdir(path)
            os.mkdir(path)
        for file in os.listdir(app.config['DB_FILES']):
            print(file)
            old_file_path = os.path.join(app.config['DB_FILES'], file)
            if os.path.isfile(old_file_path):
                if filename == file:
                    new_file_path = os.path.join(path, file)
                    with open(old_file_path, 'r') as old:
                        with open(new_file_path, 'w') as new:
                            old_file = old.readlines()
                            new.writelines(old_file)
                        new.close()
                    old.close()
    base_path = path
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w') as z:
        for f_name in os.listdir(base_path):
            z.write(f_name)
    data.seek(0)
    return send_file(
        data,
        mimetype='application/zip',
        as_attachment=True,
        download_name='gino.zip'

    )
    return render_template('search_results.html')
'''

'''


@app.route('/download_files/<filenames>')
def test(filenames):
    print(filenames)
    filename_array = filenames.split(sep=",")
    for filename in filename_array:
        dir2 = 'test'
        par_dir = 'C:\\Users\\Chiara\\OneDrive\\Desktop'
        path = os.path.join(par_dir, dir2)
        try:
            os.mkdir(path)
        except FileExistsError:
            os.rmdir(path)
            os.mkdir(path)
        for file in os.listdir(app.config['DB_FILES']):
            print(file)
            old_file_path = os.path.join(app.config['DB_FILES'], file)
            if os.path.isfile(old_file_path):
                if filename == file:
                    new_file_path = os.path.join(path, file)
                    with open(old_file_path, 'r') as old:
                        with open(new_file_path, 'w') as new:
                            old_file = old.readlines()
                            new.writelines(old_file)
                        new.close()
                    old.close()
    base_path = path
    buffer = io.BytesIO()
    with open(filename, 'wb') as f:
        f.write(buffer.getvalue())
        with ZipFile('gino.zip', mode='a') as archive:
            for f_name in os.listdir(base_path):
                with archive.open(f_name, 'w') as arc_open:
                    with open(f_name, mode='rb') as f_open:
                        while bytes := f_open.read(1):
                            arc_open.write(bytes)
        return send_file(
            "gino.zip",
            as_attachment=True,
            download_name='gino.zip'
        )
    return render_template('search_results.html')

'''


# FUNZIONA +-
@app.route('/download_files/<filenames>/<formats>', methods=['GET', 'POST'])
def test(filenames, formats):
    if request.method == 'GET':
        print("url: " + request.url)
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zf:
            filenames = filenames.split(sep=',')
            formats = formats.split(sep=',')
            for f in formats:
                print("f: " + f)
                path = return_format(f)
                print("path: " + path)
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
        return send_file(memory_file, as_attachment=True, download_name='files.zip')
    return render_template('search_results.html')


def return_format(f):
    match f:
        case '.db':
            path = app.config['DB_FILES']
            return path
        case '.ct':
            path = app.config['CT_FILES']
            return path
        case '.bpseq':
            path = app.config['BPSEQ_FILES']
            return path
        case 'nH.db':
            path = app.config['DB_FILES_NH']
            return path
        case 'nH.ct':
            path = app.config['CT_FILES_MH']
            return path
        case 'nH.bpseq':
            path = app.config['BPSEQ_FILES_NH']
            return path
        case '':
            path = ''
    return path


'''
@app.route('/download_files/', methods=['GET', 'POST'])
def test():
       print(request.method)
       if request.method == 'POST':
           ref_ids = request.args.get('variable', 'default').split(sep=",")
           format_string = request.args.get('format', 'default').split(sep=",")
           for id in ref_ids:
               print("i: " + id)
               for format_value in format_string:
                   print("format:" + format_value)
                   if format_value == "db":
                       path = "db_file/" + id + ".db"
                       filename = id + ".db"
                       print("path: " + path)
                   try:
                       return send_file(path, as_attachment=True)
                   except FileNotFoundError:
                       abort(404)
        return render_template('search_results.html')
'''

'''
VECCHIO DOWNLOAD

@app.route('/download_files/')
def test():
    ref_ids = request.args.get('variable', 'default').split(sep=",")
    format_string = request.args.get('format', 'default').split(sep=",")
    for i in format_string:
        print(i)
    for format_value in format_string:
        if format_value == "zip":
            download_from_db.create_zip_file(ref_ids, format_string)
            return render_template('search_results.html')
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
    return render_template('search_results.html')
 '''


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
