selectedImages = []

function openProcess() {
    $('#processModal').modal('show');
    var list = $('#process-files-list');
    list.empty();
    selectedImages.forEach(element => {
        list.append(`<li class="list-group-item"><a>${IMAGES[element].name}</a></li>`);
    });
}

function openUpload() {
    $('#uploadModal').modal('show');
    $.ajax({
        type: "GET",
        url: REQUEST_UPLOAD_URL,
        success: (msg) => { populateUploadForm(msg); },
        headers: {
            "X-CSRFToken": CSRF_TOKEN
        },
    });
}

function populateUploadForm(msg) {
    $('#upload-form').attr('action', msg.url);
    $('#aws-file-key').val(msg.fields.key);
    $('#aws-access-key').val(msg.fields.AWSAccessKeyId);
    $('#aws-acl').val(msg.fields.acl);
    $('#aws-policy').val(msg.fields.policy);
    $('#aws-signature').val(msg.fields.signature);
    $('#aws-security-token').val(msg.fields['x-amz-security-token']);
    //$('#aws-success_status').val(msg.fields['success_action_status']);

}

function getPresignedUploadRequest() {

}

function sendUploadRequest() {
    $("#upload-form").submit(function(event) {
        var filename = $('#input-file-upload')[0].files[0].name;
        event.preventDefault(); //prevent default action 
        var post_url = $(this).attr("action"); //get form action url
        var request_method = $(this).attr("method"); //get form GET/POST method
        fetch(post_url, {
            method: request_method,
            body: new FormData(this)
        }).then(data => {
            console.log(data);
            if (data.ok) {
                console.log(filename);
            }
        });

    });

    $('#upload-form').submit();
}

function sendProcessRequest() {
    console.log("sending");
    filenameList = selectedImages.map((i) => IMAGES[i].name);
    data = {
        'source-file-names': filenameList,
        'image-processor-type': $('#image-processor-type').val()
    };
    console.log(JSON.stringify(data));
    $.ajax({
        type: "POST",
        url: PROCESS_URL,
        success: (r) => { console.log('request success'); },
        data: JSON.stringify(data),
        contentType: "application/json",
        headers: {
            "X-CSRFToken": CSRF_TOKEN
        },
    });
}

function selectImage(index) {
    $('.images-container').children().eq(index).toggleClass('selected');
    if (selectedImages.includes(index)) {
        selectedImages = selectedImages.filter(function(e) { return e !== index });
    } else {
        selectedImages.push(index);
    }
}