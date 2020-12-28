function processQueryParamsMap(queryParamsMap) {
    var queryParams = "?";

    if (queryParamsMap != null) {
        queryParamsMap.forEach(function(value, key){
            value = encodeURIComponent(value)
            queryParams = queryParams + key + "=" + value +  "&"
        })
        queryParams = queryParams.slice(0,-1);
    } else
        queryParams = ""

    return queryParams;
}

// function makeRequest(requestObject){
//     makeRequestHelper(
//         requestObject.method,
//         requestObject.url,
//         requestObject.queryParamsMap,
//         requestObject.headers,
//         requestObject.data,
//         requestObject.contentType,
//         requestObject.successCallback,
//         requestObject.errorCallback
//         )
// }

// function makeRequestHelper(method = "GET", url, queryParamsMap, headers, data, contentType = _config.api.contentType.appjson, successCallback = defaultSuccessCallback, errorCallback = defaultErrorCallback) {
//     $.ajax({
//         // method: 'POST',
//         method: method,
//         // url: _config.api.invokeUrl + '/ride',
//         url: url + processQueryParamsMap(queryParamsMap),
//         // headers: {
//         //     Authorization: authToken
//         // },
//         headers: headers,
//         // data: JSON.stringify({
//         //     PickupLocation: {
//         //         Latitude: pickupLocation.latitude,
//         //         Longitude: pickupLocation.longitude
//         //     }
//         // }),
//         data: data,
//         // contentType: 'application/json',
//         contentType: contentType,
//         // success: completeRequest,
//         success: successCallback,
//         // error: function ajaxError(jqXHR, textStatus, errorThrown) {
//         //     console.error('Error requesting ride: ', textStatus, ', Details: ', errorThrown);
//         //     console.error('Response: ', jqXHR.responseText);
//         //     alert('An error occured when requesting your unicorn:\n' + jqXHR.responseText);
//         // }
//         error: errorCallback
//     });
// }

function defaultSuccessCallback(result) {
    console.log("Inside defaultSuccessCallback")
    console.log(result);
}

function defaultErrorCallback(result) {
    console.log("Inside defaultErrorCallback")
    console.log(result);
}