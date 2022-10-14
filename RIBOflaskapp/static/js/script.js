function check_input_length(){
     var any = document.forms.RegForm.Length.value;
     var from = document.forms.RegForm.Length_from.value;
     var to = document.forms.RegForm.Length_to.value;
     if (any !== '' && from !== '' || to !== ''){
        window.alert("You can only enter a specific length or a range.");
        any.focus();
        return "No";
     }
     return "Ok"
}

function check_input_weak_bonds(){
     var any = document.forms.RegForm.Number_of_weak_bonds.value;
     var from = document.forms.RegForm.Number_of_weak_bonds_from.value;
     var to = document.forms.RegForm.Number_of_weak_bonds_to.value;
     if (any !== '' && from !== '' || to !== ''){
        window.alert("You can only enter a specific number of base pairs or a range.");
        any.focus();
        return false;
     }
     return true
}