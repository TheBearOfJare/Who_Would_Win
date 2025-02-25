

function toggle_take_photo() {
    if (document.getElementById("take_photo").checked) {
        document.getElementById("file_select").capture = "environment";
        document.getElementById("custom_file_upload").innerHTML = "Take a Photo";
        

    } else {
        document.getElementById("file_select").capture = null;
        document.getElementById("custom_file_upload").innerHTML = "Upload a Photo";
    }
}

function enable_submit_button() {
    document.getElementById("submit").disabled = false;
    // also update the file status

    document.getElementById("file_status").innerHTML = document.getElementById("file_select").files[0].name;
    document.getElementById("file_status").style.color = "green";

}