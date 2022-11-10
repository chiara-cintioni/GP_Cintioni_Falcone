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
        var row = button.parentElement;
        var tds = row.getElementsByTagName('td');
        var tds_array = [];
        for (var i = 1; i < tds.length; i++) {
            tds_array[i - 1] = tds.item(i).innerText;
        }
        return tds_array;
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
    var rows = document.getElementsByTagName("tr");
    var ref_id_string = '';
    for(var i = 1; i < rows.length; i++) {
        if (i % 2 !== 0) {
            var temp = get_reference_id(rows[i]);
            if (temp !== '') {
                ref_id_string = ref_id_string + temp + ",";
            }
        }
    }
    return ref_id_string;
}

function download() {
    var content = get_table_header().concat("\n", get_data_rows())

    var blob = new Blob(content, {
        type: "text/plain;charset=utf-8"
    });
    saveAs(blob, "search-result.csv");
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

/*
function download_file_from_db() {
    var all_ref_id = get_all_ref_ids();
    var format = check_format_dl();
    $.ajax({
        url:'/download_files/'+all_ref_id,
        type: 'GET',
        context: document.body,
        success: function(response){
                alert("Download completed");
            },
    });

}*/
function download_file_from_db() {
    var all_ref_id = get_all_ref_ids();
    var formats = check_format_dl();
    $.ajax({
        url: '/download_files/' + all_ref_id +'/'+ formats,
        type: 'GET',
        context: document.body,
        xhrFields:{
            responseType: 'blob'
        },
        success: function(data) {
            saveAs(data, "test.zip");

        }
    });
}



/*
function final_download() {
    var row = document.getElementById('table_row');
    var ref_id = get_reference_id(row);
     $.ajax({
        url:'/download/?variable='+ref_id,
        type: 'GET',
        context: document.body,
        success: function(response){
                alert("Download completed");
            },
    });
}
*/

function redirect_to_download() {
    var content = get_data_rows();
    for (var i = 0; i < content.length; i++) {
        localStorage.setItem(i.toString(), content[i].toString());
    }
}

function showHideRow(row) {
    $("#" + row).toggle();
}

function show_taxonomy(){
    if (document.getElementById('silva_taxonomy').innerHTML.toString().split("'")[3] === 'Yes'){
        show_taxonomy_silva();
    }else{
        var el = document.createElement("p");
        var nd = document.createTextNode("Not Classified");
        el.appendChild(nd);
        document.getElementById("silva_div").appendChild(el);
    }
    show_taxonomy_ena();
    show_taxonomy_ltp();
    show_taxonomy_ncbi();
    show_taxonomy_gtdb();
}

function show_taxonomy_silva() {
    var silva = document.getElementById('silva_taxonomy').innerHTML.toString();
    var temp = silva.split("'");
    var position = document.getElementById("silva_div");
    var rank_cont = 0
    for (var i = 5; i< temp.length;i++){
        for(var j=0; j<temp.length; j++){
            if(i%2 !== 0){
                if(rank_cont%2 === 0){
                    var element = document.createElement("p");
                    element.setAttribute("id","silva_rank")
                }else{
                    var element = document.createElement("p");
                    element.setAttribute("id","silva_taxon");
                }
                rank_cont++;
                var node = document.createTextNode(temp[i]);
                element.appendChild(node);
                position.appendChild(element);
                break;
            }
        }
    }
}

function show_taxonomy_ena() {
    var ena = document.getElementById('ena_taxonomy').innerHTML.toString();
    var temp = ena.split("'");
    var position = document.getElementById("ena_div");
    var rank_cont = 0
    for (var i = 5; i< temp.length;i++){
        for(var j=0; j<temp.length; j++){
            if(i%2 !== 0){
                if(rank_cont%2 === 0){
                    var element = document.createElement("p");
                    element.setAttribute("id","ena_rank")
                }else{
                    var element = document.createElement("p");
                    element.setAttribute("id","ena_taxon");
                }
                rank_cont++;
                var node = document.createTextNode(temp[i]);
                element.appendChild(node);
                position.appendChild(element);
                break;
            }
        }
    }
}

function show_taxonomy_gtdb() {
    var gtdb = document.getElementById('gtdb_taxonomy').innerHTML.toString();
    var temp = gtdb.split("'");
    var position = document.getElementById("gtdb_div");
    var rank_cont = 0
    for (var i = 5; i< temp.length;i++){
        for(var j=0; j<temp.length; j++){
            if(i%2 !== 0){
                if(rank_cont%2 === 0){
                    var element = document.createElement("p");
                    element.setAttribute("id","gtdb_rank")
                }else{
                    var element = document.createElement("p");
                    element.setAttribute("id","gtdb_taxon");
                }
                rank_cont++;
                var node = document.createTextNode(temp[i]);
                element.appendChild(node);
                position.appendChild(element);
                break;
            }
        }
    }
}

function show_taxonomy_ltp() {
    var ena = document.getElementById('ltp_taxonomy').innerHTML.toString();
    var temp = ena.split("'");
    var position = document.getElementById("ltp_div");
    var rank_cont = 0
    for (var i = 5; i< temp.length;i++){
        for(var j=0; j<temp.length; j++){
            if(i%2 !== 0){
                if(rank_cont%2 === 0){
                    var element = document.createElement("p");
                    element.setAttribute("id","ltp_rank")
                }else{
                    var element = document.createElement("p");
                    element.setAttribute("id","ltp_taxon");
                }
                rank_cont++;
                var node = document.createTextNode(temp[i]);
                element.appendChild(node);
                position.appendChild(element);
                break;
            }
        }
    }
}

function show_taxonomy_ncbi() {
    var ena = document.getElementById('ncbi_taxonomy').innerHTML.toString();
    var temp = ena.split("'");
    var position = document.getElementById("ncbi_div");
    var rank_cont = 0
    for (var i = 5; i< temp.length;i++){
        for(var j=0; j<temp.length; j++){
            if(i%2 !== 0){
                if(rank_cont%2 === 0){
                    var element = document.createElement("p");
                    element.setAttribute("id","ncbi_rank")
                }else{
                    var element = document.createElement("p");
                    element.setAttribute("id","ncbi_taxon");
                }
                rank_cont++;
                var node = document.createTextNode(temp[i]);
                element.appendChild(node);
                position.appendChild(element);
                break;
            }
        }
    }
}