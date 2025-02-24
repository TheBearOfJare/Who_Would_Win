function enable_file_upload() {
    document.getElementById("file_select").disabled = false;
}


function toggle_take_photo() {
    if (document.getElementById("take_photo").checked) {
        document.getElementById("file_select").capture = "environment";

    } else {
        document.getElementById("file_select").capture = null;
    }
}

function enable_submit_button() {
    document.getElementById("submit").disabled = false;
}