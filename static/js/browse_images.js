function openImageRequest(name) {
    $('#myModal').modal('show');
    $('#request-image').attr("src", AWS_BUCKET_URL + name);
    $('#source-file-name').val(name);
    $('#destination-file-name').val(Date.now() + "_" + name);
}

function sendRequest() {
    console.log("sending");
    $('#request-form').submit();
}