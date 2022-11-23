
function check_taxon_rank(rank){
    var value = rank.value;
    if (value !== '' ) {
        document.getElementById("Taxon_id").disabled = false;
    } else {
        document.getElementById("Taxon_id").disabled = true;
    }
}

function get_row_data(button) {
    var boolean_button = button.firstElementChild.checked;
    if (boolean_button === true) {
        var bench_id = button.nextElementSibling.nextElementSibling.innerText;
        var hidden_row = document.getElementById("hidden_row"+bench_id);
        //fino a qua, ok
        var hidden_row_children = hidden_row.getElementsByTagName("p");
        console.log("hidden row child: "+hidden_row_children);
        var hrc_array = [];
        for (var i = 0; i < hidden_row_children.length; i++) {
            if(hidden_row_children[i].hasAttribute("name")){
                hrc_array[i] = hidden_row_children.item(i).innerText;
            }
        }
        return hrc_array;
    } else {
        return [];
    }
}

function get_data_rows() {
    var rows = document.getElementsByTagName('tr');
    var array = [];
    var array_temp = [];
    for (var i = 1; i < rows.length; i++) {
        if (i % 2 !== 0) {
            array_temp = get_row_data(rows.item(i).firstElementChild);
            if (array_temp.length !== 0) {
                array = array.concat(array_temp + "\n");
            }
        }
    }
    return array;
}


function get_table_header() {
    var rows = document.getElementsByTagName('tr');
    var row = rows[0];
    var ths = row.getElementsByTagName('th');
    var ths_array = [];
    for (var i = 1; i < ths.length; i++) {
        if (i === (ths.length - 1)) {
            ths_array[i - 1] = ths.item(i).innerText;
        } else {
            ths_array[i - 1] = ths.item(i).innerText + ",";
        }
    }
    return ths_array;
}

function get_reference_id(row){
    var ref_id = row.firstElementChild.nextElementSibling.nextElementSibling;
    var button = row.firstElementChild;
    var boolean_button = button.firstElementChild.checked;
    if (boolean_button === true) {
        return ref_id.innerText;
    } else {
        return '';
    }
}

function get_all_ref_ids() {
    var rows = document.getElementsByTagName('tr')
    ref_id_string = '';
    for(var i = 1; i < rows.length; i++) {
            var temp = get_reference_id(rows[i]);
            if (temp !== '') {
                var ref_id_string = ref_id_string + temp + ",";
            }
    }
    return ref_id_string;
}

function check_format_dl(){
    var check_buttons = document.getElementsByClassName("check_button_format")
    var result = '';
    for(var i = 0; i < check_buttons.length; i++) {
        if(check_buttons[i].checked === true){
            result = check_buttons[i].value + "," + result;
        }
    }
    return  result;
}

function check_taxonomy_dl(){
    var check_buttons = document.getElementsByClassName("check_button_taxonomy")
    var result = '';
    for(var i = 0; i < check_buttons.length; i++) {
        if(check_buttons[i].checked === true){
            result = check_buttons[i].value + "," + result;
        }
    }
    return  result;
}


function download_csv_from_db() {
    var all_ref_id = get_all_ref_ids();
    var taxonomy = check_taxonomy_dl();
    $.ajax({
        url: '/download_files_csv/' + all_ref_id +'/'+ taxonomy,
        type: 'GET',
        context: document.body,
        xhrFields:{
            responseType: 'blob'
        },
        success: function(data) {
            saveAs(data, "rna_sequences.csv");
        }
    });
}


function download_file_from_db() {
    var all_ref_id = get_all_ref_ids();
    var formats = check_format_dl();
    $.ajax({
        url: '/download_files/' + all_ref_id +'/'+ formats,
        type: 'GET',
        context: document.body,
        xhrFields:{
            responseType: 'blob',
        },
        success: function(data) {
            saveAs(data, "rna_sequences_files.zip");
        }
    });
}


function final_download(){
    if (confirm ('Are you sure you want to download these files? \n' +
        'N.B. Please consider that if you are downloading a lot of files it might take some time.')) {
        download_csv_from_db();
        download_file_from_db();
    }
}



function showHideRow(row) {
    $("#" + row).toggle();
}



/**
 * It checks if the taxonomy is classified, and if it is, it calls the function to show the taxonomy
 * @param bench_id - the id of the bench
 * @returns The taxonomy of the sequence.
 */
