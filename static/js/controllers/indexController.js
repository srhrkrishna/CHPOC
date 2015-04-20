openstackApp.controller('indexController', ['$scope', '$modal', 'openstackService', 'videoService', function ($scope, $modal, openstackService, videoService) {

    var modalInstance = null;

    $scope.apiCall = openstackService;

    $scope.showLogin = function () {
        modalInstance = $modal.open({
            templateUrl: 'html/login.html',
            controller: 'loginController',
            backdrop: 'static',
            keyboard: false
        });
    };

    $scope.currentUser = "";

    $scope.$on("loginSuccess", function (event, args) {
        if (args.username) {
            $scope.currentUser = args.username;
        }
        videoService.getVideos(function(data){
            $scope.links = data;
        });
    });
    
    $scope.downloadFile = function(link) {
        openstackService.request(link);
    }

    //$scope.links = [{ name: "File Name 1", url: "#" }, { name: "File Name 2", url: "#" }];

}]);
