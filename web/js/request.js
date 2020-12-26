function processQueryParamsMap(queryParamsMap) {
    var queryParams = "?"

    if (queryParamsMap != null) {
        
        queryParamsMap.forEach(function(value, key){
          queryParams = queryParams + key "=" value +  "&"
        })
        queryParams = queryParams.slice(0,-1);
    } else
        queryParams = ""

    return queryParams
}

function makeRequest(method, url, queryParamsMap, headers, data, contentType, successCallback, errorCallback) {
    $.ajax({
        // method: 'POST',
        method: method,
        // url: _config.api.invokeUrl + '/ride',
        url: url + processQueryParamsMap(queryParamsMap),
        // headers: {
        //     Authorization: authToken
        // },
        headers: headers,
        // data: JSON.stringify({
        //     PickupLocation: {
        //         Latitude: pickupLocation.latitude,
        //         Longitude: pickupLocation.longitude
        //     }
        // }),
        data: data,
        // contentType: 'application/json',
        contentType: contentType,
        // success: completeRequest,
        success: successCallback,
        // error: function ajaxError(jqXHR, textStatus, errorThrown) {
        //     console.error('Error requesting ride: ', textStatus, ', Details: ', errorThrown);
        //     console.error('Response: ', jqXHR.responseText);
        //     alert('An error occured when requesting your unicorn:\n' + jqXHR.responseText);
        // }
        error: errorCallback
    });
}