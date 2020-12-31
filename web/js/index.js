$(document).ready(function () {

    $( "#fileUploaderForm" ).submit(function( event ) {
        event.preventDefault();
        files = event.target[0].files;
        
        if (files.length == 0) {
            alert("Select a file to upload")
            event.preventDefault();
        }
        else {
            fileSize = files[0].size;
            MB_16 = 16 * 1024 * 1024;
            if (fileSize <= MB_16)
                upload(event, files[0]);
            else
                multipartUpload(event, files[0]);
        }
    });

});

function progress(evt){
    if (evt.lengthComputable) {
        var percentComplete = 100 * evt.loaded / evt.total;
        //Do something with download progress
        console.log(percentComplete);
    }
}

function upload(event, file) {
    
    function getUploadUrl(file, callback){
        var queryParamsMap = new Map([
                    ["filename" ,file.name],  
                    ["contentType", file.type]
            ])
        $.ajax({
            method: "GET",
            url : _config.api.invokeUrl + '/upload-url' + processQueryParamsMap(queryParamsMap),
            success: callback
        });
    }

    function sendData(uploadUrl){
        $.ajax({
            method : "PUT",
            url : uploadUrl,
            data : file,
            processData: false,  // tells jQuery not to process the data
            headers: {
                "Content-Type": file.type
            },
            success: function (event){
                console.log("File uploaded successfully")
                alert("File uploaded successfully")
            },
            error: function (e) {
                console.log(e);
                alert("Some error occurred")
            },
            xhr: function(){
                var xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener("progress", progress, false);
                return xhr;
            }
        })
    }

    getUploadUrl(file, sendData)

    // var queryParamsMap = new Map([
    //                 ["filename" ,file.name],  
    //                 ["contentType", file.type]
    //         ])

    // $.ajax({
    //     method: "GET",
    //     url : _config.api.invokeUrl + '/upload-url' + processQueryParamsMap(queryParamsMap),
    //     success: function (event) {
    //         var formData = new FormData();
    //         formData.append("file", file);
    //         $.ajax({
    //             method : "PUT",
    //             url : event,
    //             data : formData,
    //             processData: false,  // tells jQuery not to process the data
    //             headers: {
    //                 "Content-Type": file.type
    //             },
    //             success: defaultSuccessCallback,
    //             error: defaultErrorCallback
    //         })
    //     }
    // });

    event.target.reset();
}

function multipartUpload(event, file) {
    parseFile(event, file, function(result){
        // TODO
        // console.log(result);

    })
}

function parseFile(event, file, callback) {
    var fileSize   = file.size;
    // TODO make 10 MB
    var chunkSize  = 64 * 1024; // 64 KB chunks
    var offset     = 0;
    var self       = this; // we need a reference to the current object
    var chunkReaderBlock = null;

    var readEventHandler = function(evt) {
        if (evt.target.error == null) {
            offset += chunkSize;
            callback(evt.target.result); // callback for handling read chunk
        } else {
            console.log("Read error: " + evt.target.error);
            return;
        }
        if (offset >= fileSize) {
            console.log("Done reading file");
            event.target.reset();
            return;
        }

        // of to the next chunk
        chunkReaderBlock(offset, chunkSize, file);
    }

    chunkReaderBlock = function(_offset, length, _file) {
        var r = new FileReader();
        var blob = _file.slice(_offset, length + _offset);
        r.onload = readEventHandler;
        r.readAsText(blob);
        // r.readAsArrayBuffer(blob);
    }

    // now let's start the read with the first block
    chunkReaderBlock(offset, chunkSize, file);
}

// todo add arguments: event, file
function deleteFile(filename){
    $.ajax({
        method: "DELETE",
        url : _config.api.invokeUrl + '/delete-file',
        processData: false,  // tells jQuery not to process the data
        headers: {
            "Content-Type": "application/json"
        },
        data: JSON.stringify({
            // todo replace with file.name
            "objectKey": filename
        }),
        success: function (event){
            console.log("File deleted successfully")
            alert("File deleted successfully")
        },
        error: function (e) {
            console.log(e);
            alert("Some error occurred")
        }
    });
}

function search(query){
    $.ajax({
        method: "GET",
        url : _config.api.invokeUrl + '/files' + '?query=' + query,
        success: function (event){
            console.log(event)
        },
        error: function (e) {
            console.log(e);
            alert("Some error occurred")
        }
    });
}