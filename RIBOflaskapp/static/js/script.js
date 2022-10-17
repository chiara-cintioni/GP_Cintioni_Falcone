import $ from "jquery";

function check_input_length(){
    var any = document.forms.RegForm.Length.value
    var from = document.forms.RegForm.Length_from.value
    var to = document.forms.RegForm.Length_to.value
    if (any !== '' && (from !== '' || to !== '')){
        window.alert("You can only enter a specific length or a range.")
        return false
    }
    return true
}


function check_input_weak_bonds(){
     var any = document.forms.RegForm.Number_of_weak_bonds.value;
     var from = document.forms.RegForm.Number_of_weak_bonds_from.value;
     var to = document.forms.RegForm.Number_of_weak_bonds_to.value;
     if (any !== '' && (from !== '' || to !== '')){
        window.alert("You can only enter a specific number of base pairs or a range.");
        return false;
     }
     return true
}

$(function() {
	//If check_all checked then check all table rows
	$("#check_all").on("click", function () {
		if ($("input:checkbox").prop("checked")) {
			$("input:checkbox[name='row-check']").prop("checked", true);
		} else {
			$("input:checkbox[name='row-check']").prop("checked", false);
		}
	});

	// Check each table row checkbox
	$("input:checkbox[name='row-check']").on("change", function () {
		let total_check_boxes = $("input:checkbox[name='row-check']").length;
		let total_checked_boxes = $("input:checkbox[name='row-check']:checked").length;

		// If all checked manually then check check_all checkbox
		if (total_check_boxes === total_checked_boxes) {
			$("#check_all").prop("checked", true);
		}
		else {
			$("#check_all").prop("checked", false);
		}
	});
});