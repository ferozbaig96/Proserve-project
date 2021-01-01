var abc=null
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

    $( "#fileSearchForm" ).submit(function (event) {
        event.preventDefault();
        q = event.target[0].value
        searchFiles(q)
        event.target.reset();
    });

    $( "#fileDeleteForm" ).submit(function (event) {
        event.preventDefault();
        filename = event.target[0].value
        deleteFile(filename)
        event.target.reset();
    });
});

function searchFiles(q) {
    var queryParamsMap = new Map([
                    ["query" ,q]
            ])
    $.ajax({
            method: "GET",
            url : _config.api.invokeUrl + '/files' + processQueryParamsMap(queryParamsMap),
            beforeSend: function() {
              $(".loader").show();
              $("#searchResultsTable tr").remove(); 
            },
            success: function (results) {
                var table = document.getElementById("searchResultsTable")
                for (i in results){
                    row = table.insertRow(0);
                    cell = row.insertCell(0);
                    name = results[i].name
                    name = name.replaceAll('+',' ')
                    url = results[i].url
                    cell.innerHTML = '<a href='+url+'  target="_blank">'+name+'</a>'
                }
                $(".loader").hide();
            },
            error: function (e) {
                $(".loader").hide();
                console.log(e);
            }
        });
}

function progress(evt){
    if (evt.lengthComputable) {
        var percentComplete = 100 * evt.loaded / evt.total;
        console.log(percentComplete);
        percentComplete = percentComplete.toFixed(2)
        document.getElementById("loader-info").innerHTML = percentComplete + ' %'
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
            beforeSend: function() {
              $(".loader").show();
            },
            success: callback,
            error: function (e) {
                console.log(e);
                alert("Some error occurred");
                $(".loader").hide();
            },
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
            beforeSend: function() {
              $(".loader").show();
              $("#loader-info").show();
            },
            success: function (event){
                console.log("File uploaded successfully")
                alert("File uploaded successfully")
                $(".loader").hide();
                $("#loader-info").hide();
            },
            error: function (e) {
                console.log(e);
                alert("Some error occurred");
                $(".loader").hide();
                $("#loader-info").hide();
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

function deleteFile(filename){
    $.ajax({
        method: "DELETE",
        url : _config.api.invokeUrl + '/delete-file',
        processData: false,  // tells jQuery not to process the data
        headers: {
            "Content-Type": "application/json"
        },
        data: JSON.stringify({
            "objectKey": filename
        }),
        beforeSend: function() {
              $(".loader").show();
            },
        success: function (event){
            console.log("File deleted successfully")
            $(".loader").hide();
            alert("File deleted successfully")
        },
        error: function (e) {
            console.log(e);
            $(".loader").hide();
            alert("Some error occurred")
        }
    });
}
