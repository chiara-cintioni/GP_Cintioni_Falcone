import io
import json
import os
import threading
from datetime import timedelta
import pandas
import tempfile
import zipfile
from bson import json_util
from flask import Flask, render_template, request, send_file, session
from pandas import json_normalize
import gridfs
import config
import search_script
import uuid

app = Flask(__name__)
app.secret_key = 'ajdhaskdjhdkjadhfsdsd'
lock = threading.Lock()

# Loading the configuration from the config.py file.
app.config.from_pyfile('config.py')

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/search/', methods=('GET', 'POST'))
def search():
    before_request('/search/')
    return render_template('search.html')


'''
It takes the input from the user and uses it to search the database
:return: The result of the search.
'''


@app.route('/search/res/', methods=['POST'])
def search_result():
    before_request('/search/res/')
    if request.method == 'POST':
        collection_id = get_session_id()
        temp = config.DB.get_collection("rna_sequences").find({})
        config.DB.get_collection(collection_id).insert_many(temp)
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
        result_taxonomy_rank = search_script.search_rank(taxonomy, rank, taxon, config.DB.get_collection(collection_id),
                                                         collection_id)
        result_org_name = search_script.search_org_name(org_name, result_taxonomy_rank, collection_id)
        result_acc_num = search_script.search_acc_num(acc_num, result_org_name, collection_id)
        result_length = search_script.search_length(int(from_length), int(to_length), result_acc_num, collection_id)
        result_decoupled = search_script.search_num_decoup(int(num_dec), result_length, collection_id)
        result_weak_bonds = search_script.search_weak_bonds(int(weak_from), int(weak_to), result_decoupled,
                                                            collection_id)
        result_is_pseudo = search_script.search_is_pseudo(is_pseudoknotted, result_weak_bonds, collection_id)
        result_pseudo_ord = search_script.search_pseudo_order(int(pseudoknot_ord), result_is_pseudo, collection_id)
        result_rna_type = search_script.search_rna_type(rna_type, result_pseudo_ord, collection_id)
        result_genus = search_script.search_genus(int(genus), result_rna_type, collection_id)
        result_core = search_script.search_core(core, result_genus, collection_id)
        result_core_plus = search_script.search_core_plus(core_plus, result_core, collection_id)
        result_shape = search_script.search_shape(shape, result_core_plus, collection_id)
        result_benchmark = search_script.search_benchmark(benchmark_id, result_shape, collection_id)
        result_taxonomy = search_script.search_taxonomy(taxonomy, result_benchmark, collection_id)
        result_db_name = search_script.search_db_name(db_name, result_taxonomy, collection_id)
        result_is_validated = search_script.search_is_validated(is_validated, result_db_name, collection_id)
        # result gets the final output of the user research
        result = config.DB.get_collection(collection_id).find()
        return render_template("search_results.html", result_list=result)


'''
Download of rna, selected from the table, in csv format
'''


@app.route('/download_files_csv', methods=['POST'])
def download():
    if request.method == 'POST':
        data = request.json
        filenames = data['filenames']
        taxonomy = data['taxonomy'].split(sep=",")[0]
        config.DB.get_collection(get_session_id()).delete_many({})
        for filename in filenames:
            if filename != '' and taxonomy != '':
                search_script.get_file_with_one_taxonomy(filename, taxonomy, get_session_id())
        mongo_docs = config.DB.get_collection(get_session_id()).find({}, {'_id': False})
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
Download addictional files
'''


@app.route('/download_files', methods=['POST'])
def download_zip_files():
    if request.method == 'POST':
        data = request.json
        filenames = data['filenames']
        formats = data['formats'].split(sep=",")
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zf:
            for f in formats:
                if f != '':
                    for filename in filenames:
                        if filename != '':
                            file = filename + f
                            fs = gridfs.GridFS(config.DB)
                            data = config.DB.fs.files.find_one({'filename': file})
                            file_id = data['_id']
                            output_data = fs.get(file_id).read()
                            zf.writestr(file, output_data)
    memory_file.seek(0)
    return send_file(memory_file, as_attachment=True, download_name='zipFile.zip')


@app.route('/')
def home():
    before_request('/')
    # Provenience of PhyloRNA Structures table
    num_RCSB = config.COLLECTION.count_documents({'Reference database': 'NULL'})
    num_CRW = config.COLLECTION.count_documents({'Reference database': 'CRW'})
    num_tmRNA = config.COLLECTION.count_documents({'Reference database': 'NULL'})
    num_sprinzl = config.COLLECTION.count_documents({'Reference database': 'NULL'})
    num_RNASE = config.COLLECTION.count_documents({'Reference database': 'NULL'})
    num_SRP = config.COLLECTION.count_documents({'Reference database': 'NULL'})
    num_RFAM = config.COLLECTION.count_documents({'Reference database': 'RFAM'})
    num_NAD = config.COLLECTION.count_documents({'Reference database': 'NULL'})
    # Classes of PhyloRNA structures table
    num_5S = config.COLLECTION.count_documents({'Rna Type': '5S'})
    num_16S = config.COLLECTION.count_documents({'Rna Type': '16S'})
    num_23S = config.COLLECTION.count_documents({'Rna Type': '23S'})
    num_GI1 = config.COLLECTION.count_documents({'Rna Type': 'Group I Introns'})
    num_GI2 = config.COLLECTION.count_documents({'Rna Type': 'Group II Introns'})
    num_tRNA = config.COLLECTION.count_documents({'Rna Type': 'tRNA'})
    return render_template('home.html', num_RCSB=num_RCSB, num_CRW=num_CRW, num_tmRNA=num_tmRNA,
                           num_sprinzl=num_sprinzl, num_RNASE=num_RNASE, num_SRP=num_SRP, num_RFAM=num_RFAM,
                           num_NAD=num_NAD, num_5S=num_5S, num_16S=num_16S, num_23S=num_23S, num_GI1=num_GI1,
                           num_GI2=num_GI2, num_tRNA=num_tRNA)


def get_session_id():
    if "session_id" in session:
        return str(session["session_id"])
    else:
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
        return session_id


def before_request(url):
    with lock:
        print("Url attuale: ", url)
        print("Url precedente: ", session.get('previous_url'))
        if session.get('previous_url') == '/search/res/':
            if url != '/search/res/':
                session['previous_url'] = url
                config.DB.get_collection(get_session_id()).delete_many({})
                config.DB.get_collection(get_session_id()).drop()
                session.pop('session_id')
        else:
            session['previous_url'] = url


@app.route('/contact/')
def contact():
    before_request('/contact/')
    return render_template('contact.html')


@app.route('/sources/')
def sources():
    before_request('/sources/')
    num_docs = config.COLLECTION.count_documents({})
    return render_template('sources.html', num_docs=num_docs)


@app.route('/tutorial/search')
def s_tutorial():
    before_request('/tutorial/search')
    return render_template('s_tutorial.html')


@app.route('/tutorial/download')
def d_tutorial():
    before_request('/tutorial/download')
    return render_template('d_tutorial.html')
