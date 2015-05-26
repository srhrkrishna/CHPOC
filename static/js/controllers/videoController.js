openstackApp.controller('videoController', ['$scope', '$http', '$modalInstance', 'fileInfo',
    function($scope, $http, $modalInstance, fileInfo) {

        var baseUrl = App_Constants.url + '/video/',
            url;

        $scope.closePopup = function() {
            $modalInstance.dismiss('cancel');
        };

        $scope.playVideo = function() {
            var extension = fileInfo.substr( (fileInfo.lastIndexOf('.') +1) );
            if (extension != 'mp4') {
                document.getElementById('message').style.display='block';
                document.getElementById('videoPlr').style.display='none';
                return;
            }
            document.getElementById('message').style.display='none';
            document.getElementById('videoPlr').style.display='block';

            url = baseUrl + fileInfo + '/stream/' + App_Constants.auth;
            $http.get(url).
            success(function(data, status) {
                video_tag = document.getElementById('videoPlr');
                source_tag = document.getElementById('mp4Source');
                video_tag.setAttribute('src', data)
                // video_tag.src = data;
                video_tag.load();

                video_tag.addEventListener('canplaythrough', function() {
                    video_tag = document.getElementById('videoPlr');
                    video_tag.play();
                }, false);

                // video_tag.play();
                // App_Constants.videourl = data;
            }).error(function(data, status) {

            });
        }
    }
]);

// openstackApp.filter('trusted', ['$sce', function ($sce) {
//     return function(url) {
//         return $sce.trustAsResourceUrl(url);
//     };
// }]);

// video_tag = document.getElementById('videoPlr');
// video_tag.on('loadeddata', function(event) {
//     video_tag.play();
// });