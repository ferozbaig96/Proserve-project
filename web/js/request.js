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

function defaultSuccessCallback(result) {
    console.log("Inside defaultSuccessCallback")
    console.log(result);
}

function defaultErrorCallback(result) {
    console.log("Inside defaultErrorCallback")
    console.log(result);
}