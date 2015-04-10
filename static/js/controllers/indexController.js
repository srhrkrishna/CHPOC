openstackApp.controller('indexController', ['$scope', '$modal', 'openstackService', function ($scope, $modal, openstackService) {

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
    });
    
    $scope.downloadFile = function() {
        openstackService.request();
    }

    $scope.links = [{ name: "File Name 1", url: "#" }, { name: "File Name 2", url: "#" }];

}]);
