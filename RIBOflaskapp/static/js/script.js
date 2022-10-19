function check_input_length() {
    var any = document.forms.RegForm.Length.value
    var from = document.forms.RegForm.Length_from.value
    var to = document.forms.RegForm.Length_to.value
    if (any !== '' && (from !== '' || to !== '')) {
        window.alert("You can only enter a specific length or a range.")
    }
}

function check_input_weak_bonds() {
    var any = document.forms.RegForm.Number_of_weak_bonds.value;
    var from = document.forms.RegForm.Number_of_weak_bonds_from.value;
    var to = document.forms.RegForm.Number_of_weak_bonds_to.value;
    if (any !== '' && (from !== '' || to !== '')) {
        window.alert("You can only enter a specific number of base pairs or a range.");
        return false;
    }
    return true
}

function get_row_data(button) {
    var boolean_button = button.firstElementChild.checked;
    if (boolean_button === true) {
        var row = button.parentElement;
        var tds = row.getElementsByTagName('td');
        var tds_array = [];
        for (var i = 1; i < tds.length; i++) {
            tds_array[i-1] = tds.item(i).innerText;
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
        array_temp = get_row_data(rows.item(i).firstElementChild);
        array = array.concat(array_temp+"\n");
    }
    return array;
}

function get_table_header() {
    var rows = document.getElementsByTagName('tr');
    var row = rows[0];
    var ths = row.getElementsByTagName('th');
    var ths_array = [];
    for (var i = 1; i < ths.length; i++) {
        if(i===(ths.length-1)){
            ths_array[i - 1] = ths.item(i).innerText;
        }else{
            ths_array[i - 1] = ths.item(i).innerText + ",";
        }
    }
    return ths_array;
}

function download() {
    var content = get_table_header().concat("\n", get_data_rows());
    var blob = new Blob(content, {
        type: "text/plain;charset=utf-8"
    });
    saveAs(blob, "sample-file.csv");
}



