import io
import json
import os
import pandas
import tempfile
import time
import zipfile
from bson import json_util
from flask import Flask, render_template, request, send_file
from pandas import json_normalize
from pymongo import MongoClient
import config
import search_script

app = Flask(__name__)

# Connecting to the MongoDB database.
#client = MongoClient('mongodb+srv://DeniseFalcone:Giappone4ever@cluster0.yelotpf.mongodb.net/test', 27017)
client = MongoClient('localhost')
db = client.RIBOdb
collection = db.rna_sequences

# Loading the configuration from the config.py file.
app.config.from_pyfile('config.py')

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/search/', methods=('GET', 'POST'))
def search():
    return render_template('search.html')


# It takes the input from the user and uses it to search the database
# :return: The result of the search.
@app.route('/search/res/', methods=['POST'])
def search_result():
    if request.method == 'POST':
        org_name = request.form['Organism name']
        from_length = request.form['Length_from']
        # if the user doesn't insert any input, the variable takes the default value
        if from_length == '':
            from_length = -1
        to_length = request.form['Length_to']
        if to_length == '':
            to_length = -1
        acc_num = request.form['Accession number']
        benchmark_id = request.form['Benchmark ID']
        num_dec = request.form['Number of decoupled nucleotides']
        if num_dec == '':
            num_dec = -1
        weak_from = request.form['Number_of_weak_bonds_from']
        if weak_from == '':
            weak_from = -1
        weak_to = request.form['Number_of_weak_bonds_to']
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
        is_validated = request.form['Is Validated']
        # the order of the result search in the database needs to be in this order, or it doesn't work.
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
        result_benchmark = search_script.search_benchmark(benchmark_id, result_shape)
        result_taxonomy = search_script.search_taxonomy(taxonomy, result_benchmark)
        result_db_name = search_script.search_db_name(db_name, result_taxonomy)
        result_is_validated = search_script.search_is_validated(is_validated, result_db_name)
        # result gets the final output of the user research
        result = result_is_validated.find()
        return render_template("search_results.html", result_list=result)


# It takes a list of filenames and a taxonomy, then it searches the database for all the documents that have the
# given taxonomy and the given filenames, then it creates a temporary file with the results, then it sends the
# temporary file to the user.
# :param filenames: a list of filenames to download
# :param taxonomy: the taxonomy you want to search for
# :return: The file is being returned.
'''
@app.route('/download_files_csv/<filenames>/<taxonomy>', methods=['GET'])
def download(filenames, taxonomy):
    if request.method == 'GET':
        filenames = filenames.split(sep=',')
        taxonomy = taxonomy.split(sep=',')[0]
        db.get_collection("temp").delete_many({})
        for filename in filenames:
            if filename != '' and taxonomy != '':
                search_script.get_file_with_one_taxonomy(filename, taxonomy)
        mongo_docs = db.get_collection("temp").find({}, {'_id': False})
        sanitized_mongo_docs = json.loads(json_util.dumps(mongo_docs))
        normalized_mongo_docs = json_normalize(sanitized_mongo_docs)
        final_mongo_docs = pandas.DataFrame(normalized_mongo_docs)
        # We use os.path.join(tempfile.gettempdir(), os.urandom(24).hex()) because it's reliable, cross-platform and
        # the only caveat is that it doesn't work on FAT partitions. NamedTemporaryFile has a number of issues,
        # not the least of which is that it can fail to create files because of a permission error, fail to detect
        # the permission error, and then loop millions of times, hanging your program and your filesystem.
        temp_file = os.path.join(tempfile.gettempdir(), os.urandom(24).hex())
        final_mongo_docs.to_csv(temp_file, sep=',', index=False)
        return send_file(temp_file, as_attachment=True)

'''

'''
@app.route('/download_files_csv', methods=['POST'])
def download():
    filenames = request.form.getlist('filenames')
    taxonomy = request.args.get("taxonomy")
    db.get_collection("temp").delete_many({})
    for filename in filenames:
        if filename != '' and taxonomy != '':
            search_script.get_file_with_one_taxonomy(filename, taxonomy)
    mongo_docs = db.get_collection("temp").find({}, {'_id': False})
    sanitized_mongo_docs = json.loads(json_util.dumps(mongo_docs))
    normalized_mongo_docs = json_normalize(sanitized_mongo_docs)
    final_mongo_docs = pandas.DataFrame(normalized_mongo_docs)
    temp_file = os.path.join(tempfile.gettempdir(), os.urandom(24).hex())
    final_mongo_docs.to_csv(temp_file, sep=',', index=False)
    return send_file(temp_file, as_attachment=True)
'''


