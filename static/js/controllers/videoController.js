openstackApp.controller('videoController', ['$scope', '$http', '$modalInstance', 'fileInfo',
    function($scope, $http, $modalInstance, fileInfo) {

        var baseUrl = App_Constants.url + '/video/',
            url;

        $scope.isMp4 = true;

        $scope.closePopup = function() {
            $modalInstance.dismiss('cancel');
        };

        $scope.playVideo = function() {
            var extension = fileInfo.substr( (fileInfo.lastIndexOf('.') +1) );
            $scope.isMp4 = extension !== 'mp4' ? false : true;

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