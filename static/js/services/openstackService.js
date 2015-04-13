openstackApp.service('openstackService', ['$rootScope', function ($rootScope) {

    var apiCall = { 
        isDownloading: false
        , request: null
    }, url = App_Constants.url + '/video/';

    function createCORSRequest(method, url) {
        var xhr = new XMLHttpRequest();
        xhr.responseType = 'arraybuffer';
        if ("withCredentials" in xhr) {
            xhr.open(method, url, true);
        } else {
            xhr = null;
        }
        return xhr;
    };

    apiCall.request = function makeCorsRequest() {  

        var xhr = createCORSRequest('POST', url);
        if (!xhr) {
            console.log('CORS not supported');
            return;
        }
        apiCall.isDownloading = true;

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
            a.download = 'test.mp4';
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
    
    return apiCall;


}]);

