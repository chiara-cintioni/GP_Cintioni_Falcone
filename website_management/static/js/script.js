
/**
 * If the user selects a taxon rank, enable the taxon dropdown menu
 * @param rank - the select box where the user can select a taxon rank
 */
function check_taxon_rank(rank){
    document.getElementById("Taxon_id").disabled = rank.value === '';
}

function check_format_dl(){
    var check_button_format = document.getElementsByClassName("check_button_format")
    var formats_string = '';
    for(var i = 0; i < check_button_format.length; i++) {
        if(check_button_format[i].checked === true){
            formats_string = check_button_format[i].value + "," + formats_string;
        }
    }
    return  formats_string;
}

function check_taxonomy_dl(){
    var check_buttons_taxonomy = document.getElementsByClassName("check_button_taxonomy")
    var taxonomy_string = '';
    for(var i = 0; i < check_buttons_taxonomy.length; i++) {
        if(check_buttons_taxonomy[i].checked === true){
            taxonomy_string = check_buttons_taxonomy[i].value + "," + taxonomy_string;
        }
    }
    return  taxonomy_string;
}

function download_csv_from_db() {
    var all_ref_ids = rows_selected;
    var taxonomy = check_taxonomy_dl();
    $.ajax({
        url: '/download_files_csv/' + all_ref_ids +'/'+ taxonomy,
        type: 'GET',
        context: document.body,
        xhrFields:{
            responseType: 'blob'
        },
        success: function(data) {
            let date = new Date().toJSON();
            let filename = date.concat(".csv")
            saveAs(data, filename);
        }
    });
}

function download_file_from_db() {
    var all_ref_id = rows_selected;
    var formats = check_format_dl();
    $.ajax({
        url: '/download_files/' + all_ref_id +'/'+ formats,
        type: 'GET',
        context: document.body,
        xhrFields:{
            responseType: 'blob',
        },
        success: function(data) {
            let date = new Date().toJSON();
            let filename = date.concat(".zip")
            saveAs(data, filename);
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
        var el_silva = document.createElement("p");
        var nd_silva = document.createTextNode("Not Classified");
        el_silva.appendChild(nd_silva);
        el_silva.setAttribute("id", "silva_taxon"+bench_id)
        document.getElementById("silva_div"+bench_id).appendChild(el_silva);
    }
    if (document.getElementById("ena_taxonomy" + bench_id).innerHTML.toString().split("'")[3] === 'Yes'){
        show_taxonomy_ena(bench_id);
    }else{
        var el_ena = document.createElement("p");
        var nd_ena = document.createTextNode("Not Classified");
        el_ena.appendChild(nd_ena);
        document.getElementById("ena_div"+bench_id).appendChild(el_ena);
    }
    if (document.getElementById("ltp_taxonomy" + bench_id).innerHTML.toString().split("'")[3] === 'Yes'){
        show_taxonomy_ltp(bench_id);
    }else{
        var el_ltp = document.createElement("p");
        var nd_ltp = document.createTextNode("Not Classified");
        el_ltp.appendChild(nd_ltp);
        document.getElementById("ltp_div"+bench_id).appendChild(el_ltp);
    }
    if (document.getElementById("ncbi_taxonomy" + bench_id).innerHTML.toString().split("'")[3] === 'Yes'){
        show_taxonomy_ncbi(bench_id);
    }else{
        var el_ncbi = document.createElement("p");
        var nd_ncbi = document.createTextNode("Not Classified");
        el_ncbi.appendChild(nd_ncbi);
        document.getElementById("ncbi_div"+bench_id).appendChild(el_ncbi);
    }
    if (document.getElementById("gtdb_taxonomy" + bench_id).innerHTML.toString().split("'")[3] === 'Yes'){
        show_taxonomy_gtdb(bench_id);
    }else{
        var el_gtdb = document.createElement("p");
        var nd_gtdb = document.createTextNode("Not Classified");
        el_gtdb.appendChild(nd_gtdb);
        document.getElementById("gtdb_div"+bench_id).appendChild(el_gtdb);
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
    var ltp = document.getElementById('ltp_taxonomy'+bench_id).innerHTML.toString();
    var temp = ltp.split("'");
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
    var ncbi = document.getElementById('ncbi_taxonomy'+bench_id).innerHTML.toString();
    var temp = ncbi.split("'");
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