@app.route('/download_files_csv', methods=['POST'])
def download():
    data = request.json
    filenames = data['filenames']
    taxonomy = data['taxonomy'].split(sep=",")[0]
    db.get_collection("temp").delete_many({})
    for filename in filenames:
        if filename != '' and taxonomy != '':
            search_script.get_file_with_one_taxonomy(filename, taxonomy)
    mongo_docs = db.get_collection("temp").find({}, {'_id': False})
    sanitized_mongo_docs = json.loads(json_util.dumps(mongo_docs))
    normalized_mongo_docs = json_normalize(sanitized_mongo_docs)
    final_mongo_docs = pandas.DataFrame(normalized_mongo_docs)
    # We use os.path.join(tempfile.gettempdir(), os.urandom(24).hex()) because it's reliable, cross-platform and
    # the only caveat is that it doesn't work on FAT partitions. NamedTemporaryFile has a number of issues,
    # not the least of which is that it can fail to create files because of a permission error, fail to detect
    # the permission error, and then loop millions of times, hanging your program and your filesystem.
    temp_file = os.path.join(tempfile.gettempdir(), os.urandom(24).hex())
    final_mongo_docs.to_csv(temp_file, sep=',', index=False)
    return send_file(temp_file, as_attachment=True)

# It takes two strings as input, one containing the filenames and the other containing the formats, and it returns a zip
# file containing the files with the specified filenames and formats.
# :param filenames: a string of filenames separated by commas
# :param formats: a string of file extensions separated by commas
# :return: a zip file containing the files selected by the user.
@app.route('/download_files/<filenames>/<formats>', methods=['GET'])
def download_zip_files(filenames, formats):
    if request.method == 'GET':
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zf:
            filenames = filenames.split(sep=',')
            formats = formats.split(sep=',')
            for f in formats:
                format_path = return_format_path(f)
                if format_path != '':
                    for filename in filenames:
                        if filename != '':
                            file = filename + f
                            for file_selected in os.listdir(format_path):
                                if file == file_selected:
                                    file_path = os.path.join(format_path, file_selected)
                                    open_file = open(file_path, 'r')
                                    file_content = ''
                                    for line in open_file:
                                        file_content = file_content + line
                                    data = zipfile.ZipInfo(file_selected)
                                    data.date_time = time.localtime(time.time())[:6]
                                    data.compress_type = zipfile.ZIP_DEFLATED
                                    zf.writestr(data, file_content)
                                    break
        memory_file.seek(0)
        # Ricontrollare perche' chiamiamo search_result()
        # search_result()
        # download name non puo' essere tolto
        return send_file(memory_file, as_attachment=True, download_name='zipFile.zip')


def return_format_path(f):
    if f == '.dbn':
        format_path = config.DBN_FILES
        return format_path
    elif f == '.ct':
        format_path = config.CT_FILES
        return format_path
    elif f == '.bpseq':
        format_path = config.BPSEQ_FILES
        return format_path
    elif f == '.fasta':
        format_path = config.FASTA_FILES
        return format_path
    elif f == '_nH.dbn':
        format_path = config.DB_FILES_NH
        return format_path
    elif f == '_nH.ct':
        format_path = config.CT_FILES_NH
        return format_path
    elif f == '_nH.bpseq':
        format_path = config.BPSEQ_FILES_NH
        return format_path
    elif f == '_nH.fasta':
        format_path = config.FASTA_FILES_NH
        return format_path
    else:
        format_path = ''
    return format_path


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/contact/')
def contact():
    return render_template('contact.html')


@app.route('/sources/')
def sources():
    return render_template('sources.html')


@app.route('/tutorial/search')
def s_tutorial():
    return render_template('s_tutorial.html')


@app.route('/tutorial/download')
def d_tutorial():
    return render_template('d_tutorial.html')
