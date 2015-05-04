openstackApp.service('openstackService', ['$rootScope', '$http', function ($rootScope, $http) {

    var apiCall = { 
        isDownloading: false
        , request: null
    }, baseUrl = App_Constants.url + '/video/', url;

    function createCORSRequest(method, url) {
        var xhr = new XMLHttpRequest();
        if ("withCredentials" in xhr) {
            xhr.open(method, url, true);
            xhr.responseType = 'arraybuffer';
        } else {
            xhr = null;
        }
        return xhr;
    };

    apiCall.request = function makeCorsRequest(link) {  

        url = baseUrl + link,
        xhr = createCORSRequest('GET', url);

        if (!xhr) {
            console.log('CORS not supported');
            return;
        }
        apiCall.isDownloading = true;

        xhr.setRequestHeader("x-a12n", App_Constants.auth);
        //xhr.setRequestHeader("filename", link);

        xhr.onload = function () {
            var text = xhr.response;
            var file = new Blob([text], {
                type: 'video/mp4'
            });
            apiCall.isDownloading = false;
            $rootScope.$apply();
            var fileURL = URL.createObjectURL(file);
            var a = document.createElement('a');
            a.href = fileURL;
            a.target = '_blank';
            a.download = link;
            document.body.appendChild(a);
            a.click();
            console.log('XMLHTTPRequest Success.');
        };

        xhr.onerror = function () {
            console.log('XMLHTTPRequest Error.');
            apiCall.isDownloading = false;
        };

        xhr.send();
    };

    apiCall.viewMetadata = function(success, error, info) {

        success();
        
    }
    
    return apiCall;


}]);

