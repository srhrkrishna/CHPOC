openstackApp.controller('videoController', ['$scope', '$http', '$modalInstance', 'fileInfo',
    function($scope, $http, $modalInstance, fileInfo) {

        var baseUrl = App_Constants.url + '/video/',
            url;
        $scope.videourl = "http://169.53.139.163/static/videos/rdk20150512_044038.mp4";

        $scope.closePopup = function() {
            $modalInstance.dismiss('cancel');
        };

        $scope.playVideo = function() {
            url = baseUrl + fileInfo + '/stream/' + App_Constants.auth;
            $http.get(url).
            success(function(data, status) {
                $scope.videourl = data;
            }).error(function(data, status) {
        		
            });
        }
    }
]);

openstackApp.filter('trusted', ['$sce', function ($sce) {
    return function(url) {
        return $sce.trustAsResourceUrl(url);
    };
}])