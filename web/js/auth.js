var redirect_uri = 'https://project.baigmohd.myinstance.com'
var LOGIN_URI = 'https://project.baigmohd.myinstance.com/login?client_id=r6idl4n64lotv1ijlvpv5sb0f&response_type=code&scope=openid&redirect_uri='+redirect_uri

var code = (new URLSearchParams(window.location.search)).get('code')

if ( code == null ) {
	window.location.href = LOGIN_URI
} else {
	var queryParamsMap = new Map([
                    ["code" ,code]
            ])
        $.ajax({
            method: "GET",
            url : _config.api.invokeUrl + '/token' + processQueryParamsMap(queryParamsMap),
            success: function (event) {
            	console.log(event)
            	if (event.error != null) {
            		window.location.href = LOGIN_URI
            	} else {
            		access_token = event.access_token
            		id_token = event.id_token
            		refresh_token = event.refresh_token
            		expires_in = event.expires_in

            		// todo check for security issues
            		decodedAccessToken = parseJwt(access_token)
            		if (decodedAccessToken['cognito:groups'] == null)
            			group = null
            		else
            			group = decodedAccessToken['cognito:groups'][0]

                    if (group == "admin") {
                        $( ".upload" ).show()
                        $( ".delete" ).show()
                    }
            	}
            }
        });
}

function parseJwt (token) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
};