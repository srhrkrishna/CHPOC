openstackApp.controller('loginController', ['$scope', '$rootScope', '$modalInstance', 'loginService','jsonService','jsonFolderService',function ($scope, $rootScope, $modalInstance, loginService,jsonService,jsonFolderService) {

    $scope.user = {
        username: "",
        password: ""
    }

    $scope.loginFailed = false;

    $scope.signIn = function () {
        var info = {
            ConsumerNumber: 'sreehari.parameswaran@cognizant.com',
            Password: 'Admin1234$$'
        };

       // jsonService.login();

        loginService.login(function (success) {
            $scope.loginFailed = !success;
            $rootScope.$broadcast("loginSuccess", {
                username: $scope.user.username
            });
            $modalInstance.dismiss('cancel');
        }, function () {
            $scope.loginFailed = true;
        }, info);
    };

    $scope.cancelSignIn = function () {

    };


}]);