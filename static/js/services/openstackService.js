openstackApp.service('openstackService', ['$http', function ($http) {

    var url = 'http://169.53.139.163:8000/video/';

    function createCORSRequest(method, url) {
        var xhr = new XMLHttpRequest();
        xhr.responseType = 'arraybuffer';
        if ("withCredentials" in xhr) {
            xhr.open(method, url, true);
        } else {
            xhr = null;
        }
        return xhr;
    }

    var apiCall = function makeCorsRequest() {        

        var xhr = createCORSRequest('POST', url);
        if (!xhr) {
            console.log('CORS not supported');
            return;
        }

        xhr.onload = function () {
            var text = xhr.response;
            var file = new Blob([text], {
                type: 'video/mp4'
            });
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
        };

        xhr.send();
    }
    
    return apiCall;

    //makeCorsRequest();


}]);