function show_taxonomy(bench_id){
    if(document.getElementById("silva_taxon"+bench_id)){
        return;
    }
    if (document.getElementById("silva_taxonomy" + bench_id).innerHTML.toString().split("'")[3] === 'Yes'){
        show_taxonomy_silva(bench_id);
    }else{
        var el_s = document.createElement("p");
        var nd_s = document.createTextNode("Not Classified");
        el_s.appendChild(nd_s);
        el_s.setAttribute("id", "silva_taxon"+bench_id)
        document.getElementById("silva_div"+bench_id).appendChild(el_s);
    }
     if (document.getElementById("ena_taxonomy" + bench_id).innerHTML.toString().split("'")[3] === 'Yes'){
        show_taxonomy_ena(bench_id);
    }else{
        var el_e = document.createElement("p");
        var nd_e = document.createTextNode("Not Classified");
        el_e.appendChild(nd_e);
        document.getElementById("ena_div"+bench_id).appendChild(el_e);
    }
     if (document.getElementById("ltp_taxonomy" + bench_id).innerHTML.toString().split("'")[3] === 'Yes'){
        show_taxonomy_ltp(bench_id);
    }else{
        var el_l = document.createElement("p");
        var nd_l = document.createTextNode("Not Classified");
        el_l.appendChild(nd_l);
        document.getElementById("ltp_div"+bench_id).appendChild(el_l);
    }
     if (document.getElementById("ncbi_taxonomy" + bench_id).innerHTML.toString().split("'")[3] === 'Yes'){
        show_taxonomy_ncbi(bench_id);
    }else{
        var el_n = document.createElement("p");
        var nd_n = document.createTextNode("Not Classified");
        el_n.appendChild(nd_n);
        document.getElementById("ncbi_div"+bench_id).appendChild(el_n);
    }
     if (document.getElementById("gtdb_taxonomy" + bench_id).innerHTML.toString().split("'")[3] === 'Yes'){
        show_taxonomy_gtdb(bench_id);
    }else{
        var el_g = document.createElement("p");
        var nd_g = document.createTextNode("Not Classified");
        el_g.appendChild(nd_g);
        document.getElementById("gtdb_div"+bench_id).appendChild(el_g);
    }
}

function show_taxonomy_silva(bench_id) {
    var silva = document.getElementById('silva_taxonomy'+bench_id).innerHTML.toString();
    var temp = silva.split("'");
    var position = document.getElementById("silva_div"+bench_id);
    var rank = []
    var rank_cont = 0
    for (var i = 5; i< temp.length;i++){
        if(i%2 !== 0){
            if(rank_cont%2 === 0){
                rank.push(temp[i])
            }else {
                var element = document.createElement("p");
                element.setAttribute("id", "silva_taxon" + bench_id);
                element.setAttribute("class", "popover-test")
                element.setAttribute("data-mdb-toggle", "popover")
                element.setAttribute("title", rank.pop())
                console.log("Taxa:", temp[i])
                var node = document.createTextNode(temp[i]);
                element.appendChild(node);
                position.appendChild(element);
            }
            rank_cont++;
        }
    }
}

function show_taxonomy_ena(bench_id) {
    var ena = document.getElementById('ena_taxonomy'+bench_id).innerHTML.toString();
    var temp = ena.split("'");
    var position = document.getElementById("ena_div"+bench_id);
    var rank = []
    var rank_cont = 0
    for (var i = 5; i< temp.length;i++){
        if(i%2 !== 0){
            if(rank_cont%2 === 0){
                rank.push(temp[i])
            }else {
                var element = document.createElement("p");
                element.setAttribute("id", "ena_taxon" + bench_id);
                element.setAttribute("class", "popover-test")
                element.setAttribute("data-mdb-toggle", "popover")
                element.setAttribute("title", rank.pop())
                var node = document.createTextNode(temp[i]);
                element.appendChild(node);
                position.appendChild(element);
            }
            rank_cont++;
        }
    }
}

function show_taxonomy_gtdb(bench_id) {
    var gtdb = document.getElementById('gtdb_taxonomy'+bench_id).innerHTML.toString();
    var temp = gtdb.split("'");
    var position = document.getElementById("gtdb_div"+bench_id);
    var rank = []
    var rank_cont = 0
    for (var i = 5; i< temp.length;i++){
        if(i%2 !== 0){
            if(rank_cont%2 === 0){
                rank.push(temp[i])
            }else {
                var element = document.createElement("p");
                element.setAttribute("id", "gtdb_taxon" + bench_id);
                element.setAttribute("class", "popover-test")
                element.setAttribute("data-mdb-toggle", "popover")
                element.setAttribute("title", rank.pop())
                var node = document.createTextNode(temp[i]);
                element.appendChild(node);
                position.appendChild(element);
            }
            rank_cont++;
        }
    }
}

function show_taxonomy_ltp(bench_id) {
    var ena = document.getElementById('ltp_taxonomy'+bench_id).innerHTML.toString();
    var temp = ena.split("'");
    var position = document.getElementById("ltp_div"+bench_id);
    var rank = []
    var rank_cont = 0
    for (var i = 5; i< temp.length;i++){
        if(i%2 !== 0){
            if(rank_cont%2 === 0){
                rank.push(temp[i])
            }else {
                var element = document.createElement("p");
                element.setAttribute("id", "ltp_taxon" + bench_id);
                element.setAttribute("class", "popover-test")
                element.setAttribute("data-mdb-toggle", "popover")
                element.setAttribute("title", rank.pop())
                var node = document.createTextNode(temp[i]);
                element.appendChild(node);
                position.appendChild(element);
            }
            rank_cont++;
        }
    }
}

function show_taxonomy_ncbi(bench_id) {
    var ena = document.getElementById('ncbi_taxonomy'+bench_id).innerHTML.toString();
    var temp = ena.split("'");
    var position = document.getElementById("ncbi_div"+bench_id);
    var rank = []
    var rank_cont = 0
    for (var i = 5; i< temp.length;i++){
        if(i%2 !== 0){
            if(rank_cont%2 === 0){
                rank.push(temp[i])
            }else {
                var element = document.createElement("p");
                element.setAttribute("id", "ncbi_taxon" + bench_id);
                element.setAttribute("class", "popover-test")
                element.setAttribute("data-mdb-toggle", "popover")
                element.setAttribute("title", rank.pop())
                var node = document.createTextNode(temp[i]);
                element.appendChild(node);
                position.appendChild(element);
            }
            rank_cont++;
        }
    }
}
