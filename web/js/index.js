$(document).ready(function () {

    $( "#fileUploaderForm" ).submit(function( event ) {
        files = event.target[0].files
        
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

        event.preventDefault();
    });

});

function upload(event, file) {
    makeRequest(
        'GET',
        _config.api.invokeUrl + '/upload-url',
        new Map([
            ["filename" ,file.name],  
            ["contentType", file.type]
        ]),
        null,
        null,
        _config.contentType.appjson,
        successCallback,
        successCallback)


    event.target.reset();
}

function multipartUpload(event, file) {
    parseFile(event, file, function(result){
        // TODO
        // console.log(result);

    })
}

// makeRequest('GET', "https://t8p0b4729e.execute-api.us-east-1.amazonaws.com/uploads", null, null, "application/json", successCallback, successCallback)

function successCallback(result) {
    console.log("SUCCESS");
    console.log(result);
}

function completeRequest(result) {
    var unicorn;
    var pronoun;
    console.log('Response received from API: ', result);
    unicorn = result.Unicorn;
    pronoun = unicorn.Gender === 'Male' ? 'his' : 'her';
    displayUpdate(unicorn.Name + ', your ' + unicorn.Color + ' unicorn, is on ' + pronoun + ' way.');
    animateArrival(function animateCallback() {
        displayUpdate(unicorn.Name + ' has arrived. Giddy up!');
        WildRydes.map.unsetLocation();
        $('#request').prop('disabled', 'disabled');
        $('#request').text('Set Pickup');
    });
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
