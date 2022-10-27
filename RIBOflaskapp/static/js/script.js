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
            result = result + "," + check_buttons[i].value;

        }
    }
    return  result;
}


function download_file_from_db() {
    var all_ref_id = get_all_ref_ids();
    var format = check_format_dl();
    $.ajax({
        url:'/download_files/?variable='+all_ref_id+"&format="+format,
        type: 'GET',
        context: document.body,
        success: function(response){
                alert("Download completed");
            },
    });

}


function redirect_to_download() {
    var content = get_data_rows();
    for (var i = 0; i < content.length; i++) {
        localStorage.setItem(i.toString(), content[i].toString());
    }
}

function showHideRow(row) {
    $("#" + row).toggle();
}